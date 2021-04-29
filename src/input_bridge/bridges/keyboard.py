import logging

import keyboard

from input_bridge import Bridge


class KeyboardBridge(Bridge):
    def __init__(self):
        import queue
        self.event_queue = queue.Queue()

    def send_keys(self, *keys):
        for key in keys:
            logging.info(f'Pressing key {key}')
            keyboard.send(key)
