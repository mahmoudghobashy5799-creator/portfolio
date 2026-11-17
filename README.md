# Mahmoud Ghobashy — Portfolio

A small, accessible static portfolio built for GitHub Pages. No framework, package installation, remote fonts, analytics, or server is required.

## Local preview

From this folder, using Python 3.10 or newer:

```powershell
python tools/build.py
python tools/check.py
python -m http.server 4173 --bind 127.0.0.1 --directory dist
```

Open http://127.0.0.1:4173. The source also works by opening `index.html` directly.

## Edit content

- `index.html`: name, introduction, skills, about section, selected work, and contact links.
- `movie-recommendation.html`: case study and its recorded results.
- `styles.css`: colors, typography, responsive layouts, and reduced-motion support.
- `script.js`: mobile menu and keyboard-accessible dashboard dialog.
- `assets/`: optimized project images, favicon, and social sharing image.

Run the build and check after edits. The build copies only an explicit list of public assets. Keep raw datasets, model files, original reports, credentials, and personal notes outside the public output. Keep `.review/` local.

## Publishing and future updates

The owner approved public publishing in this chat. Deployment repository: https://github.com/mahmoudghobashy5799-creator/portfolio. Check the repository’s Pages settings or latest successful deployment for the live URL.

The initial setup and deployment process:

1. Use the dedicated `portfolio` repository. Preserve the existing `Knowledge-hub` repository.
2. Push this portfolio's reviewed source to the repository's `main` branch. GitHub account authorization is required; never put tokens in source files.
3. Under Settings → Pages, set the build source to **GitHub Actions**.
4. Run the included **Publish portfolio to GitHub Pages** workflow, or push to `main` after Pages is configured.
5. Wait for the deployment, then check both the homepage and case study at the URL returned by the deployment. Check image loading, mobile navigation, email, and WhatsApp links.

The workflow gets the final base URL from GitHub Pages, including repository subpaths. The build then adds canonical URLs, absolute Open Graph image URLs, a sitemap, and robots.txt. Do not substitute a guessed URL.

To prepare a production build manually:

```powershell
python tools/build.py --site-url https://YOUR-ACCOUNT.github.io/portfolio
python tools/check.py
```

Replace the example URL with the real destination. Future updates are edits followed by commits to `main`; the workflow rebuilds and deploys automatically.

## Provenance and review

The owner confirmed the identity, title, education, skill list, contacts, and that the Movie Recommendation System is a completed individual course project. See `CONTENT_REVIEW.md` for copy and public-content review. The case study is grounded in local scripts and saved outputs; the owner approved the rendered portfolio for public publishing.

MovieLens is a GroupLens dataset. Only selected visualizations are included, with attribution; no raw data, model artifacts, PBIX files, source project scripts, or original PDFs are redistributed.

