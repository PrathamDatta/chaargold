# ChaarGold website (static)

Plain HTML/CSS/JS — host the folder on any static host (Vercel, Netlify, cPanel…). Open `index.html` via a local server, e.g. `python -m http.server`.

- Edit copy in `tools/build.py` (page content) or `data/*.json` (FAQ, Terms, Blog), then run `python tools/build.py` to regenerate the pages.
- Colours/typography: top of `assets/css/style.css` (`--gold:#bc9c23`, `--ink:#040404`).
- Enquiries use `mailto:` links to contact@chaargold.com (no forms). Social links are placeholders: set `INSTAGRAM` / `FACEBOOK` in `tools/build.py`.
- `tools/prepare_assets.py` and `tools/extract_blog.py` were one-off scripts used to import the client's zips.
