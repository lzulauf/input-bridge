import argparse
import importlib
import logging

from ruamel.yaml import YAML

from input_bridge import Manager


logger = logging.getLogger('input_bridge')


def log_level_parser(default_level=None):
    """
    Argument Parser that automatically handles setting log levels.

    Uses logging.WARN as default threshold and raises or lowers the threshold
    with successive quiet and verbose arguments.

    examples:
        Lower logging threshold to info:
            $ prog -v
        Lower logging threshold to debug:
            $ prog -vv
        Raise logging threshold to critical:
            $ prog -qq

    add this functionality to your parser by passing it as a parent:
        parser = argparse.ArgumentParser(parents=[log_level_parser()])
    """
    default_level = default_level or logging.WARNING
    logging.root.setLevel(default_level)
    parser = argparse.ArgumentParser(add_help=False)
    group = parser.add_argument_group('Logging')
    group.add_argument(
        '--verbose', '-v', action=_LoggingAction, dest='log_level', default=default_level,
        help='set verbose level incrementally (repeat to increase futher)')
    group.add_argument(
        '--quiet', '-q', action=_LoggingAction, dest='log_level',
        help='decrease verbose level (repeat to decrease further)')
    return parser


class _LoggingAction(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        kwargs.pop('nargs', None)
        super(_LoggingAction, self).__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=0,  # Specify zero arguments
            **kwargs)

    def __call__(self, parser, namespace, values, option_string):
        multiplier = -1 if option_string in ('-v', '--verbose') else 1
        old_level = getattr(namespace, self.dest, logging.WARNING)
        new_level = old_level + 10*multiplier
        logging.root.setLevel(new_level)
        setattr(namespace, self.dest, old_level + 10 * multiplier)


def _import(object_path):
    if ':' in object_path:
        module_path, object_name = object_path.split(':', 1)
    else:
        module_path, object_name = object_path, None

    module = importlib.import_module(module_path)
    return getattr(module, object_name) if object_name else module


def _load_handler(handler_config, bridges):
    args = [
        bridges[bridge_name]
        for bridge_name in handler_config.get('bridge_args', [])
    ]
    args += handler_config.get('args', [])
    return _import(handler_config['type'])(*args)


def main(argv=None):
    parser = argparse.ArgumentParser(parents=[log_level_parser()])
    parser.add_argument('--config', metavar='YAML', default='config.yml', help='Configuration yaml')
    parser.add_argument(
        '--rate', type=float, default=0.2, help='Update rate in seconds [%(default)s]')
    args = parser.parse_args(argv)

    with open(args.config) as handle:
        config = YAML(typ='safe').load(handle)

    logging.debug(f'{config=}')

    bridges = {
        bridge_name: _import(bridge_config['type'])(*bridge_config.get('args', []))
        for bridge_name, bridge_config in config.get('bridges', {}).items()
    }

    handlers = [
        _load_handler(handler_config, bridges)
        for handler_config in config.get('handlers', [])
    ]

    manager = Manager(
        bridges=list(bridges.values()),
        handlers=handlers,
        rate=args.rate,
    )
    manager.run()


if __name__ == '__main__':
    main()
