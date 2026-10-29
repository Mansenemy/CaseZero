"""
CaseZero HTTP Server and JSON API.
Built entirely using Python's standard library (http.server, json, mimetypes).
No external pip dependencies required.
"""

import os
import sys
import json
import mimetypes
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from game.state import GameSession
from game.cases import CASES

BASE_DIR = Path(__file__).resolve().parent
WEB_DIR = BASE_DIR / "web"

# Initialize global game session
SESSION = GameSession()
SESSION.start_case("case_1")

class CaseZeroHandler(SimpleHTTPRequestHandler):
    """
    HTTP handler serving static web assets and RESTful JSON API endpoints.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)

    def do_GET(self):
        url = self.path.split("?")[0]

        if url.startswith("/api/"):
            self.handle_api_get(url)
        else:
            # Fallback to index.html for root
            if url == "/" or url == "":
                self.path = "/index.html"
            super().do_GET()

    def do_POST(self):
        url = self.path.split("?")[0]
        if url.startswith("/api/"):
            content_length = int(self.headers.get("Content-Length", 0))
            body_bytes = self.rfile.read(content_length) if content_length > 0 else b"{}"
            try:
                data = json.loads(body_bytes.decode("utf-8")) if body_bytes else {}
            except Exception:
                data = {}
            self.handle_api_post(url, data)
        else:
            self.send_error(404, "Endpoint not found")

    def handle_api_get(self, url: str):
        if url == "/api/cases":
            cases_list = [
                {
                    "id": "case_1",
                    "title": CASES["case_1"]["title"],
                    "location": CASES["case_1"]["location"],
                    "difficulty": CASES["case_1"]["difficulty"],
                    "suspect_count": len(CASES["case_1"]["suspects"]),
                    "briefing": CASES["case_1"]["briefing"],
                    "image": CASES["case_1"]["scene_image"]
                },
                {
                    "id": "case_2",
                    "title": CASES["case_2"]["title"],
                    "location": CASES["case_2"]["location"],
                    "difficulty": CASES["case_2"]["difficulty"],
                    "suspect_count": len(CASES["case_2"]["suspects"]),
                    "briefing": CASES["case_2"]["briefing"],
                    "image": CASES["case_2"]["scene_image"]
                },
                {
                    "id": "procedural",
                    "title": "Operation Chimera",
                    "location": "Black-Site Nexus Research Facility",
                    "difficulty": "Procedural",
                    "suspect_count": 6,
                    "briefing": "Procedurally generated case with randomized graph, trait matrix and planted lie.",
                    "image": "assets/img/scenes/vault_scene.svg"
                }
            ]
            self.send_json(cases_list)

        elif url == "/api/session/state":
            self.send_json(SESSION.to_dict())

        elif url == "/api/dsa/stats":
            tab = self.path.split("tab=")[-1].split("&")[0] if "tab=" in self.path else "suspects"
            suspect_id = self.path.split("suspect_id=")[-1].split("&")[0] if "suspect_id=" in self.path else None
            hood = SESSION.get_under_the_hood(tab, suspect_id)
            self.send_json(hood)

        else:
            self.send_error(404, "API endpoint not found")

    def handle_api_post(self, url: str, data: dict):
        if url == "/api/session/start":
            case_id = data.get("case_id", "case_1")
            seed = data.get("seed")
            state = SESSION.start_case(case_id, seed)
            self.send_json(state)

        elif url == "/api/lead/explore":
            lead_id = data.get("lead_id", "")
            res = SESSION.explore_lead(lead_id)
            self.send_json(res)

        elif url == "/api/clue/debunk":
            clue_id = data.get("clue_id", "")
            res = SESSION.debunk_clue(clue_id)
            self.send_json(res)

        elif url == "/api/graph/path":
            start = data.get("start", "")
            target = data.get("target", "")
            res = SESSION.query_path(start, target)
            self.send_json(res)

        elif url == "/api/alibi/check":
            suspect_id = data.get("suspect_id", "")
            time_target = data.get("time", "23:45")
            res = SESSION.check_alibi(suspect_id, time_target)
            self.send_json(res)

        elif url == "/api/suspect/toggle":
            suspect_id = data.get("suspect_id", "")
            res = SESSION.toggle_suspect(suspect_id)
            self.send_json(res)

        elif url == "/api/search":
            query = data.get("query", "")
            matches = SESSION.trie.autocomplete(query)
            self.send_json({"matches": matches})

        elif url == "/api/hint":
            res = SESSION.get_hint()
            self.send_json(res)

        elif url == "/api/accuse":
            culprit = data.get("culprit", "")
            accomplice = data.get("accomplice", "")
            res = SESSION.submit_accusal(culprit, accomplice)
            self.send_json(res)

        else:
            self.send_error(404, "API endpoint not found")

    def send_json(self, payload: any, status: int = 200):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        # Quiet logger to keep terminal clean
        pass


def run_server(port: int = 8000) -> tuple[ThreadingHTTPServer, int]:
    """Starts HTTP server on port with fallback."""
    for p in [port, 8001, 8080, 8888]:
        try:
            server = ThreadingHTTPServer(("127.0.0.1", p), CaseZeroHandler)
            return server, p
        except OSError:
            continue
    raise RuntimeError("Could not bind to any available port.")

if __name__ == "__main__":
    server, port = run_server(8000)
    print(f"CaseZero Server listening on http://127.0.0.1:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
