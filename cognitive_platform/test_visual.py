import sys
sys.path.insert(0, '.')
from fastapi.testclient import TestClient
from app import app

c = TestClient(app)
r = c.get('/')
html = r.text

css = open('static/css/ahims.css').read()

print('Status:', r.status_code)
print('Size:', len(html), 'bytes')
print('Sections:', html.count('class="sec'))
print('Has perf-radar:', 'perf-radar' in html)
print('Has brain-abstract:', 'brain-abstract' in html)
print('Has theme-btn:', 'theme-btn' in html)
print('Has cover-ring:', 'cover-ring' in html)
print('Has explorer-cards:', 'explorer-cards' in html)
print('Has brain-main:', 'brain-main' in html)
print('Has arch-flow:', 'arch-flow' in html)
print('Has func-grid:', 'func-grid' in html)
print('Has interp-cards:', 'interp-cards' in html)
print('Has dev-matrix:', 'dev-matrix' in html)
print('Has labs-flow:', 'labs-flow' in html)
print('CSS has theme toggle:', '.theme-btn' in css)
print('CSS has light theme:', '[data-theme="light"]' in css)
print('CSS has score ring:', '.ring' in css)
