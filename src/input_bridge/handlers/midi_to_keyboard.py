from input_bridge import Handler
from input_bridge.bridges.midi import MidiBridge
from input_bridge.bridges.keyboard import KeyboardBridge


class MidiKeyboardHandler(Handler):
    def __init__(self, midi_bridge, keyboard_bridge, channel, encoder_num, *keys):
        assert isinstance(midi_bridge, MidiBridge)
        assert isinstance(keyboard_bridge, KeyboardBridge)
        self.midi_bridge = midi_bridge
        self.keyboard_bridge = keyboard_bridge
        self.channel = channel
        self.encoder_num = encoder_num
        self.keys = keys

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

        encoder_num, _ = midi_data.data1, midi_data.data2
        if encoder_num != self.encoder_num:
            return False

        self.keyboard_bridge.send_keys(*self.keys)

        return True

    def __repr__(self):
        return f'{self.__class__.__name__}({self.channel}, {self.encoder_num}, {self.keys})'


class MidiAbletonHandler(Handler):
    """
    Handles Abelton mode

    relative increment / decrements encoded as:
        1-63: increment (higher means more increment)
        64: neutral
        65-127: decrement (higher means more decrement)
    """
    def __init__(self, channel, encoder_num, increment_keys=None, decrement_keys=None):
        self.channel = channel
        self.encoder_num = encoder_num
        self.increment_keys = increment_keys
        self.decrement_keys = decrement_keys

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
        if encoder_num == self.encoder_num:
            keys = []
            if value < 64 and self.increment_keys:
                # increment
                for i in range(value):
                    keys.extend(self.increment_keys)

            elif value > 64 and self.decrement_keys:
                # decrement
                for i in range(value - 64):
                    keys.extend(self.decrement_keys)

        self.keyboard_bridge.send_keys(*keys)

        return True
