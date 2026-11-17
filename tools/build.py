"""Build only allowlisted portfolio files. No project datasets enter the output."""
from pathlib import Path
from urllib.parse import urlparse
import argparse
import shutil

ROOT = Path(__file__).resolve().parents[1]
PAGES = ['index.html', 'movie-recommendation.html']
ASSETS = ['dashboard.webp', 'rating-distribution.webp', 'movies-by-genre.webp', 'social-card.png', 'favicon.svg']

def build(site_url=''):
    if site_url:
        parsed = urlparse(site_url)
        if parsed.scheme != 'https' or not parsed.netloc or parsed.query or parsed.fragment:
            raise ValueError('Public site URL must be an absolute HTTPS URL without query or fragment.')
        site_url = site_url.rstrip('/')
    out = ROOT / 'dist'
    out.mkdir(exist_ok=True)
    # This directory contains generated output only. Resolve before clearing it.
    if out.resolve().parent != ROOT.resolve() or out.is_symlink():
        raise ValueError('Unexpected build directory.')
    for item in out.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()
    (out / 'assets').mkdir()
    for name in PAGES:
        html = (ROOT / name).read_text(encoding='utf-8')
        if site_url:
            canonical = f'{site_url}/' if name == 'index.html' else f'{site_url}/{name}'
            html = html.replace('content="assets/social-card.png"', f'content="{site_url}/assets/social-card.png"')
            html = html.replace('</head>', f'  <link rel="canonical" href="{canonical}">\n  <meta property="og:url" content="{canonical}">\n</head>')
        (out / name).write_text(html, encoding='utf-8')
    for name in ['styles.css', 'script.js']:
        shutil.copy2(ROOT / name, out / name)
    for name in ASSETS:
        shutil.copy2(ROOT / 'assets' / name, out / 'assets' / name)
    (out / '.nojekyll').write_text('', encoding='utf-8')
    if site_url:
        (out / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {site_url}/sitemap.xml\n', encoding='utf-8')
        urls = [f'{site_url}/', f'{site_url}/movie-recommendation.html']
        (out / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{u}</loc></url>' for u in urls) + '</urlset>', encoding='utf-8')
    print(f'Built {len(list(out.rglob("*")))} entries in {out}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site-url', default='', help='Final HTTPS URL, including any GitHub Pages repository subpath.')
    build(parser.parse_args().site_url)
