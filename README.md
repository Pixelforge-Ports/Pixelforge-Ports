# PixelForge Ports

The website discovers public ports from https://github.com/Pixelforge-Ports.
Metadata, guides and screenshots come from GitHub. Downloads link directly to
GitHub release assets; no local port installations or ZIP copies are required.

## Enable automatic updates

1. Create a website repository in Pixelforge-Ports. Use `Pixelforge-Ports.github.io`
   for the organization homepage, or another name for a project website.
2. Upload this website source, including `.github/workflows/pages.yml` and `dist/`.
3. In Settings -> Pages, choose **GitHub Actions** as the build source.
4. In Actions -> Deploy website, choose **Run workflow** for the first deployment.

The workflow discovers repositories, rebuilds the website, validates it and deploys
GitHub Pages. It runs on website pushes to `main`, manually, and **hourly at minute
17 UTC**. GitHub schedules can run late; updates are not guaranteed to be immediate.
Schedules run from the default branch. GitHub may disable scheduled workflows in
public repositories after 60 days without activity; re-enable the workflow if needed.

The private Sites preview is a build snapshot. This hourly workflow updates the
GitHub Pages website once installed in your website repository; it does not
schedule automatic publication of the private Sites preview.

## Publish a game update

Update its metadata and guide before tagging a release. Publish a GitHub release
in the game's repository and attach the universal BYO ZIP. The filename must match
`package/port.json`'s `name`, ignoring capitalization, for example `Residual.zip`.

The next website run chooses the newest published release with a matching uploaded
ZIP. Prereleases are included and labeled **Testing release**. Drafts are excluded.
Ports without matching release assets appear as **Awaiting release**, with their
repository link and no download button. Uploading a ZIP later makes it discoverable
on the next run. A newer release without its ZIP does not replace an older download.

A downloadable release's guide, screenshot and metadata come from its release tag,
so they match the selected package. Keep those files at the tag. Unreleased ports
use the default branch. Checksums are displayed only when GitHub supplies an asset
SHA-256 digest; the website does not verify release ZIP contents itself.

## Add a new port

Create a public, non-archived repository in Pixelforge-Ports with:

```text
package/
  port.json
  README.md
  screenshot.png
```

Follow the existing port metadata format: unique lowercase `.zip` name, title,
description, genres and store links. The site skips repositories without
`package/port.json`, including the website repository. More than 100 repositories
are supported through pagination. Publish a matching release ZIP when ready.
No hardcoded game list or local source path needs updating.

## Refresh immediately

Run Actions -> Deploy website -> Run workflow in the website repository.
The workflow also accepts `repository_dispatch` with event type `port-updated`
for a future webhook integration. Cross-repository dispatch requires a GitHub App
or a suitable token authorized for the website repository. The ordinary token
from another game's repository is not sufficient by default. Hourly discovery
requires no custom secret and no workflow in each port repository.

## Local build and preview

```powershell
python build_catalog.py
python validate.py
python -m unittest discover -s tests
python -m http.server 4173 --directory dist
```

Open http://localhost:4173. Python 3.9+ and internet access are required for refresh.
Optionally supply `GITHUB_TOKEN` through your environment for a higher API limit.
Actions uses its built-in token only during build. Tokens are never embedded in the
website, and visitors do not make GitHub API requests.

If GitHub is unavailable or metadata is malformed, the workflow fails before
publication and the previously deployed site stays online. Inspect the Actions
log, correct the issue and rerun. A partial catalog is not automatically published.

Templates: `build_catalog.py`. GitHub discovery: `github_catalog.py`. Styling:
`dist/styles.css`. Search: `dist/catalog.js`. Authored assets stay in `dist/assets/`.
Guides, catalog data and game screenshots are generated; downloads remain on GitHub.

Original website code: Copyright (c) 2026 Pixelforge Ports contributors, MIT.
Game names and artwork retain their creators' rights. Each port retains its licenses.
Font licensing is in `dist/assets/FONT-LICENSE.txt`.

The optional WebMCP search API is feature-detected. A supported WebMCP validation
context was unavailable; ordinary catalog search does not depend on it.

## Connect and Support cards

Edit `support-links.json` to set the Discord invitation, Source repository,
Sponsors and Ko-fi URLs. Use complete HTTPS links. Empty URLs display a visibly
unavailable card instead of sending visitors to an invented destination.
The shared section is rendered before the footer on every page and is preserved
by automatic catalog rebuilds.
