class ConfigurationRuntimeError(Exception):
    """
    An exception raised when a configuration isn't valid for the given system.

    For example, a configured device may not exist.
    """
