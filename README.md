# PixelForge Ports

Responsive static website for the twelve ports by Pixelforge ports (Ronax).
The authored website is in `dist/`: catalog, individual game guides, screenshots,
licensed font, and verified bring-your-own-data ZIP downloads. It works with GitHub Pages
and other static hosts without npm or a server-side application.

## Preview

From this source folder:

```powershell
python -m http.server 4173 --directory dist
```

Open http://localhost:4173.

## Refresh the catalog

Build the individual port packages first, then run:

```powershell
python build_catalog.py --sources "C:\Users\prata\Desktop\Rg34\greennow\git upload"
python validate.py
```

The generator reads each source's package metadata, package README, screenshot and
single release ZIP. It copies only the public ZIP and screenshot into the website.
It never copies game installation folders or purchased game files. Keep package
READMEs current, including controls and compatibility. Rebuild the website after
any package change so download checksums remain accurate.

Layout and color rules are in `dist/styles.css`; filtering is in `dist/catalog.js`.
Page templates are in `build_catalog.py`. No API keys or third-party analytics are required.

## Publish on GitHub Pages

1. Create a repository for this website and upload this source folder's contents.
2. In repository Settings → Pages, select **GitHub Actions** as the build source.
3. Run the included **Deploy website** workflow, or push to `main`.

The workflow publishes only `dist/`. Relative links support both a project URL
and a custom domain. Do not upload the parent game workspace.

## Attribution

Original website code: Copyright (c) 2026 Pixelforge Ports contributors, MIT.
Game artwork and names belong to Orangepixel and Cairn4. Each port archive retains
its own applicable licenses. Font licensing is in `dist/assets/FONT-LICENSE.txt`.
The forge backdrop was created for this website.

Device reports are community observations, not a promise of support for all firmware.
MewnBase 1.0.2 remains unverified. The Residual RGDS Panfrost input issue is recorded
on its guide page.

The optional WebMCP search integration is feature-detected. A supported WebMCP
browser validation context was not available during authoring; ordinary catalog
search does not depend on it.
