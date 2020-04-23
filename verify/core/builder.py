#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

from abc import ABCMeta, abstractmethod
from typing import Iterable
from PIL import Image, ImageDraw
from ..config import config


class AbstractFrameBuilder(metaclass=ABCMeta):
    """ Frame interface. """

    @abstractmethod
    def create_chars(self, angle_iter: Iterable, string: str, char_filter, *args, **kwargs) -> Iterable:
        """ Create character pictures. """

    @abstractmethod
    def create_background(self, line_iter: Iterable, back_filter, *args, **kwargs):
        """ Create character background layer. """

    @abstractmethod
    def back_fix_char(self, frame, char_iter: Iterable, position_iter, *args, **kwargs):
        """ Mix the generated characters into the background layer. """


class CommonBuilderMixin(object):
    """ Common mixing in, achieving some common functions. """

    @staticmethod
    def fix(frame, char, position):
        """
        Fix char to the frame according to position.
        :return the frame mixed char.
        """
        x, y = position

        width, high = char.size

        box = (x, y, x + width, y + high)

        frame.paste(char, box=box, mask=char.split()[3])

    def back_fix_char(self, frame, char_iter, position_iter, *args, **kwargs):
        """ Follow the interface. """

        [self.fix(frame=frame, char=char, position=position) for char, position in zip(char_iter, position_iter)]

    @staticmethod
    def create_background(line_iter: Iterable, back_filter, *args, **kwargs):
        """
        Follow the interface.
        :param line_iter: Noise lines style msg
        :param back_filter: filter of background, add some actions to background.
        :return: back_filter(frame)
        """

        background = Image.new('RGBA', size=config.VERIFY_SIZE, color=config.BACK_COLOR)
        frame = back_filter(back=background, line_iter=line_iter)
        return frame

    @staticmethod
    def create_chars(angle_iter, string: str, char_filter, *args, **kwargs):
        """ Follow the interface. """

        for index, char in enumerate(string):
            angle = angle_iter.__next__()
            img = Image.new('RGBA', config.VERIFY_CODE_SIZE, color=config.NULL_COLOR)
            draw = ImageDraw.Draw(img)
            draw.text(xy=(2, 2), text=char, align='center', font=config.CHAR_FONT, fill=config.BACK_COLOR)
            img = img.rotate(angle=angle, fillcolor=config.NULL_COLOR, expand=True)
            img = char_filter(img)
            del draw
            yield img


class GifFrameBuilder(CommonBuilderMixin, AbstractFrameBuilder):
    """ GifVerify frame builder """

    def create_chars(self, angle_iter, string, char_filter, *args, **kwargs):
        """ create characters for frame of GifVerify. """
        return super().create_chars(angle_iter, string, char_filter, *args, **kwargs)

    def create_background(self, line_iter: Iterable, back_filter, *args, **kwargs):
        """ create background layer for GifVerify. """
        return super().create_background(line_iter=line_iter, back_filter=back_filter, *args, **kwargs)

    def back_fix_char(self, frame, char_iter, position_iter, *args, **kwargs):
        """ frame back_fix_char of GifVerify  """
        super().back_fix_char(frame=frame, char_iter=char_iter, position_iter=position_iter, *args, **kwargs)