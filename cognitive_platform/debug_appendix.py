from app import app
from starlette.testclient import TestClient

c = TestClient(app)
r = c.get('/')
html = r.text

# Check if brain_image is in the rendered __D data
import re

# Extract the __D block
m = re.search(r'window\.__D=(\{.*?\});\s*\n', html, re.DOTALL)
if m:
    raw = m.group(1)
    # Check for brain_image
    imgs = re.findall(r'"brain_image":\s*"([^"]+)"', raw)
    print("brain_image values in __D:", imgs)
    print("Total glossary entries with brain_image:", len(imgs))
else:
    print("__D block not found")

# Check the appendix HTML
idx = html.find('id="app-brain-grid"')
if idx >= 0:
    print("\napp-brain-grid container found at char", idx)
    print("Context:", html[idx-20:idx+100])
else:
    print("\napp-brain-grid NOT found in HTML")

# Check the CSS for abcard__img
css = open('static/css/ahims.css', encoding='utf-8').read()
for line in css.split('\n'):
    if 'abcard' in line:
        print("CSS:", line.strip())
