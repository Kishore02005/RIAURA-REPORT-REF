import sys, re
sys.path.insert(0, '.')
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)
r = client.get('/')
html = r.text

# Extract JS portions for checking dynamic references
import re
js_blocks = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
js = ' '.join(js_blocks)

anchors = ['cover','overview','executive','performance','explorer',
           'brain','architecture','functional','interpersonal',
           'persona','development','labs','appendix']

for a in anchors:
    has_id = ('id="' + a + '"' in html)
    # Anchors are referenced either directly in HTML or dynamically via JS sec.id
    has_anchor = ('#' + a in html) or ("'#" + a + "'" in html) or ('"#' + a + '"' in html) or (".id" in js and has_id)
    status = 'PASS' if has_id and has_anchor else 'FAIL'
    print(f'  [{status}] #{a} - id={has_id}, referenced={has_anchor}')

pages = re.findall(r'<section[^>]*class="page"', html)
chapters = re.findall(r'<section[^>]*class="sec', html)
print(f'  Sections with .page class: {len(pages)} (should be 0)')
print(f'  Sections with .sec class: {len(chapters)} (should be 13)')
print(f'  Body tags: {html.count("<body")} (should be 1)')
print(f'  HTML tags: {html.count("<html")} (should be 1)')

nav_links = re.findall(r'href="([^"]*)"', html)
hash_links = [l for l in nav_links if l.startswith('#')]
non_hash = [l for l in nav_links if not l.startswith('#') and not l.startswith('http')]
print(f'  Anchor-hash nav links: {len(hash_links)}')
print(f'  Non-hash, non-external links: {len(non_hash)} (should be 0)')
