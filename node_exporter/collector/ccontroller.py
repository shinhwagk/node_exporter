class CollectorController:
    def __init__(self, white, black):
        self.white = white
        self.black = black
        self._collectors = {}
        self.initRegister()

    def initRegister(self):
        from .diskstats import DiskstatsCollector
        from .loadavg import LoadavgCollector
        from .filesystem import FilesystemCollector
        from .stat import StatCollector
        from .meminfo import MeminfoCollector
        from .cpu import CpuCollector

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
