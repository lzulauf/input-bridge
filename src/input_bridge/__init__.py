import abc
import logging
import time


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
    def __init__(self, bridges=None, handlers=None, rate=None):
        self.bridges = bridges or []
        self.handlers = handlers or []
        self.rate = rate

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
                start_time = time.perf_counter()
                self.update()
                end_time = time.perf_counter()
                if self.rate is not None:
                    sleep_time = self.rate - (end_time - start_time)
                    if sleep_time > 0:
                        logging.debug(f'sleeping for {sleep_time}')
                        time.sleep(sleep_time)

        except KeyboardInterrupt:
            pass
