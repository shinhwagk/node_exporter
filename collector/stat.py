from prometheus_client.core import GaugeMetricFamily

from collector.namespace import NAMESPACE
from collector.collector import Collector


class StatCollector(Collector):
    name = "stat"

    collectors = [G]

    def __init__(self, r):
        super().__init__(r)

    def collect(self):
        with open('/proc/stat', 'r') as f:
            for line in f:
                stat_name = line.split(' ')[0]
                if stat_name == 'btime':
                    stat_value = float(line.split(' ')[1])
                    GaugeMetricFamily('{}_boot_time_seconds'.format(
                        NAMESPACE), 'Node boot time, in unixtime.',  value=stat_value))
