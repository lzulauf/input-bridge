import abc


__all__ = [
    'Bridge',
    'Handler',
    'Manager',
]


class Bridge:
    def begin_update(self):
        pass

    def end_update(self):
        pass


class Handler(abc.ABC):
    @abc.abstractmethod
    def update(self):
        pass


class Manager:
    def __init__(self, bridges=None, handlers=None):
        self.bridges = bridges or []
        self.handlers = handlers or []

    def add_bridge(self, bridge):
        self.bridges.append(bridge)

    def add_handler(self, handler):
        self.handlers.append(handler)

    def update(self):
        for bridge in self.bridges:
            bridge.begin_update()

        for handler in self.handlers:
            handler.update()

        for bridge in self.bridges:
            bridge.end_update()

    def run(self):
        try:
            while True:
                self.update()
        except KeyboardInterrupt:
            pass
