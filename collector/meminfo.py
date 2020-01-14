import re

from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily

from collector.namespace import NAMESPACE
from collector.collector import Collector


def parseMemInfo(lines):
    meminfo = {}
    for l in lines:
        parts = re.split('\s+', l)
        value = float(parts[1])
        key = parts[0][0:-1]  # remove trailing: from key
        m = re.search('\((.*)\)', key)
        if m:
            key = re.sub('\((.*)\)', m.group(1), key)
        if len(parts) >= 3:
            value *= 1024
            key = "{}_bytes".format(key)
        meminfo[key.lower()] = value
    return meminfo


class MeminfoCollector(Collector):
    name = "memory"

    def collect(self):
        with open('/proc/meminfo', 'r') as f:
            meminfo = parseMemInfo(f)
        for k, v in meminfo.items():
            if k.endswith('_total'):
                m = CounterMetricFamily("{}_{}_{}".format(
                    NAMESPACE, self.name, k), value=v, documentation="")
            else:
                m = GaugeMetricFamily("{}_{}_{}".format(
                    NAMESPACE, self.name, k), value=v, documentation="")
            yield m
