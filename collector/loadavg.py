from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import re
import os

from prometheus_client import Counter, Gauge, generate_latest, Metric
from prometheus_client.core import REGISTRY

from collector.diskstats import DiskstatsCollector

from collector.namespace import NAMESPACE



class LoadavgCollector():
    def __init__(self):
        self.m = Gauge('{}_load1'.format(NAMESPACE), '1m load average.')

    def collect(self):
        with open('/proc/loadavg', 'r') as f:
            load1_val = f.readline().split(' ')[0]
        self.m.set(load1_val)
