# import logging

from prometheus_client.core import REGISTRY


class Collector(object):
    name: str

    isRegister: bool = False

    def collect(self):
        pass

    def register(self):
        if not self.isRegister:
            REGISTRY.register(self)
            self.isRegister = True

    def unregister(self):
        print(self.__str__)
        if self.isRegister:
            REGISTRY.unregister(self)
            self.isRegister = False


class CollectorController:
    def __init__(self, white, black):
        self.white = white
        self.black = black
        self._collectors = {}

    def initRegister(self):
        from collector.diskstats import DiskstatsCollector
        from collector.loadavg import LoadavgCollector
        from collector.filesystem import FilesystemCollector
        from collector.stat import StatCollector
        from collector.meminfo import MeminfoCollector
        from collector.cpu import CpuCollector

        ALLCOLLECTORS = [
            DiskstatsCollector,
            LoadavgCollector,
            FilesystemCollector,
            StatCollector,
            MeminfoCollector,
            CpuCollector
        ]

        print('Enabled collectors:')
        for c in ALLCOLLECTORS:
            self._collectors[c.name] = c()
            self._collectors[c.name].register()
            print("  - {} ".format(c.name))

    def collect(self, names=[]):
        if len(names) == 0:
            for k, v in self._collectors.items():
                v.register()
        for name in names:
            self._collectors[name].register()
        for name in self._collectors.keys():
            if name not in names:
                self._collectors[name].unregister()
