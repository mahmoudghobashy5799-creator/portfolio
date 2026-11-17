"""Check the generated site: links, resources, IDs, metadata, and artifact scope."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1] / 'dist'

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path, self.ids, self.links, self.errors = path, set(), [], []
        self.title, self.description, self.h1 = False, False, 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            if attrs['id'] in self.ids:
                self.errors.append(f'Duplicate id: {attrs["id"]}')
            self.ids.add(attrs['id'])
        if tag == 'title': self.title = True
        if tag == 'h1': self.h1 += 1
        if tag == 'meta' and attrs.get('name') == 'description': self.description = bool(attrs.get('content'))
        if tag == 'img' and not attrs.get('alt'): self.errors.append('Image missing descriptive alt text')
        if tag == 'img' and not (attrs.get('width') and attrs.get('height')): self.errors.append('Image missing dimensions')
        if tag == 'a' and attrs.get('target') == '_blank' and 'noopener' not in attrs.get('rel', ''): self.errors.append('External tab missing noopener')
        for key in ['href', 'src']:
            if key in attrs: self.links.append(attrs[key])

pages = {}
errors = []
for path in ROOT.glob('*.html'):
    page = Page(path)
    page.feed(path.read_text(encoding='utf-8'))
    pages[path.name] = page
    if not page.title or not page.description or page.h1 != 1: page.errors.append('Title, description, or unique h1 missing')
    errors += [f'{path.name}: {error}' for error in page.errors]

for page in pages.values():
    for link in page.links:
        url = urlsplit(link)
        if url.scheme or url.netloc: continue
        target = ROOT / unquote(url.path) if url.path else page.path
        if not target.is_file(): errors.append(f'{page.path.name}: missing {link}')
        if url.fragment and target.name in pages and url.fragment not in pages[target.name].ids:
            errors.append(f'{page.path.name}: broken anchor {link}')

if len(pages) != 2: errors.append('Expected homepage and case study')
allowed = {'.html', '.css', '.js', '.webp', '.png', '.svg', '.txt', '.xml', ''}
for path in ROOT.rglob('*'):
    if path.is_file() and path.suffix not in allowed: errors.append(f'Unexpected public file: {path.name}')
if errors: raise SystemExit('\n'.join(errors))
print(f'PASS: {len(pages)} pages; local links, anchors, image descriptions, metadata, and output file types.')
print(f'Public output size: {sum(p.stat().st_size for p in ROOT.rglob("*") if p.is_file()):,} bytes')
