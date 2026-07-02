from app import app
from starlette.testclient import TestClient
c = TestClient(app)
r = c.get('/')
html = r.text

ids = ['explorer-cards','brain-main','func-grid','interp-cards','dev-roadmap','dev-focus','labs-flow','app-brain-grid','app-glossary','app-colors','cover-ring','perf-radar','domain-bars','arch-sankey','persona','sticky-footer','btn-download']
for i in ids:
    found = ('id="'+i+'"') in html
    print(f"{i}: {'YES' if found else 'NO'}")

# Check CSS sections exist
css = open('static/css/ahims.css', encoding='utf-8').read()
sections = ['COVER','OVERVIEW','EXECUTIVE','PERFORMANCE','DOMAIN CARDS','BRAIN','ARCHITECTURE','FUNCTIONAL','INTERPERSONAL','PERSONA','DEVELOPMENT','LABS','APPENDIX','STICKY']
for s in sections:
    found = s in css
    print(f"CSS {s}: {'YES' if found else 'NO'}")
