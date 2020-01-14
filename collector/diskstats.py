import re

from prometheus_client.core import CounterMetricFamily

from collector.namespace import NAMESPACE
from collector.collector import Collector


ignored_devies = r"^(ram|loop|fd|(h|s|v|xv)d[a-z]|nvme\d+n\d+p)\d+$"
factors = [1, 1, 1, 0.001, 1, 1, 1, 0.001, 1, 0.001, 0.001]


def parseDiskStats(lines, name):
    ms = [CounterMetricFamily('{}_{}_reads_completed_total'.format(NAMESPACE, name), documentation='1m load average.', labels=['device']),
          CounterMetricFamily('{}_{}_reads_merged_total'.format(
              NAMESPACE, name), '1m load average.', labels=['device']),
          CounterMetricFamily('{}_{}_read_bytes_total'.format(
              NAMESPACE, name), '1m load average.', labels=['device']),
          CounterMetricFamily('{}_{}_read_time_seconds_total'.format(
              NAMESPACE, name), '1m load average.', labels=['device']),
          CounterMetricFamily('{}_{}_writes_completed_total'.format(
              NAMESPACE, name), '1m load average.', labels=['device']),
          CounterMetricFamily('{}_{}_writes_merged_total'.format(
              NAMESPACE, name), '1m load average.', labels=['device']),
          CounterMetricFamily('{}_{}_writes_bytes_total'.format(
              NAMESPACE, name), '1m load average.', labels=['device']),
          CounterMetricFamily('{}_{}_writes_time_seconds_total'.format(
              NAMESPACE, name), '1m load average.', labels=['device']),
          CounterMetricFamily('{}_{}_io_now'.format(
              NAMESPACE, name), '1m load average.', labels=['device']),
          CounterMetricFamily('{}_{}_io_time_seconds_total'.format(
              NAMESPACE, name), '1m load average.', labels=['device']),
          CounterMetricFamily('{}_{}_io_time_weighted_seconds_total'.format(NAMESPACE, name), '1m load average.', labels=['device'])]

    for line in lines:
        parts = re.split(r'\s+', line)
        if len(parts) >= 5:
            dev = parts[3]
            if re.match(ignored_devies, dev) is None:
                stats = parts[4:]
                for i, val in enumerate(stats):
                    if i < len(ms):
                        value = float(val) * factors[i]
                        ms[i].add_metric([dev], value)
    return ms


class DiskstatsCollector(Collector):
    name = "disk"

    def collect(self):
        with open('/proc/diskstats', 'r') as f:
            for m in parseDiskStats(f, self.name):
                yield m
