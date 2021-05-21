import logging
import queue

import keyboard

from input_bridge import Bridge


class KeyboardBridge(Bridge):
    def __init__(self):
        self.events = []
        self.event_queue = queue.Queue()
        keyboard.start_recording(self.event_queue)

    def __del__(self):
        keyboard.stop_recording()

    def send_keys(self, *keys):
        for key in keys:
            logging.info(f'Pressing key {key}')
            keyboard.send(key)

    def begin_update(self):
        try:
            while True:
                self.events.append(self.event_queue.get(block=False))
                self.event_queue.task_done()
        except queue.Empty:
            pass

    def end_update(self):
        self.events = []
