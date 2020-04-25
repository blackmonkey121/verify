#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
__author__ = "monkey"

from typing import Iterable
import random

from .storage import GifStorage, PngStorage
from ..config import Config
from ..core.errors import ConfigError, FilterError, StyleError, StorageError
from ..core.filter import GifFilter, PngFilter
from ..core.style import GifStyle, PngStyle
from ..core.builder import GifFrameBuilder, PngFrameBuilder
from ..config import config


class StringMixin(object):
    """ A mixin for subclass add a random strings method. """

    @staticmethod
    def create_string():
        """  """
        char_list = random.choices(config.VERIFY_CODE_SET, k=config.VERIFY_CODE_NUMBER)
        string = ''.join(char_list)
        return string


class CommonVerify(object):

    def __init__(self, config=None, filter=None, style=None, storage=None, *args, **kwargs):
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
            self.config = config()
        else:
            raise ConfigError(config)

        filter = filter or self._meta.filter
        if issubclass(filter, self._meta.filter):
            self.filter = filter()
        else:
            raise FilterError(filter)

        style = style or self._meta.style
        if issubclass(style, self._meta.style):
            self.style = style()
        else:
            raise StyleError(style)

        storage = storage or self._meta.storage
        if issubclass(storage, self._meta.storage):
            self.storage = storage
        else:
            raise StorageError(storage)

    def __call__(self, string=None, *args, **kwargs):

        self.string = string or self.create_string()

        assert isinstance(self.string, str), "%s must be instance of `str`. Not a %s." % (string, type(string))

        verify = self.create_verify(*args, **kwargs)

        return self._meta.storage(instance=verify, string=self.string, *args, **kwargs)

    class _meta:
        filter = None
        style = None
        storage = None
        builder = None


class VerifyGif(StringMixin, CommonVerify):
    """ """

    def create_frame(self, style_data, *args, **kwargs):

        builder = self._meta.builder or kwargs.get('builder', None)

        if not issubclass(builder, self._meta.builder):
            raise ('%s must be a subclass of `%s`.' % (builder, self._meta.builder.__class__.__name__))

        builder = builder()

        line_iter = style_data['style']['line']

        # Get frame background.
        frame = builder.create_background(line_iter=line_iter, back_filter=self.filter.back_filter, *args, **kwargs)

        # Get a background characters rotate angle iterator.
        angle_iter: Iterable = style_data['style']['char']['angle']

        # Create a background character iterator.
        char_iter: Iterable = builder.create_chars(angle_iter=angle_iter, string=self.string,
                                                   char_filter=self.filter.char_filter)

        # Get a background character position iterator.
        position_iter: Iterable = style_data['style']['char']['position']

        # Fix the char on the background
        builder.back_fix_char(frame=frame, char_iter=char_iter, position_iter=position_iter,
                              char_filter=self.filter.back_filter)

        # Add filters for new frame.
        self.filter.frame_filter(frame)

        return frame

    def create_verify(self, *args, **kwargs):

        frames = []

        frame_style = self.style.frame_style()

        for frame_index in range(config.FRAME_NUMBER):
            style = frame_style.__next__()
            style_data = {
                'style': style,
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


class PngVerify(StringMixin, CommonVerify):
    """  """

    def create_frame(self, style_data, builder=PngFrameBuilder, *args, **kwargs):

        builder = builder or kwargs.get('builder', None)

        if not issubclass(builder, PngFrameBuilder):
            raise ('%s must be a subclass of `PngFrameBuilder`.' % builder)

        builder = builder()   # get the builder instance.

        line_iter = style_data['style']['line']    # Noise lines style data :Type Iterable.

        # Get frame background.
        frame = builder.create_background(line_iter=line_iter, back_filter=self.filter.back_filter, *args, **kwargs)

        # Get a background characters rotate angle iterator.
        angle_iter: Iterable = style_data['style']['char']['angle']

        # Create a background character iterator.
        char_iter: Iterable = builder.create_chars(angle_iter=angle_iter, string=self.string, char_filter=self.filter.char_filter)

        # Get a background character position iterator.
        position_iter: Iterable = style_data['style']['char']['position']

        # Fix the char on the background
        builder.back_fix_char(frame=frame, char_iter=char_iter, position_iter=position_iter, char_filter=self.filter.back_filter)

        # Add filters for new frame.
        self.filter.frame_filter(frame)

        return frame

        # Fixme Add others.

    def create_verify(self, *args, **kwargs):
        """ Jpeg verify builder in the project . """

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

