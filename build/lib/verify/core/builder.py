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
    def create_chars(self, angle_iter: 'Iterable', string: str, char_filter, *args, **kwargs) -> 'Iterable':
        """ Create character pictures. """

    @abstractmethod
    def create_background(self, line_iter: 'Iterable', back_filter, *args, **kwargs):
        """ Create character background layer. """

    @abstractmethod
    def back_fix_char(self, frame, char_iter: 'Iterable', position_iter: 'Iterable', *args, **kwargs) -> None:
        """ Mix the generated characters into the background layer. """


class BuilderBase(object):
    """ Common mixing in, achieving some common functions. """

    def create_chars(self, angle_iter: 'Iterable', string: str, char_filter, *args, **kwargs) -> 'Iterable':
        """ create characters for frame. """

        for index, char in enumerate(string):
            angle = angle_iter.__next__()
            img = Image.new('RGBA', config.VERIFY_CODE_SIZE, color=config.NULL_COLOR)
            draw = ImageDraw.Draw(img)
            draw.text(xy=(1, 1), text=char, align='center', font=config.CHAR_FONT, fill=config.CHAR_COLOR)
            img = img.rotate(angle=angle, fillcolor=config.NULL_COLOR, expand=True)
            img = char_filter(verify=self, char=img)
            del draw
            yield img

    def create_background(self, back_filter, *args, **kwargs) -> 'Image.Image':
        """
        create background layer for GifVerify.
        :param back_filter: filter of background, add some actions to background.
        :return: back_filter(frame)
        """
        background = Image.new('RGBA', size=config.VERIFY_SIZE, color=config.BACK_COLOR)
        frame = back_filter(verify=self, back=background)
        return frame

    @staticmethod
    def fix(frame: 'Image.Image', char: 'Image.Image', position: 'tuple') -> None:
        """ Fix char to the frame according to position. """
        x, y = position

        width, high = char.size

        box = (x, y, x + width, y + high)

        frame.paste(char, box=box, mask=char.split()[3])

    def back_fix_char(self, frame: 'Image.Image', char_iter: 'Iterable', position_iter: 'Iterable', *args, **kwargs) -> None:
        """ Follow the interface. """

        [self.fix(frame=frame, char=char, position=position) for char, position in zip(char_iter, position_iter)]


class GifFrameBuilder(BuilderBase, AbstractFrameBuilder):
    """ GifVerify frame builder """


class PngFrameBuilder(BuilderBase, AbstractFrameBuilder):
    """ PngVerify frame builder """
