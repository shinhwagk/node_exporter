from prometheus_client import Gauge

from collector.namespace import NAMESPACE
from collector.collector import Collector

# def parseStat(data):
#     return float(data.split(' ')[0])


class StatCollector(Collector):
    name = "stat"

    def __init__(self, r):
        super().__init__(r)
        self.m = Gauge('{}_boot_time_seconds'.format(
            NAMESPACE), 'Node boot time, in unixtime.')

    def collect(self):
        with open('/proc/stat', 'r') as f:
            for line in f:
                stat_name = line.split(' ')[0]
                if stat_name == 'btime':
                    stat_value = float(line.split(' ')[1])
                    self.m.set(stat_value)
