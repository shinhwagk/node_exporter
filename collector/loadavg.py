from prometheus_client import Gauge

from collector.namespace import NAMESPACE

def parseLoad(data):
    return float(data.split(' ')[0])

class LoadavgCollector():
    def __init__(self):
        self.m = Gauge('{}_load1'.format(NAMESPACE), '1m load average.')

    def collect(self):
        with open('/proc/loadavg', 'r') as f:
            load1_val = parseLoad(f.readline())
        self.m.set(float(load1_val))
