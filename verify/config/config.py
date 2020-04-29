#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"


# All configurations must be capitalized, such as FRAME_NUMBER, VERIFY_SIZE, if you don't follow this format,
# it will not be included in config.

# No matter where you introduce config and modify its properties, it will be immediately applied to the global.
# You can even inherit Config and then use the configuration as a class attribute, which is very convenient
# when there are many custom configuration items.

#           eg:
#               method 1

#               from verify import config
#                   config.PORT = 3309
#
#               method 2

#               from verify import Config
#               class MyConfig(Config):
#                   PORT = 3309
#                   FRAME_NUMBER = 30
#
#               conf = MyConfig    # You have to instantiate it because the update operation depends on the
# __new__ method.


from PIL import ImageFont
import os


# numbers
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
VERIFY_SIZE = (200, 60)

# NOISE CONFIG
BACK_NOISE_NUMBER = 200
# Noise size
BACK_NOISE_TYPE = 2
# Noise lines number
LINES_NUMBER = 6

# CHAR NOISE CONFIG
CHAR_NOISE_NUMBER: int = 4
# char noise present
CHAR_NOISE_PRESENT: float = 0.25
# the color point of the character itself, bigger it is, the clearer the characters
CHAR_POINT_NUMBER = 20

# GIF
FRAME_NUMBER = 30

# JPG/JPEG


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

STORAGE_DIR = '/Users/ms/Desktop/Gif'

DEFORM_NUMBER = 2
DEFORM_OFFSET = 4
# DATABASE = {
#
# }

