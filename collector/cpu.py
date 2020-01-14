from re import match, search

from prometheus_client.core import CounterMetricFamily

from collector.namespace import NAMESPACE
from collector.collector import Collector


class CpuCollector(Collector):
    name = "cpu"

    def metric(self, value, cpuid, mode):
        m = CounterMetricFamily('{}_{}_seconds_total'.format(
            NAMESPACE, self.name), 'Seconds the cpus spent in each mode.',  labels=["cpu", "mode"])

        m.add_metric(labels=[cpuid, mode], value=value)
        return m

    def collect(self):
        with open('/proc/stat', 'r') as f:
            for line in f:
                s = search(
                    r'^cpu([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+', line)
                if s:
                    cpuid, user, nice, system, idle, iowait, irq, softirq, steal = s.group(1), s.group(2),  s.group(3), s.group(4), s.group(
                        5), s.group(6), s.group(7), s.group(8), s.group(9)
                    yield self.metric(float(user), cpuid, "user")
                    yield self.metric(float(nice), cpuid, "nice")
                    yield self.metric(float(system), cpuid, "system")
                    yield self.metric(float(idle), cpuid, "idle")
                    yield self.metric(float(iowait), cpuid, "iowait")
                    yield self.metric(float(irq), cpuid, "irq")
                    yield self.metric(float(softirq), cpuid, "softirq")
                    yield self.metric(float(steal), cpuid, "steal")
