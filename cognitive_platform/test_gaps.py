import sys
sys.path.insert(0, '.')
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)
r = client.get('/')
html = r.text

checks = {
    'Sticky footer HTML': 'sticky-footer' in html or 'id="sticky-footer"' in html,
    'Download button': 'btn-download' in html,
    'Share button': 'btn-share' in html,
    'Brain abstract container': 'brain-abstract' in html,
    'Domain pill cross-link JS': 'pill' in html,
    '13 sections': html.count('class="sec') >= 13,
    'Single body': html.count('<body') == 1,
}

css = open('static/css/ahims.css').read()
css_checks = {
    'prefers-reduced-motion (reveal)': 'prefers-reduced-motion' in css,
    'prefers-reduced-motion (rings)': 'ring__fill' in css and 'transition:none' in css.replace(' ',''),
    'prefers-reduced-motion (lollipop)': 'gauges__fill' in css,
    'prefers-reduced-motion (brain)': 'bcard' in css,
    'prefers-reduced-motion (persona)': 'persona__word' in css,
    'Sticky footer CSS': '.sticky' in css,
    'Pill cursor': '.pill' in css,
    'Strip node cursor': '.strip__node' in css,
    'Theme toggle CSS': '.theme-btn' in css,
    'Theme toggle HTML': 'theme-btn' in html,
    'Radar HTML': 'perf-radar' in html,
}

print('=== HTML CHECKS ===')
for name, ok in checks.items():
    print(f'  [{"PASS" if ok else "FAIL"}] {name}')

print('\n=== CSS CHECKS ===')
for name, ok in css_checks.items():
    print(f'  [{"PASS" if ok else "FAIL"}] {name}')

all_ok = all(checks.values()) and all(css_checks.values())
print(f'\n{"ALL CHECKS PASSED" if all_ok else "SOME CHECKS FAILED"}')
