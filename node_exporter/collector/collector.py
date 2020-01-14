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
        if self.isRegister:
            REGISTRY.unregister(self)
            self.isRegister = False
