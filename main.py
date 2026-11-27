from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse
import mimetypes

HOST, PORT = "0.0.0.0", 8000
STATIC = (Path(__file__).parent / "static").resolve()


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/":
            path = "/index.html"

        file = (STATIC / path.lstrip("/")).resolve()

        if STATIC in file.parents and file.is_file():
            ctype = mimetypes.guess_type(file.name)[0] or "application/octet-stream"
            if ctype.startswith("text/"):
                ctype += "; charset=utf-8"
            data = file.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        else:
            self.send_error(404)


if __name__ == "__main__":
    print(f"Сервер запущен: http://localhost:{PORT}")
    HTTPServer((HOST, PORT), Handler).serve_forever()