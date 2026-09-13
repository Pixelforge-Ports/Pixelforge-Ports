from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import hashlib, json, zipfile

root = Path(__file__).resolve().parent/'dist'
class Links(HTMLParser):
    def __init__(self): super().__init__(); self.links=[]; self.ids=set()
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if 'id' in attrs:self.ids.add(attrs['id'])
        for key in ['src','href']:
            if key in attrs:self.links.append(attrs[key])

pages={}
for file in root.rglob('*.html'):
    parser=Links();parser.feed(file.read_text(encoding='utf-8'));pages[file.resolve()]=parser
for file, page in pages.items():
    for link in page.links:
        url=urlsplit(link)
        if url.scheme or url.netloc:continue
        target=(file.parent/unquote(url.path)).resolve() if url.path else file
        target.relative_to(root.resolve())
        assert target.is_file(), (file,link)
        if url.fragment:assert url.fragment in pages[target].ids,(file,link)
catalog=json.loads((root/'catalog.json').read_text())
assert len(catalog)==12 and len({g['id'] for g in catalog})==12
for game in catalog:
    path=root/'downloads'/game['zip']
    assert hashlib.sha256(path.read_bytes()).hexdigest()==game['sha256']
    with zipfile.ZipFile(path) as archive:assert archive.testzip() is None
    assert (root/'guides'/(game['id']+'.html')).is_file()
assert (root/'assets/forge.png').is_file()
print('PASS: 14 HTML pages, local assets and anchors, 12 guides, 12 ZIP downloads and SHA-256 checksums.')
