class CollectorController:
    def __init__(self, white, black):
        self.white = white
        self.black = black
        self._collectors = {}
        self.initRegister()

    def initRegister(self):
        from node_exporter.collector.diskstats import DiskstatsCollector
        from node_exporter.collector.loadavg import LoadavgCollector
        from node_exporter.collector.filesystem import FilesystemCollector
        from node_exporter.collector.stat import StatCollector
        from node_exporter.collector.meminfo import MeminfoCollector
        from node_exporter.collector.cpu import CpuCollector

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


CController = CollectorController([], [])
