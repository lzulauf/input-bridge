from input_bridge import Manager
from input_bridge.bridges.midi import MidiBridge
from input_bridge.bridges.keyboard import KeyboardBridge
from input_bridge.bridges.mac_osa import MacOSABridge
from input_bridge.handlers.midi_to_keyboard import MidiKeyboardHandler
from input_bridge.handlers.midi_to_mac_osa import MidiMacMuteHandler, MidiMacVolumeHandler
from input_bridge.devices.killamix_mini import KillamixMidiChannel

"""
This script will control various MacOS functionality with a Killamix Mini controller.

- The mini's first channel will control the system volume (be sure to set your encoder mode to use
  absolute values)
- The mini's first push button will control volume mute status (be sure to set your first push
  button to flashing mode)
- The mini's second push button will send Cmd-Shift-A (hotkey for toggling microphone in Zoom)
- The mini's second push button will send Cmd-Shift-V (hotkey for toggling video camera in Zoom)
"""


def main(argv=None):
    midi_bridge = MidiBridge('Kenton Killamix Mini')
    keyboard_bridge = KeyboardBridge()
    mac_osa_bridge = MacOSABridge()
    handlers = [
        MidiMacVolumeHandler(midi_bridge, mac_osa_bridge, KillamixMidiChannel.One.value, 1),
        MidiMacMuteHandler(midi_bridge, mac_osa_bridge, KillamixMidiChannel.One.value, 10),
        MidiKeyboardHandler(
            midi_bridge, keyboard_bridge, KillamixMidiChannel.One.value, 11, 'command+shift+a'),
        MidiKeyboardHandler(
            midi_bridge, keyboard_bridge, KillamixMidiChannel.One.value, 12, 'command+shift+v'),
    ]

    manager = Manager(
        bridges=(midi_bridge, keyboard_bridge, mac_osa_bridge),
        handlers=handlers)
    manager.run()


if __name__ == '__main__':
    main()
