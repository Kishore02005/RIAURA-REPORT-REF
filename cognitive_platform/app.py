"""
AHIMS™ Cognitive Intelligence Platform — FastAPI Application
Interactive scroll-based microsite edition.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.base import BaseHTTPMiddleware

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from models.schema import PsychometricReport
from engine.ahims_engine import CognitiveTransformer

app = FastAPI(title="AHIMS Cognitive Intelligence", version="3.0.0")


class NoCacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        if request.url.path.startswith("/static/"):
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
        return response


app.add_middleware(NoCacheMiddleware)

app.mount("/static", StaticFiles(directory=str(PROJECT_ROOT / "static")), name="static")
templates = Jinja2Templates(directory=str(PROJECT_ROOT / "templates"))
transformer = CognitiveTransformer()


def _load_report() -> dict:
    data_path = PROJECT_ROOT / "data" / "sample_report.json"
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)


@app.get("/", response_class=HTMLResponse)
async def report_page(request: Request):
    raw = _load_report()
    report = PsychometricReport(**raw)
    ctx = transformer.process(report)
    ctx["request"] = request

    response = templates.TemplateResponse(request=request, name="ahims.html", context=ctx)
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.get("/api/report")
async def api_report():
    raw = _load_report()
    report = PsychometricReport(**raw)
    return transformer.process(report)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "ahims"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=9000, reload=True)
