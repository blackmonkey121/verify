#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"


from .config import *
from ..core.errors import ConfigNotExist


class Config(object):
    """ Global Config Class """
    _instance = None   # unique instance~

    def __new__(cls, *args, **kwargs):
        """
        Ensure that all configurations act on a unique instance.
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)   # Get instance addr
            # Add all current uppercase variables as instance attributes.
            for k, v in globals().items():
                if k.isupper():
                    setattr(cls._instance, k, v)
        else:
            # Update local capitalized variables as global `config` attributes.
            for k, v in cls.__dict__.items():
                if k.isupper():
                    setattr(cls._instance, k, v)
        return cls._instance   # return this unique object.

    def __getattr__(self, item):
        """"""
        try:
            return self[item]
        except TypeError:
            pass  # FIXME: add log
        raise ConfigNotExist(item)


config = Config()

if __name__ == "__main__":

    # test ...
    class MyConfig(Config):

        NAME = 'Monkey'

        TEST_UPDATE = 'UPDATE_INIT'

        test_low = 'asd'

    config = Config()
    print(config.__dict__)

    my_config = MyConfig()
    print(my_config.__dict__)

    # print(my_config.test_low)

    print(my_config.not_exist)