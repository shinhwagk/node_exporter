from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from sys import argv
from urllib.parse import quote_plus, parse_qs, urlparse

from prometheus_client import generate_latest, start_http_server, MetricsHandler, exposition

from collector.collector import CollectorController
import time

__version__ = '0.3.0'

# collectorController = CollectorController([], [])
# collectorController.initRegister()

# start_http_server(9100)
# while True:
#     time.sleep(1)


class NodeExporterServer(MetricsHandler):
    # def do_GET(self):
    #     if self.path == "/metrics":
    #         print("GET request,\nPath: %s\nHeaders:\n%s\n",
    #               str(self.path), str(self.headers))
    #         self.wfile.write(generate_latest())
    #     else:
    #         self.wfile.write("""<html>
        # 		<head><title>Node Exporter</title></head>
        # 		<body>
        # 		<h1>Node Exporter</h1>
        # 		<p><a href="/metrics">Metrics</a></p>
        # 		</body>
        # 		</html>""".encode('utf-8'))

    def do_GET(self):
        registry = self.registry
        params = parse_qs(urlparse(self.path).query)
        encoder, content_type = exposition.choose_encoder(
            self.headers.get('Accept'))
        if 'collect[]' in params:
            names = params['collect[]']
            collectorController.collect(names)
            # registry = registry.restricted_registry(params['name[]'])
        try:
            output = encoder(registry)
        except:
            self.send_error(500, 'error generating metric output')
            raise
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.end_headers()
        self.wfile.write(output)


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
