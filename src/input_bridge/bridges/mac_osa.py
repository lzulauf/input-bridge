import osascript

from input_bridge import Bridge


class MacOSABridge(Bridge):

    def run(self, command, background=False):
        return osascript.run(command, background=background)

    def get_current_volume(self):
        code, out, err = self.run('output volume of (get volume settings)', background=False)
        try:
            return int(out)
        except ValueError:
            return 0

    def set_current_volume(self, volume):
        self.run(f'set volume output volume {volume}', background=False)
