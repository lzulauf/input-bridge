import logging
import time

import pygame.midi

from input_bridge import Bridge
from input_bridge.exceptions import ConfigurationRuntimeError


logger = logging.getLogger('input_bridge.bridges.midi')


class MidiData:
    def __init__(self, channel, data1=0, data2=0, data3=0, timestamp=0):
        self.channel = channel
        self.data1 = data1
        self.data2 = data2
        self.data3 = data3
        self.timestamp = timestamp

    @staticmethod
    def from_data(data):
        info, timestamp = data
        channel, data1, data2, data3 = info
        return MidiData(channel=channel, data1=data1, data2=data2, data3=data3, timestamp=timestamp)

        info, self.timestamp = data

    def to_data(self):
        """return a list suitable for sending to a device."""
        return [[self.channel, self.data1, self.data2, self.data3], self.timestamp]

    def __repr__(self):
        return f'{self.channel}, {self.data1}, {self.data2}, {self.data3}'


class MidiBridge(Bridge):
    """
    More general replacement for MidiToKeyboard
    """
    def __init__(self, device_name):
        pygame.midi.init()
        # Create one just to close it first.
        self.midi_input = pygame.midi.Input(
                self.get_midi_device_index(device_name, requires_input=True))
        self.midi_output = pygame.midi.Output(
                self.get_midi_device_index(device_name, requires_output=True))
        self.midi_datas = []

        # Ugly hack - there is a slight delay between creating the input and when data can be read.
        time.sleep(0.01)
        # Clear out any old messages in the pipe
        while True:
            if not self.midi_input.read(20):
                break

    def send_midi_message(self, midi_data):
        data = midi_data.to_data()
        self.midi_output.write([data])

    @staticmethod
    def list_midi_devices():
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
        raise ConfigurationRuntimeError(f'Could not find device "{name}"')

    def begin_update(self):
        if self.midi_input.poll():
            self.midi_datas = [
                MidiData.from_data(data)
                for data in self.midi_input.read(20)
            ]
        logging.debug(repr(self.midi_datas))

    def end_update(self):
        for midi_data in self.midi_datas:
            logging.debug(f'Unhandled midi command: {midi_data}')
        self.midi_datas = []
