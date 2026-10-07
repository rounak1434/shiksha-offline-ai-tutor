"""
backend/service.py
Lightweight Local HTTP & SSE Service for SHIKSHA Offline AI Tutor.
Exposes REST and Server-Sent Events (SSE) endpoints over localhost:8080.
Guaranteed 100% OFFLINE operation: zero external cloud dependencies.
"""

import os
import sys
import json
import uuid
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from backend.inference_engine import ShikshaInferenceEngine

HOST = "127.0.0.1"
PORT = 8080

engine = ShikshaInferenceEngine()

class ShikshaRequestHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == "/health" or path == "/info":
            info = engine.get_model_info()
            self._send_json(200, info)
        else:
            self._send_json(404, {"error": "Not Found", "path": path})

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        # Read request body
        content_length = int(self.headers.get("Content-Length", 0))
        body = {}
        if content_length > 0:
            raw_body = self.rfile.read(content_length).decode("utf-8")
            try:
                body = json.loads(raw_body)
            except Exception:
                self._send_json(400, {"error": "Invalid JSON payload"})
                return

        if path == "/load":
            model_path = body.get("model_path")
            ctx_size = body.get("ctx_size", 2048)
            n_threads = body.get("n_threads", 4)
            try:
                res = engine.load_model(model_path, ctx_size, n_threads)
                self._send_json(200, res)
            except Exception as e:
                self._send_json(400, {"error": str(e)})

        elif path == "/unload":
            res = engine.unload_model()
            self._send_json(200, res)

        elif path == "/cancel":
            req_id = body.get("request_id")
            if not req_id:
                self._send_json(400, {"error": "request_id is required"})
                return
            success = engine.stop_generation(req_id)
            self._send_json(200, {"request_id": req_id, "cancelled": success})

        elif path == "/benchmark":
            runs = body.get("num_runs", 2)
            try:
                res = engine.benchmark(runs)
                self._send_json(200, res)
            except Exception as e:
                self._send_json(500, {"error": str(e)})

        elif path == "/generate":
            question = body.get("prompt") or body.get("question")
            if not question:
                self._send_json(400, {"error": "prompt/question field is required"})
                return
                
            grade = body.get("grade")
            subject = body.get("subject")
            req_id = body.get("request_id") or str(uuid.uuid4())
            max_tokens = body.get("max_tokens", 250)
            temp = body.get("temperature", 0.0)
            
            try:
                resp = engine.generate(
                    question=question,
                    grade=grade,
                    subject=subject,
                    request_id=req_id,
                    max_tokens=max_tokens,
                    temperature=temp
                )
                self._send_json(200, resp.to_dict())
            except Exception as e:
                self._send_json(500, {"error": str(e)})

        elif path == "/generate/stream":
            question = body.get("prompt") or body.get("question")
            if not question:
                self._send_json(400, {"error": "prompt/question field is required"})
                return
                
            grade = body.get("grade")
            subject = body.get("subject")
            req_id = body.get("request_id") or str(uuid.uuid4())
            max_tokens = body.get("max_tokens", 250)
            temp = body.get("temperature", 0.0)

            # Initiate Server-Sent Events (SSE)
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream; charset=utf-8")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            try:
                for chunk in engine.stream_generate(
                    question=question,
                    grade=grade,
                    subject=subject,
                    request_id=req_id,
                    max_tokens=max_tokens,
                    temperature=temp
                ):
                    event_payload = json.dumps(chunk.to_dict(), ensure_ascii=False)
                    sse_message = f"data: {event_payload}\n\n"
                    self.wfile.write(sse_message.encode("utf-8"))
                    self.wfile.flush()
            except Exception as e:
                err_payload = json.dumps({"request_id": req_id, "error": str(e), "done": True})
                self.wfile.write(f"data: {err_payload}\n\n".encode("utf-8"))
                self.wfile.flush()

        else:
            self._send_json(404, {"error": "Not Found", "path": path})

def run_server(port: int = PORT):
    server = HTTPServer((HOST, port), ShikshaRequestHandler)
    print(f"🚀 SHIKSHA Offline AI Tutor Service running on http://{HOST}:{port}")
    print("🔒 Mode: 100% OFFLINE (Local inference via llama.cpp)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.server_close()

if __name__ == "__main__":
    p = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    run_server(p)
