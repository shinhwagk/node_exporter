import re

from prometheus_client.core import CounterMetricFamily, REGISTRY

from collector.namespace import NAMESPACE

diskSubsystem = "diskstats"


class DiskstatsCollector(object):
    def __init__(self):
        self.ignored_devies = r"^(ram|loop|fd|(h|s|v|xv)d[a-z]|nvme\d+n\d+p)\d+$"
        self.factors = [1, 1, 1, 0.001, 1, 1, 1, 0.001, 1, 0.001, 0.001]

    def collect(self):
        ms = [CounterMetricFamily('{}_{}_reads_completed_total'.format(NAMESPACE, diskSubsystem), documentation='1m load average.', labels=['device']),
              CounterMetricFamily('{}_{}_reads_merged_total'.format(
                  NAMESPACE, diskSubsystem), '1m load average.', labels=['device']),
              CounterMetricFamily('{}_{}_read_bytes_total'.format(
                  NAMESPACE, diskSubsystem), '1m load average.', labels=['device']),
              CounterMetricFamily('{}_{}_read_time_seconds_total'.format(
                  NAMESPACE, diskSubsystem), '1m load average.', labels=['device']),
              CounterMetricFamily('{}_{}_writes_completed_total'.format(
                  NAMESPACE, diskSubsystem), '1m load average.', labels=['device']),
              CounterMetricFamily('{}_{}_writes_merged_total'.format(
                  NAMESPACE, diskSubsystem), '1m load average.', labels=['device']),
              CounterMetricFamily('{}_{}_writes_bytes_total'.format(
                  NAMESPACE, diskSubsystem), '1m load average.', labels=['device']),
              CounterMetricFamily('{}_{}_writes_time_seconds_total'.format(
                  NAMESPACE, diskSubsystem), '1m load average.', labels=['device']),
              CounterMetricFamily('{}_{}_io_now'.format(
                  NAMESPACE, diskSubsystem), '1m load average.', labels=['device']),
              CounterMetricFamily('{}_{}_io_time_seconds_total'.format(
                  NAMESPACE, diskSubsystem), '1m load average.', labels=['device']),
              CounterMetricFamily('{}_{}_io_time_weighted_seconds_total'.format(NAMESPACE, diskSubsystem), '1m load average.', labels=['device'])]

        with open('/proc/diskstats', 'r') as f:
            for line in f.readlines():
                parts = re.split('\s+', line)
                if len(parts) >= 5:
                    dev = parts[3]
                    if re.match(self.ignored_devies, dev) is None:
                        stats = parts[4:]
                        for i, val in enumerate(stats):
                            if i < len(ms):
                                value = float(val) * self.factors[i]
                                ms[i].add_metric([dev], value)
        for c in ms:
            yield c
