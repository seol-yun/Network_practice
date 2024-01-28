import os
import http
import http.server
import socketserver
import sqlite3


PREFIX = ''

FLAGS = _ = None
DEBUG = False

EXT = {'.html': 'text/html;charset=utf-8',
       '.js': 'text/javascript;charset=utf-8'}

CONN = sqlite3.connect('./Log.db')
CUR = CONN.cursor()
CUR.execute('''CREATE TABLE IF NOT EXISTS Log (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 ip TEXT,
                 request TEXT);''')
CONN.commit()


class MyHTTPDaemon(http.server.HTTPServer):
    allow_reuse_address = True


class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.rootdir = FLAGS.rootdir
        self.conn = CONN
        self.cur = CUR
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if DEBUG:
            print(f'Command: {self.command}')
            print(f'Path: {self.path}')
            print(f'Headers: {self.headers}')

        self.cur.execute('''INSERT INTO Log (ip, request)
                            VALUES (?, ?);''', (self.client_address[0], self.requestline))
        self.conn.commit()

        if not self.path.startswith(PREFIX):
            return None
        self.path = self.path[len(PREFIX):]
        if self.path == '/':
            path = 'index.html'
        else:
            path = self.path[1:]
        path = os.path.join(self.rootdir, path)
        if DEBUG:
            print(f'Joined path: {self.rootdir} {self.path} {path}')
        if not os.path.exists(path):
            self.send_error(http.HTTPStatus.NOT_FOUND, 'File not found')
        else:
            ext = os.path.splitext(path)[-1].lower()
            self.send_response(http.HTTPStatus.OK)
            self.send_header('Content-Type', EXT[ext])
            with open(path, 'rb') as f:
                self.cur.execute('''SELECT MAX(id) FROM Log;''')
                counter = self.cur.fetchone()[0]
                body = f.read()
                body = body.replace('{{ COUNTER }}'.encode('utf-8'), f'{counter}'.encode('utf-8'))
                self.send_header('Content-Length', len(body))
                self.end_headers()
                self.wfile.write(body)

def main():
    print(f'Parsed arguments: {FLAGS}')
    print(f'Unparsed arguments: {_}')

    with MyHTTPDaemon((FLAGS.host, FLAGS.port), 
                      MyHTTPRequestHandler) as httpd:
        try:
            print(f'Start server {httpd.server_address}')
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f'Stop server {httpd.server_address}')
            httpd.shutdown()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='Debug message')
    parser.add_argument('--host', default='0.0.0.0', type=str,
                        help='IP address')
    parser.add_argument('--port', default=8888, type=int,
                        help='Port number')
    parser.add_argument('--rootdir', default='./dir', type=str,
                        help='Root directory')

    FLAGS, _ = parser.parse_known_args()
    DEBUG = FLAGS.debug

    main()

