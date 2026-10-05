# Ending the Gaza War Must Restore Our Humanity · The Virtuous City Vision · website repo

A static site: two click-through slideshows (the pitch on the front page, the full deck on full.html), plus the PDF and plain-text editions. No framework, no build server. The infrastructure is a copy of the Islamabad Accords repo (dhanna11/islamabad-accords), duplicated on purpose (Oct 2026); de-duplicating the two is a later clean-up, so a fix to the shared parts (`build-slideshow.py`'s wrapper, `tests/`, the workflow) may need porting to the other repo.

## Files
- `index.html`: the front page, the **pitch** slideshow, built from `pitch/`. One self-contained page; it loads only Google Fonts from outside. Links to full-deck slides on it (`index.html#<id>`) forward to `full.html#<id>`.
- `full.html`: the **full deck** slideshow, built from `deck/`. Both pages carry a Pitch | Full deck switch.
- `virtuous-city-vision.md`: the plain-text edition, the author's essay as written; the "Ask Claude" / "Ask ChatGPT" buttons point the AI at it. Never edit its text except on the author's word.
- `virtuous-city-vision.pdf`: the PDF edition, linked from the PDF button. For now it is the full deck printed one slide per page.
- `.nojekyll`: keeps GitHub Pages from running Jekyll, which would turn the `.md` into an HTML page and break its URL.
- `deck/` and `pitch/`: the two decks in the Slides export format (`deck.json` for slide order and sections, `slides/<id>.html` for one slide each). These are the sources of `full.html` and `index.html`. Do not hand-edit `index.html` or `full.html`.
- `build-slideshow.py`: regenerates `index.html` from `pitch/` and `full.html` from `deck/` (plus `preview.html` and `preview-full.html`, never committed). It needs only Python 3.
- `README.md`: the human steps for GitHub Pages and a custom domain.
- `LICENSE` (MIT: build scripts, tests, workflow, page wrapper) and `LICENSE-CONTENT.md` (CC BY 4.0: text and design, in every edition).
- `.github/workflows/check.yml` and `tests/`: the check that runs on every PR (see "Checks").

## Where the deck lives
The first version of both decks (4 Oct 2026) was cut from the author's essay (`virtuous-city-vision.md`) in a Claude Code session: slide text is the essay's sentences, trimmed; headings and card labels were drawn from it. On 5 Oct 2026 both decks were regrouped into the six blocks of the author's architecture diagram ("The Virtuous City Vision: A Geopolitical Architecture") and given its extra detail; where the diagram and the essay conflict, the essay's wording stands. The essay (`.md`) was not changed, so it lacks the diagram's detail. No Slides artifact holds these decks yet. Once the author picks one up in the chat app, record its URL here, and from then on the artifact is upstream and `deck/` / `pitch/` are copies of it, as in the Accords repo.

## Tasks
### Updating after the deck changes
1. Replace `deck/` and `pitch/` with the new export (remove slides no longer in it), and the PDF and `.md` with their new versions.
2. Run `python3 build-slideshow.py`, then delete `preview.html` and `preview-full.html`.
3. For every removed or renamed slide id, add an entry to `SLIDE_ALIASES` in `build-slideshow.py` pointing it at the slide that now holds its content.
4. Commit, push to the working branch, and open a PR into `main` (merging it publishes the site).

### Checks
Every PR and every push to `main` runs `.github/workflows/check.yml`. Merge only when it is green.
1. Build check: `python3 build-slideshow.py` must print no warnings, and the `index.html` and `full.html` it writes must match the committed ones.
2. `tests/smoke.mjs`: opens both pages in Chromium and checks every slide link, content spilling off a slide, the Ask/PDF/feedback links, taps and keys, and that the control bar stays on one line from 1280px down to 320px.
Run it locally before pushing: `cd tests && npm ci && npx playwright install chromium && node smoke.mjs` (where Chromium is preinstalled, skip the install step). If a check fails, fix the cause; never loosen or skip a check to get green.

## Rules
- The words on the slides are the author's. Never rewrite slide text without the author's word.
- Keep the site static and self-contained. Don't add trackers, analytics or third-party scripts without asking.
- Every slide has a stable link (`index.html#<slide-id>`). Don't rename slide ids casually. When one is dropped, `SLIDE_ALIASES` redirects it; never delete an alias.
- The menu labels (`SECTION_LABEL`, `SLIDE_LABEL`), `ASK_PROMPT` and `FEEDBACK` in `build-slideshow.py` are the author's wording; change them only on the author's word. Keep the Ask buttons ordinary outbound links.
- If the build warns about an icon missing from `ICONS`, add that icon's 24px line paths to `ICONS`.
