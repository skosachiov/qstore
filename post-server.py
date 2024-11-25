#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import json

class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):        
        self.send_response(200)
        self.end_headers()
        if '.json' not in self.path:
          self.wfile.write('json not in path'.encode())
          return
        with open(self.path[1:], "r") as f:
            data = json.load(f)
            self.wfile.write(json.dumps(data).encode())

#do if server noticed a new post / request processing

    def do_POST(self):
        content_len = int(self.headers.get('content-length', '0'))
        post_body = self.rfile.read(content_len)
        try:
          data = json.loads(post_body)
        except Exception as e:
          data = str(post_body)
        self.send_response(200)
        self.end_headers()
        with open(self.path[1:], "w") as f:
            f.write(json.dumps(data))

#start server

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8000), RequestHandler)
    print('Starting server at http://localhost:8000')
    server.serve_forever()
