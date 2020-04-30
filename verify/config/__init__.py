#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"


from .config import *
from ..core.errors import ConfigNotExist, ConfigFileNotFoundError, StringError


class Config(object):
    """ Global Config Class """
    _instance = None   # unique instance~

    NUMBERS = [str(i) for i in range(10)]
    # lower char
    CHARS_LOW = [chr(char) for char in range(97, 123)]
    # upper char
    CHARS_BIG = [chr(char) for char in range(65, 91)]

    # CHAR CONFIG
    # Font
    CHAR_FONT = ImageFont.truetype('Arial.ttf', 40)
    #
    VERIFY_CODE_SET = NUMBERS + CHARS_BIG + CHARS_LOW
    # char counts
    VERIFY_CODE_NUMBER = 4
    # char size
    VERIFY_CODE_SIZE = (40, 40)

    # COLOR
    BACK_COLOR = (255, 255, 255, 255)
    CHAR_COLOR = (0, 0, 0, 255)
    NULL_COLOR = (0, 0, 0, 0)

    # BACKGROUND CONFIG
    # verify size
    VERIFY_SIZE = (180, 60)

    # NOISE CONFIG
    BACK_NOISE_NUMBER = 200
    # Noise size
    BACK_NOISE_TYPE = 2
    # Noise lines number
    LINES_NUMBER = 4

    # CHAR NOISE CONFIG
    CHAR_CUT_NUMBER: int = 8
    # char noise present
    CHAR_CUT_PRESENT: float = 0.2

    CIRCLE_NUMBER = 6

    # GIF
    FRAME_NUMBER = 30

    # control
    TRACK_INTERVAL = 10
    # rotation interval ～ +-60
    ANGLE_INTERVAL = 60
    # start rotation angle
    START_ANGLE = 60

    # verify root dir
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    RSA_FOLDER = 'RSA_KEY'
    RSA_KEY_DIR = os.path.join(os.path.dirname(BASE_DIR), RSA_FOLDER)
    SAFE_ENGINE = 'RSA'

    # secret key for itsdangerous.
    SECRET_KEY = 'a-=3bb51t_x#wza&jh3uz#kgym_yx^!#==l(js4_=w^40xj#7g'

    STORAGE_DIR = 'Verify'  # Storage path

    DEFORM_NUMBER = 2
    DEFORM_OFFSET = 6

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

    def __init__(self, fname: str = None):
        """
        Update config use `fname.py`.
        :param fname: config file of user.
        """
        conf_flag = True   # Whether the user give the fname.

        if fname is None:
            fname = 'config'
            conf_flag = False

        if not isinstance(fname, str):    # Make sure the filename must be a string.
            raise StringError(fname)

        fname = fname.split('.')[0]    # Cut off the extend name.

        # Update config .
        try:
            conf = __import__(fname)
            for k, v in conf.__dict__.items():
                if k.isupper():
                    setattr(self._instance, k, v)

        except ModuleNotFoundError:
            if conf_flag:    # If user give the filename, Not found will raise ..
                raise ConfigFileNotFoundError(fname=fname)


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