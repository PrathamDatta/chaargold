# ChaarGold website (static)

Plain HTML/CSS/JS — host the folder on any static host (Vercel, Netlify, cPanel…). Open `index.html` via a local server, e.g. `python -m http.server`.

- Edit copy in `tools/build.py` (page content) or `data/*.json` (FAQ, Terms, Blog), then run `python tools/build.py` to regenerate the pages.
- Colours/typography: top of `assets/css/style.css` (`--gold:#bc9c23`, `--ink:#040404`).
- The Contact page has an on-site enquiry form (name, number, optional company, message). It posts to `FORM_ENDPOINT` in `tools/build.py` (currently FormSubmit, which emails contact@chaargold.com; the first submission needs a one-time confirmation click in that inbox). Product pages use `mailto:` buttons.
- Social links are placeholders: set `INSTAGRAM` / `FACEBOOK` in `tools/build.py`.
- `tools/prepare_assets.py`, `tools/prepare_new_assets.py` and `tools/extract_blog.py` were one-off scripts used to import the client's zips.
