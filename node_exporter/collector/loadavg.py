from prometheus_client.core import GaugeMetricFamily

from .namespace import NAMESPACE
from .collector import Collector


def parseLoad(data):
    return float(data.split(' ')[0])


class LoadavgCollector(Collector):
    name = "loadavg"

    def collect(self):
        with open('/proc/loadavg', 'r') as f:
            load1_val = parseLoad(f.readline())
        yield GaugeMetricFamily(
            '{}_load1'.format(NAMESPACE), documentation='', value=float(load1_val))
