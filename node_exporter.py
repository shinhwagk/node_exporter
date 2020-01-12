from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import os

from prometheus_client import generate_latest
from prometheus_client.core import REGISTRY, GaugeMetricFamily

from collector.diskstats import DiskstatsCollector
from collector.loadavg import LoadavgCollector
from collector.filesystem import FilesystemCollector
from collector.stat import StatCollector
from collector.collector import Collector


__version = '0.1.0'


for i in[LoadavgCollector]:
    if i.name == 'loadavg':
        i(REGISTRY).register()


# collectors = [LoadavgCollector(REGISTRY)]


class NodeExporterServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/metrics":
            logging.info("GET request,\nPath: %s\nHeaders:\n%s\n",
                         str(self.path), str(self.headers))
            # for m in ms:
            #     m.collect()
            # lc.collect()
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
