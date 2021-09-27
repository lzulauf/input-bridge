import logging

import pygame.midi

from input_bridge import Bridge


class MidiData:
    def __init__(self, data):
        info, self.timestamp = data
        self.channel, self.data1, self.data2, self.data3 = info

    def __repr__(self):
        return f'{self.channel}, {self.data1}, {self.data2}, {self.data3}'


class MidiBridge(Bridge):
    """
    More general replacement for MidiToKeyboard
    """
    def __init__(self, device_name):
        pygame.midi.init()
        self.midi_input = pygame.midi.Input(
                self.get_midi_device_index(device_name, requires_input=True))
        self.midi_datas = []

    def list_midi_devices(self):
        for i in range(pygame.midi.get_count()):
            yield pygame.midi.get_device_info(i)

    def get_midi_device_index(self, name, requires_input=False, requires_output=False):
        logging.debug(f'MIDI devices found: {list(self.list_midi_devices())}')
        for i, device_info in enumerate(self.list_midi_devices()):
            if device_info[1] == bytes(name, 'utf8'):
                if requires_input and not device_info[2]:
                    continue
                if requires_output and not device_info[3]:
                    continue
                logging.info(f'Using device: {device_info}')
                return i

    def begin_update(self):
        if self.midi_input.poll():
            self.midi_datas = [
                MidiData(data)
                for data in self.midi_input.read(20)
            ]

    def end_update(self):
        for midi_data in self.midi_datas:
            logging.debug(f'Unhandled midi command: {midi_data}')
        self.midi_datas = []
