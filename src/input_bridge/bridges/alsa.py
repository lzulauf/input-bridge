import re
import subprocess

from input_bridge import Bridge

CURRENT_VOLUME_RE = re.compile(r'^.* (Left|Right):.*\[(?P<percent>\d+)%\] \[(?P<off_on>off|on)\].*$')


class AlsaBridge(Bridge):
    def __init__(self):
        pass

    def get_volume(self):
        """
        Get volume.

        Volume is a float between 0.0 and 1.0.
        """
        completed_process = subprocess.run(
            ['amixer', '-D', 'pulse', 'get', 'Master'],
            check=True,
            capture_output=True,
        )
        for line in completed_process.stdout.decode().splitlines():
            if match := CURRENT_VOLUME_RE.match(line):
                return int(int(match.group('percent')) / 100.0 * 127)
        raise RuntimeError('Could not determine volume.')

    def get_muted(self):
        """
        Get muted.
        """
        completed_process = subprocess.run(
            ['amixer', '-D', 'pulse', 'get', 'Master'],
            check=True,
            capture_output=True,
        )
        for line in completed_process.stdout.decode().splitlines():
            if match := CURRENT_VOLUME_RE.match(line):
                return match.group('off_on') == 'off'
        raise RuntimeError('Could not determine muted status.')

    def set_volume(self, percent):
        """
        Set master volume to percent [0.0, 1.0].
        """
        subprocess.run(
            ['amixer', '-D', 'pulse', 'sset', 'Master', f'{percent*100:0.0f}%'],
            check=True,
        )

    def set_mute(self, muted):
        """
        Set mute to muted (mutes if True, otherwise unmutes)
        """
        subprocess.run(
            ['amixer', '-D', 'pulse', 'set', 'Master', 'mute' if muted else 'unmute' ],
            check=True,
        )

    def get_microphone_volume(self):
        """
        Get microphone volume.

        Volume is a float between 0.0 and 1.0.
        """
        completed_process = subprocess.run(
            ['amixer', '-D', 'pulse', 'get', 'Capture'],
            check=True,
            capture_output=True,
        )
        for line in completed_process.stdout.decode().splitlines():
            if match := CURRENT_VOLUME_RE.match(line):
                return int(int(match.group('percent')) / 100.0 * 127)

        raise RuntimeError('Could not determine microphone volume.')

    def get_microphone_muted(self):
        """
        Get microphone muted.
        """
        completed_process = subprocess.run(
            ['amixer', '-D', 'pulse', 'get', 'Capture'],
            check=True,
            capture_output=True,
        )
        for line in completed_process.stdout.decode().splitlines():
            if match := CURRENT_VOLUME_RE.match(line):
                return match.group('off_on') == 'off'

        raise RuntimeError('Could not determine microphone muted status.')

    def set_microphone_volume(self, percent):
        """
        Set master volume to percent [0.0, 1.0].
        """
        subprocess.run(
            ['amixer', '-D', 'pulse', 'sset', 'Capture', f'{percent*100:0.0f}%'],
            check=True,
        )

    def set_microphone_mute(self, muted):
        """
        Set mute to muted (mutes if True, otherwise unmutes)
        """
        subprocess.run(
            ['amixer', '-D', 'pulse', 'set', 'Capture', 'nocap' if muted else 'cap' ],
            check=True,
        )

    def begin_update(self):
        pass

    def end_update(self):
        pass
