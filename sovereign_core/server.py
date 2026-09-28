"""Stdlib HTTP server for SovereignChat. No third-party deps."""
from __future__ import annotations

import json
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from .engine import SovereignChatEngine

ROOT = Path(__file__).resolve().parent.parent
WEB = ROOT / "web"
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)

SESSIONS: dict[str, SovereignChatEngine] = {}


def _engine(sid: str) -> SovereignChatEngine:
    if sid not in SESSIONS:
        SESSIONS[sid] = SovereignChatEngine()
    return SESSIONS[sid]


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB), **kwargs)

    def log_message(self, fmt, *args):
        print(f"[sovereign] {self.address_string()} {fmt % args}")

    def _json(self, code: int, payload: dict):
        raw = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(raw)

    def _read_json(self) -> dict:
        n = int(self.headers.get("Content-Length") or 0)
        if n <= 0:
            return {}
        raw = self.rfile.read(n)
        try:
            return json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            return {}

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        path = urlparse(self.path).path
        body = self._read_json()
        sid = str(body.get("session") or "default")[:64]

        if path == "/api/chat":
            text = str(body.get("text") or "").strip()
            if not text:
                return self._json(400, {"error": "text required"})
            result = _engine(sid).chat(text)
            self._persist(sid)
            return self._json(200, result)

        if path == "/api/reset":
            _engine(sid).reset()
            self._persist(sid)
            return self._json(200, {"ok": True, "session": sid})

        if path == "/api/lead":
            lead = {
                "name": str(body.get("name") or "").strip()[:120],
                "email": str(body.get("email") or "").strip()[:180],
                "trade": str(body.get("trade") or "").strip()[:80],
                "note": str(body.get("note") or "").strip()[:500],
            }
            if not lead["email"] or "@" not in lead["email"]:
                return self._json(400, {"error": "valid email required"})
            path_out = DATA / "leads.jsonl"
            with path_out.open("a", encoding="utf-8") as f:
                f.write(json.dumps(lead) + "\n")
            return self._json(200, {
                "ok": True,
                "checkout": "https://buy.stripe.com/dRm8wPbb72pY2Mz8BR43S1D",
                "storefront": "https://garrettc123.github.io/",
            })

        return self._json(404, {"error": "not found"})

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/health":
            return self._json(200, {"ok": True, "product": "SovereignChat", "sessions": len(SESSIONS)})
        if path in ("/", ""):
            self.path = "/index.html"
        return super().do_GET()

    def _persist(self, sid: str):
        eng = SESSIONS[sid]
        payload = {
            "mode": eng.mode,
            "memories": eng.memories,
            "turns": len(eng.history),
        }
        (DATA / f"session-{sid}.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")


def serve(host: str = "0.0.0.0", port: int = 8787):
    httpd = ThreadingHTTPServer((host, port), Handler)
    print(f"SovereignChat live  http://127.0.0.1:{port}")
    print(f"Chat                http://127.0.0.1:{port}/index.html")
    print(f"Offer               http://127.0.0.1:{port}/sell.html")
    httpd.serve_forever()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8787"))
    serve(port=port)
