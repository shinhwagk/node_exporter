class Collector(object):
    name: str

    def __init__(self, register):
        self._register = register

    def register(self):
        self._register.register(self)

    def unregister(self):
        self._register.unregister(self)
