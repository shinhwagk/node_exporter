from prometheus_client.core import GaugeMetricFamily

from collector.namespace import NAMESPACE
from collector.collector import Collector


def parseLoad(data):
    return float(data.split(' ')[0])


class LoadavgCollector(Collector):
    name = "loadavg"

    def collect(self):
        with open('/proc/loadavg', 'r') as f:
            load1_val = parseLoad(f.readline())
        yield GaugeMetricFamily(
            '{}_load1'.format(NAMESPACE), '1m load average.', value=float(load1_val))
