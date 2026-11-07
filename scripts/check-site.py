"""Verify both built editions and every local HTML asset/link."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1] / '_site'

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        self.links.extend(v for k, v in attrs if k in ('href', 'src') and v)

errors = []
for page in ROOT.rglob('*.html'):
    parser = Links()
    parser.feed(page.read_text())
    for link in parser.links:
        url = urlsplit(link)
        if url.scheme or url.netloc or not url.path:
            continue
        target = ROOT / unquote(url.path).lstrip('/') if url.path.startswith('/') else page.parent / unquote(url.path)
        if not target.exists():
            errors.append(f'{page.relative_to(ROOT)}: {link}')
for lang in ('en', 'zh'):
    feeds = [p for p in (ROOT / lang).rglob('*.xml') if ET.parse(p).getroot().tag == 'rss']
    if len(feeds) != 3 or not (ROOT / lang / 'search.json').exists():
        errors.append(f'{lang}: missing RSS feeds or search index')
if errors:
    raise SystemExit('\n'.join(errors))
print('PASS: internal page/asset links, 6 RSS feeds, and both search indexes.')
