#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl, urllib.parse, json
import uuid, time

class PaddleApiServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write('This is an activation server for GPGMail.'.encode())

    def do_POST(self):
        body = self.rfile.read(int(self.headers['Content-Length'], 0)).decode()
        self.send_response(200)
        self.end_headers()

        print('Receive a POST request from %s:%d -->' % self.client_address)
        request_info = urllib.parse.parse_qs(body)
        for key in request_info.keys():
            print('%-32s =' % key, request_info[key])
        print()

        response_info = {}
        response_info['success'] = 1
        response_info['response'] = {}
        response_info['response']['product_id'] = request_info['product_id'][0]
        response_info['response']['activation_id'] = str(uuid.uuid4())      # it can be anything
        response_info['response']['expires'] = 0                            # if set by 1, 'expiry_date' field is required.
                                                                            # Otherwise, license never expires.
        # response_info['response']['expiry_date'] = time.time() + 24 * 60 * 60 * 365       # expires after a year
        response_info['response']['type'] = 'activation_license'            # it also can be 'feature_license'. Not tested
        self.wfile.write(json.dumps(response_info).encode())

IP = '127.0.0.1'
Port = 443

httpd = HTTPServer((IP, Port), PaddleApiServerHandler)
httpd.socket = ssl.wrap_socket(httpd.socket, 
                               keyfile = 'cert-key.pem', 
                               certfile = 'cert-crt.pem', 
                               server_side = True)
httpd.serve_forever()

