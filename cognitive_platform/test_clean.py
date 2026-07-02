import sys
sys.path.insert(0, '.')
from fastapi.testclient import TestClient
from app import app

c = TestClient(app)
r = c.get('/')
html = r.text

print('Status:', r.status_code)
print('Size:', len(html), 'bytes')
print('Watermark divs:', html.count('class="watermark"'))
print('Section labels:', html.count('Section I'))
print('section-divider:', html.count('section-divider'))
print('sec class:', html.count('class="sec'))
print('Has perf-radar:', 'perf-radar' in html)
print('Has theme-btn:', 'theme-btn' in html)
print('Has brain-abstract:', 'brain-abstract' in html)
