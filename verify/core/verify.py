#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
__author__ = "monkey"

from abc import abstractmethod, ABCMeta
from typing import Iterable
from PIL import Image
import random


from .storage import GifStorage, PngStorage, AbstractStorage
from ..config import Config
from ..core.errors import ConfigError, FilterError, StyleError, StorageError, BuilderError
from ..core.filter import GifFilter, PngFilter, AbstractFilter
from ..core.style import GifStyle, PngStyle, AbstractStyle
from ..core.builder import GifFrameBuilder, PngFrameBuilder, AbstractFrameBuilder
from ..config import config


class StringMixin(object):
    """ A mixin for subclass add a random strings method. """

    @staticmethod
    def create_string() -> str:
        """  """
        char_list = random.choices(config.VERIFY_CODE_SET, k=config.VERIFY_CODE_NUMBER)
        string = ''.join(char_list)
        return string


class AbstractVerify(metaclass=ABCMeta):

    @abstractmethod
    def create_string(self) -> str:
        """ create random string. """

    @abstractmethod
    def create_frame(self, style_data: dict, *args, **kwargs) -> 'Image.Image':
        """ create a frame layer. """

    @abstractmethod
    def create_verify(self, *args, **kwargs) -> object:
        """ create verify return AbstractStorage instance. """


class CommonVerify(object):

    def __init__(self, config = None, filter=None, style=None, storage=None, builder=None, *args, **kwargs) -> None:
        """
        Commander of GifVerify, it not be instanced.
        :param config: The config will have a higher priority than settings.
        :param filter: For the global filter class, it must be have char_filter、
        back_filter、frame_filter methods.
        :param style: The `style` must be a subclass of  `AbstractStyle`.
        :param string: Character used for Verification code .
        """
        self.string = None

        # TODO:The code seems redundant

        config = config or Config
        if issubclass(config, Config):
            self.config = config(**kwargs)
        else:
            raise ConfigError(config)

        filter = filter or self._meta.filter
        if issubclass(filter, AbstractFilter):
            self.filter = filter()
        else:
            raise FilterError(filter)

        style = style or self._meta.style
        if issubclass(style, AbstractStyle):
            self.style = style()
        else:
            raise StyleError(style)

        storage = storage or self._meta.storage
        if issubclass(storage, AbstractStorage):
            self.storage = storage
        else:
            raise StorageError(storage)

        builder = builder or self._meta.builder

        if issubclass(builder, AbstractFrameBuilder):
            self.builder = builder()
        else:
            raise BuilderError(builder)

    def __call__(self, string=None, *args, **kwargs) -> AbstractStorage:

        self.string = string or self.create_string()

        assert isinstance(self.string, str), "%s must be instance of `str`. Not a %s." % (string, type(string))

        verify = self.create_verify(*args, **kwargs)

        return self.storage(instance=verify, string=self.string, *args, **kwargs)

    def create_frame(self, style_data: dict, *args, **kwargs) -> 'Image.Image':

        self.line_iter = style_data['style']['line']

        # Get frame background.
        self.frame = self.builder.create_background(back_filter=self.filter.back_filter, *args, **kwargs)

        # Get a background characters rotate angle iterator.
        angle_iter: Iterable = style_data['style']['char']['angle']

        # Create a background character iterator.
        char_iter: Iterable = self.builder.create_chars(angle_iter=angle_iter, string=self.string,
                                                   char_filter=self.filter.char_filter)

        # Get a background character position iterator.
        position_iter: Iterable = style_data['style']['char']['position']

        # Fix the char on the background
        self.builder.back_fix_char(frame=self.frame, char_iter=char_iter, position_iter=position_iter,
                              char_filter=self.filter.back_filter)

        # Add filters for new frame.
        return self.filter.frame_filter(verify=self)

    class _meta:
        filter = None
        style = None
        storage = None
        builder = None


class VerifyGif(StringMixin, CommonVerify, AbstractVerify):
    """ Gif verification interface. """

    def create_verify(self, *args, **kwargs) -> list:

        frames = []

        frame_style = self.style.frame_style()

        for frame_index in range(config.FRAME_NUMBER):

            style_data = {
                'style': frame_style.__next__(),
                'string': self.string,
            }

            frame = self.create_frame(style_data=style_data)

            frames.append(frame)

        return frames

    class _meta:
        filter = GifFilter
        style = GifStyle
        storage = GifStorage
        builder = GifFrameBuilder


class VerifyPng(StringMixin, CommonVerify, AbstractVerify):
    """ Png verification interface """

    def create_verify(self, *args, **kwargs) -> 'Image.Image':
        """ Png verify builder in the project . """

        frame_style = self.style.frame_style()
        style_data = {
            'style': frame_style,
            'string': self.string
        }
        frame = self.create_frame(style_data=style_data, builder=PngFrameBuilder)

        return frame

    class _meta:
        filter = PngFilter
        style = PngStyle
        storage = PngStorage
        builder = PngFrameBuilder
