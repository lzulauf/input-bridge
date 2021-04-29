import enum
"""
Killamix Mini MIDI adapter


Push Button Configuration Mode

    Push button configuration mode can be entered by holding down the 9 Knob button and pressing the
    8 Knob button. Each push button's mode can be toggled by pressing that push button

    On: Pushing the button sends a single control message of 127
    Off: Pushing the button sends a control message of 127 when pressed, 0 when released
    Flashing: Push button toggles between sending 127 and 0 each time it is pressed


Configuration Mode

    Enter configuration mode by unplugging, then holding the 6 and 8 _push_ buttons while booting
    up. The 9 push button will be illuminated. Pressing the other push buttons will toggle
    features. Pressing the 9 push button will exit configuration mode.

    1: Encoder mode
       Off (send absolute values)
       1 (send deltas using Doepfer encoding)
       2 (send deltas using Ableton encoding)
    2: Joystick mode - See Joystick Channels below
       Off (Standard Mode - 2 Axis)
       1 (Send as four axes analog ranging 0-127)
       2 (Send as four axes binary 0,127)
    3: Receive mode
       Off (ignores incoming midi messages)
       1 (Enable setting midi values for all channels and encoders)
       2 (Enable setting only push button on/off state)
    4: Hi-Speed Encoder mode
        Off (normal operation. Encoder values change based on three detected speeds)
        On (Much lower thresholds for entering higher encoder delta speeds)
    5: Push Button MIDI Notes
        Off (Normal operation - buttons send control signals)
        1 (Notes send white key notes starting from middle C #60)
        2 (Notes send all consecutive keys starting from #36)
        3 (Notes send all consecutive keys starting from #48)
        4 (Notes send all consecutive keys starting from #60)
    6: Knob button mode
        Off (Knob buttons change channels)
        1 (Knob buttons send 127 message on encoding channels 24-32 on current channel when
           pressed, nothing on release)
        2 (Knob buttons send 127 message on encoding channels 24-32 on current channel when
           pressed, 0 on release)
    7: Offset mode
        Off (Send standard encoder numbers)
        1 (2, 3, ...) (Add 10 (20, 30, ...) to all encoder numbers)


Joystick channels
    2 Axis Mode (X = channel 19, Y = channel 20)
    4 Axis Mode (Right=19, Up=20, Left=21, Right=22)


Ableton encoding:
    relative increment / decrements encoded as:
        1-63: increment (higher means more increment)
        64: neutral
        65-127: decrement (higher means more decrement)
"""


# Encoder number for knob presses. Channel will be the knob pressed
KNOB_BUTTON_ENCODER = 23


class KillamixMidiChannel(enum.Enum):
    One = 176
    Two = 177
    Three = 178
    Four = 179
    Five = 180
    Six = 181
    Seven = 182
    Eight = 183
    Nine = 184
