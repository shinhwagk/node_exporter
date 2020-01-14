from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from sys import argv

from prometheus_client import generate_latest

from collector.collector import CollectorController


__version__ = '0.2.0'


class NodeExporterServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/metrics":
            print("GET request,\nPath: %s\nHeaders:\n%s\n",
                  str(self.path), str(self.headers))
            self.wfile.write(generate_latest())
        else:
            self.wfile.write("""<html>
			<head><title>Node Exporter</title></head>
			<body>
			<h1>Node Exporter</h1>
			<p><a href="/metrics">Metrics</a></p>
			</body>
			</html>""".encode('utf-8'))


def run(server_class=HTTPServer, handler_class=NodeExporterServer, port=9100):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting node_exporter port{}...\n'.format(port))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    lprint('Stopping httpd...\n')


if __name__ == '__main__':
    collectorController = CollectorController([], [])
    collectorController.initRegister()
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
