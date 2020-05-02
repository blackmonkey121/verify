#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
__author__ = "monkey"

from abc import ABCMeta, abstractmethod
from math import cos, sin, pi
import random
from typing import Iterable

from ..config import config


class AbstractStyle(metaclass=ABCMeta):

    @abstractmethod
    def get_lines(self, *args, **kwargs) -> 'Iterable':
        """ lines styles """

    @abstractmethod
    def get_positions(self, *args, **kwargs) -> list:
        """ positions styles """

    @abstractmethod
    def get_angles(self, *args, **kwargs) -> list:
        """ angles styles """

    @abstractmethod
    def frame_style(self, *args, **kwargs) -> 'Iterable':
        """ frame styles"""


class StyleCommonMixin(object):
    """ Some common method. """

    @staticmethod
    def get_frame_position() -> 'Iterable':
        """ Generate initial data for the coordinates of a frame of characters in the background. """

        x, y = config.VERIFY_SIZE
        char_x, char_y = config.VERIFY_CODE_SIZE
        site_y = (y - char_y) // 6  # coordinate
        sep = int(x * 0.9 // config.VERIFY_CODE_NUMBER)  # step length

        for index in range(config.VERIFY_CODE_NUMBER):
            site = (sep * index, site_y)  # Trajectory center

            yield site

    @staticmethod
    def get_frame_angle() -> 'Iterable':
        """ Initial data of character rotation angle on one frame. """
        s_angle = config.ANGLE_INTERVAL
        for angle in range(config.VERIFY_CODE_NUMBER):
            yield random.randint(-s_angle, s_angle)

    @staticmethod
    def get_first_line() -> 'Iterable':
        """ One frame style of data. """

        x, y = config.VERIFY_SIZE

        # offset list: random choose a function to simulate randomly moving a pixel.
        funcs = [
            lambda x, y, start, end: (x + random.randint(start, end), y + random.randint(start, end)),
            lambda x, y, start, end: (x + random.randint(start, end), y - random.randint(start, end)),
            lambda x, y, start, end: (x - random.randint(start, end), y + random.randint(start, end)),
            lambda x, y, start, end: (x - random.randint(start, end), y - random.randint(start, end)),
        ]

        for i in range(config.LINES_NUMBER):
            p1 = (random.randint(0, x), random.randint(0, y))
            p2 = random.choice(funcs)(*p1, 20, 30)
            p3 = random.choice(funcs)(*p2, 20, 30)
            yield p1, p2, p3

    @staticmethod
    def get_next_line(line_iter: 'Iterable') -> 'Iterable':
        """ get next line style data. """

        one_step = [
            lambda x, y: (x + 1, y + 1),  # ↗ Move 1 pixel in the upper right corner.
            lambda x, y: (x + 1, y - 1),  # ↘ Move 1 pixel in the lower right corner.
            lambda x, y: (x - 1, y + 1),  # ↙ Move 1 pixel in the lower left corner.
            lambda x, y: (x - 1, y - 1),  # ↖ Move 1 pixel in the upper left corner.
        ]

        for line in line_iter:
            p1, p2, p3 = line

            p1 = random.choice(one_step)(*p1)
            p2 = random.choice(one_step)(*p2)
            p3 = random.choice(one_step)(*p3)
            yield p1, p2, p3

    def get_lines(self, *args, **kwargs) -> 'Iterable':
        """ get lines style data. """
        current_line = self.get_first_line()
        for line in range(config.FRAME_NUMBER):
            tmp = [i for i in current_line]
            yield tmp.__iter__()
            current_line = self.get_next_line(tmp)


class GifStyle(StyleCommonMixin, AbstractStyle):
    """ A style class for Gif verify. """

    def get_positions(self, *args, **kwargs) -> list:
        """ Position data of all frames and characters in the background in one GIF. """
        positions = []

        for site in self.get_frame_position():
            char_position = []

            x, y = site
            r = config.TRACK_INTERVAL
            angle = random.randint(0, 360)
            sep = 360 // config.FRAME_NUMBER
            for index in range(1, config.FRAME_NUMBER + 1):
                x1 = x + r * cos(angle * pi / 180)
                y1 = y + r * sin(angle * pi / 180)
                angle += sep
                char_position.append((int(x1), int(y1)))

            positions.append(char_position)

        return positions

    def get_angles(self, *args, **kwargs) -> list:
        """ One frame angles data. """
        ret = []
        N = config.FRAME_NUMBER // 2
        for index in range(config.VERIFY_CODE_NUMBER):
            angle = random.randint(0, config.ANGLE_INTERVAL)
            sep = config.ANGLE_INTERVAL // N

            tmp = [angle + i * sep for i in range(N)]

            ret.append(tmp + tmp[::-1])
        return ret

    def frame_style(self, *args, **kwargs) -> Iterable:
        """ frame style include lines、angles、positions and ... """
        char_positions = self.get_positions()
        char_angles = self.get_angles()
        lines = self.get_lines()

        for frame_index in range(config.FRAME_NUMBER):

            char_position = []
            char_angle = []

            for char_index in range(config.VERIFY_CODE_NUMBER):
                char_position.append(char_positions[char_index][frame_index])
                char_angle.append(char_angles[char_index][frame_index])

            # format data
            yield {
                'char': {
                    'position': char_position.__iter__(),
                    'angle': char_angle.__iter__(),
                },
                'line': lines.__next__(),
            }


class PngStyle(StyleCommonMixin, AbstractStyle):
    """ A style class for Png verify.It's not recommend. """

    def get_positions(self, *args, **kwargs) -> 'Iterable':
        """ Get character position on the frame. """

        position = self.get_frame_position()

        return position

    def get_angles(self, *args, **kwargs) -> 'Iterable':
        """ Get character spin angle on the frame. """

        angles = self.get_frame_angle()

        return angles

    def get_lines(self, *args, **kwargs) -> Iterable:
        """
        Get a frame Noise-Line arguments.
        :return: A tuple containing three pixel.
        """
        return self.get_first_line()

    def frame_style(self, *args, **kwargs) -> Iterable:
        """
        Package style arguments for the frame.
        :return: A dict that containing all style arguments
        """
        return {
            'char': {
                'position': self.get_positions(),
                'angle': self.get_angles(),
            },
            'line': self.get_lines(),
        }
