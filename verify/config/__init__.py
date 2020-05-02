#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

#     All configurations must be capitalized, such as FRAME_NUMBER, VERIFY_SIZE, if you don't follow this format,
# it will not be included in config.

#     No matter where you introduce config and modify its properties, it will be immediately applied to the global.
# You can even inherit Config and then use the configuration as a class attribute, which is very convenient
# when there are many custom configuration items.

#     You can write your configuration information to a file. Then pass it to Config when it is instantiated, and
# it will update itself with your configuration. It is recommended to customize the configuration information
# in this way.
# Like this：
#
#   from verify import Config
#       Config(myconf)
#   `or`
#       Config(myconf.py)
#   `Tips`
#       1 Suppose you have created myconf.py in the current directory.
#       2 The extension does not affect its work.
#       3 No need to create references for instances,the looks weird, but it ’s okay if you quote it.

import os
from PIL import ImageFont

from ..core.errors import ConfigNotExist, ConfigFileNotFoundError, StringError, CleanParaError


class Config(object):
    """ Global Config Class """
    _instance = None  # unique instance~

    NUMBERS: list = [str(i) for i in range(10)]  # Numbers

    CHARS_LOW: list = [chr(char) for char in range(97, 123)]  # Lower char

    CHARS_BIG: list = [chr(char) for char in range(65, 91)]  # Upper char

    CHAR_FONT = ImageFont.truetype('Arial.ttf', 40)  # Font and size

    VERIFY_CODE_SET: list = NUMBERS + CHARS_BIG + CHARS_LOW  # Random character set

    VERIFY_CODE_NUMBER: int = 4  # Number of characters on each layer

    VERIFY_CODE_SIZE: tuple = (40, 40)  # Character size

    # COLOR
    BACK_COLOR: tuple = (255, 255, 255, 255)
    CHAR_COLOR: tuple = (0, 0, 0, 255)
    NULL_COLOR: tuple = (0, 0, 0, 0)

    VERIFY_SIZE: tuple = (180, 60)  # CAPTCHA size

    BACK_NOISE_NUMBER: int = 200  # Number of background noise

    BACK_NOISE_TYPE: int = 2  # Size of background noise

    LINES_NUMBER: int = 4  # Number of interference lines

    CHAR_CUT_NUMBER: int = 8  # Number of character fragments

    CHAR_CUT_PRESENT: float = 0.2  # Size of incomplete area

    CIRCLE_NUMBER: int = 6  # Number of interference circle

    FRAME_NUMBER: int = 30  # Frame number of GIF Verify

    TRACK_INTERVAL: int = 10  # Character rotation radius

    ANGLE_INTERVAL: int = 60  # < ±60 > Rotation range of characters

    _BASE_DIR: str = os.path.dirname(os.path.dirname(__file__))  # verify root dir

    RSA_FOLDER: str = 'RSA_KEY'  # RSA key save directory

    RSA_KEY_DIR: str = os.path.join(os.path.dirname(_BASE_DIR), RSA_FOLDER)  # RSA key save path

    SAFE_ENGINE: str = 'RSA'  # Default encryption engine

    SECRET_KEY: str = 'a-=3bb51t_x#wza&jh3uz#kgym_yx^!#==l(js4_=w^40xj#7g'  # Secret key for fast encryption engine

    STORAGE_DIR: str = 'Verify'  # Storage location of CAPTCHA path

    DEFORM_NUMBER: int = 2  # Number of character twists
    DEFORM_OFFSET: int = 6  # The degree of character distortion

    def __new__(cls, *args, **kwargs) -> 'Config':
        """
        Ensure that all configurations act on a unique instance.
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)   # Get instance object
        else:
            # Update local capitalized variables as global `config` attributes.
            # and make class method to instance method.
            for k, v in cls.__dict__.items():
                if k.isupper():
                    setattr(cls._instance, k, v)
                if callable(v):
                    if k.endswith('_clean'):
                        try:
                            cls._instance.__asself__(v)()
                        except TypeError:
                            raise CleanParaError(k)
                    setattr(cls._instance, k, cls._instance.__asself__(v))

        return cls._instance   # return this unique object.

    def __getattr__(self, item) -> object:
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

    def __asself__(self, func=None):
        def self_func(*args, **kwargs):
            func(self.__class__._instance, *args, **kwargs)
        return self_func


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
