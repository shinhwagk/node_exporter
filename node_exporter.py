from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import re
import os

from prometheus_client import Counter, Gauge, generate_latest
from prometheus_client.core import REGISTRY

from collector.diskstats import DiskstatsCollector
from collector.loadavg import LoadavgCollector


REGISTRY.register(DiskstatsCollector())
ms = [LoadavgCollector()]


class NodeExporterServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/metrics":
            logging.info("GET request,\nPath: %s\nHeaders:\n%s\n",
                         str(self.path), str(self.headers))
            for m in ms:
                m.collect()
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
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting node_exporter port{}...\n'.format(port))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
