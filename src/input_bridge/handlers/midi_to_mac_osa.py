import logging

from input_bridge import Handler
from input_bridge.bridges.midi import MidiBridge
from input_bridge.bridges.mac_osa import MacOSABridge


class MidiMacVolumeHandler(Handler):
    def __init__(self, midi_bridge, mac_osa_bridge, channel, encoder_num):
        assert isinstance(midi_bridge, MidiBridge)
        assert isinstance(mac_osa_bridge, MacOSABridge)
        self.midi_bridge = midi_bridge
        self.mac_osa_bridge = mac_osa_bridge
        self.channel = channel
        self.encoder_num = encoder_num

    def update(self):
        volume = None

        unused_midi_datas = []
        for midi_data in self.midi_bridge.midi_datas:
            if midi_data.channel != self.channel or midi_data.data1 != self.encoder_num:
                unused_midi_datas.append(midi_data)
                continue

            # Remap range [0, 127] to [0, 100]
            volume = midi_data.data2 * 100 // 127

        if volume is None:
            return

        # Remove volume midi datas from queue
        self.midi_bridge.midi_datas[:] = unused_midi_datas
        logging.info(f'Setting volume to {volume}')
        self.mac_osa_bridge.set_current_volume(volume)


class MidiMacMuteHandler(Handler):
    def __init__(self, midi_bridge, mac_osa_bridge, channel, encoder_num):
        assert isinstance(midi_bridge, MidiBridge)
        assert isinstance(mac_osa_bridge, MacOSABridge)
        self.midi_bridge = midi_bridge
        self.mac_osa_bridge = mac_osa_bridge
        self.channel = channel
        self.encoder_num = encoder_num
        self.last_volume = self.mac_osa_bridge.get_current_volume()

    def update(self):
        mute = None

        unused_midi_datas = []
        for midi_data in self.midi_bridge.midi_datas:
            if midi_data.channel != self.channel or midi_data.data1 != self.encoder_num:
                unused_midi_datas.append(midi_data)
                continue

            # Remap range [0, 127] to [0, 100]
            mute = midi_data.data2 == 0

        if mute is None:
            return

        current_volume = self.mac_osa_bridge.get_current_volume()
        if current_volume == 0 and mute:
            return

        if current_volume > 0 and not mute:
            return

        volume = 0 if mute else self.last_volume
        self.last_volume = self.mac_osa_bridge.get_current_volume()

        # Remove volume midi datas from queue
        self.midi_bridge.midi_datas[:] = unused_midi_datas
        logging.info('Muting' if mute else 'Unmuting')
        self.mac_osa_bridge.set_current_volume(volume)
