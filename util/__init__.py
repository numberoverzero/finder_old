

class ConfigObject(object):
    def __init__(self, default=None):
        self.__default__ = default

    def __getattr__(self, name):
        try:
            return object.__getattr__(self, name)
        except AttributeError:
            return self.__default__
