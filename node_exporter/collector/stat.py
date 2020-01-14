from prometheus_client.core import GaugeMetricFamily

from .namespace import NAMESPACE
from .collector import Collector


class StatCollector(Collector):
    name = "stat"

    def collect(self):
        with open('/proc/stat', 'r') as f:
            for line in f:
                stat_name = line.split(' ')[0]
                if stat_name == 'btime':
                    stat_value = float(line.split(' ')[1])
                    yield GaugeMetricFamily('{}_boot_time_seconds'.format(
                        NAMESPACE), documentation='',  value=stat_value)
