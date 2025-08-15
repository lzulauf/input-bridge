import time

from input_bridge import Handler
from input_bridge.bridges.midi import MidiBridge, MidiData
from input_bridge.bridges.alsa import AlsaBridge

DEVICE_SYNCHRONIZATION_THRESHOLD = 0.4


class MidiAlsaVolumeHandler(Handler):
    def __init__(self, midi_bridge, alsa_bridge, channel, encoder, is_microphone=False):
        assert isinstance(midi_bridge, MidiBridge)
        assert isinstance(alsa_bridge, AlsaBridge)
        self.midi_bridge = midi_bridge
        self.alsa_bridge = alsa_bridge
        self.channel = channel
        self.encoder_num = encoder
        self.is_microphone = is_microphone
        self.last_device_synchronization = time.time()

        self.synchronize_midi_device()

    def synchronize_midi_device(self):
        if self.is_microphone:
            volume = self.alsa_bridge.get_microphone_volume()
            self.midi_bridge.send_midi_message(
                MidiData(channel=self.channel, data1=self.encoder_num, data2=volume)
            )
        else:
            volume = self.alsa_bridge.get_volume()
            self.midi_bridge.send_midi_message(
                MidiData(channel=self.channel, data1=self.encoder_num, data2=volume)
            )
        self.last_device_synchronization = time.time()

    def update(self):
        datas_to_keep = []
        for midi_data in self.midi_bridge.midi_datas:
            result = self.handle(midi_data)
            if result is False:
                datas_to_keep.append(midi_data)
        self.midi_bridge.midi_datas[:] = datas_to_keep

        if time.time() - self.last_device_synchronization > DEVICE_SYNCHRONIZATION_THRESHOLD:
            self.synchronize_midi_device()

    def handle(self, midi_data):
        if midi_data.channel != self.channel:
            return False

        encoder_num, value = midi_data.data1, midi_data.data2
        if encoder_num != self.encoder_num:
            return False

        if self.is_microphone:
            self.alsa_bridge.set_microphone_volume(value / 127.0)
        else:
            self.alsa_bridge.set_volume(value / 127.0)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.channel}, {self.encoder_num})'



class MidiAlsaMuteHandler(Handler):
    def __init__(self, midi_bridge, alsa_bridge, channel, encoder, is_microphone=False):
        assert isinstance(midi_bridge, MidiBridge)
        assert isinstance(alsa_bridge, AlsaBridge)
        self.midi_bridge = midi_bridge
        self.alsa_bridge = alsa_bridge
        self.channel = channel
        self.encoder_num = encoder
        self.is_microphone = is_microphone

        if self.is_microphone:
            muted = self.alsa_bridge.get_microphone_muted()
            self.midi_bridge.send_midi_message(
                MidiData(channel=self.channel, data1=self.encoder_num, data2=(127 if muted else 0))
            )
        else:
            muted = self.alsa_bridge.get_muted()
            self.midi_bridge.send_midi_message(
                MidiData(channel=self.channel, data1=self.encoder_num, data2=(127 if muted else 0))
            )

    def update(self):
        datas_to_keep = []
        for midi_data in self.midi_bridge.midi_datas:
            result = self.handle(midi_data)
            if result is False:
                datas_to_keep.append(midi_data)
        self.midi_bridge.midi_datas[:] = datas_to_keep

    def handle(self, midi_data):
        if midi_data.channel != self.channel:
            return False

        encoder_num, value = midi_data.data1, midi_data.data2
        if encoder_num != self.encoder_num:
            return False

        if self.is_microphone:
            self.alsa_bridge.set_microphone_mute(value != 0)
        else:
            self.alsa_bridge.set_mute(value != 0)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.channel}, {self.encoder_num})'



