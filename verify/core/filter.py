#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

import random
from abc import ABCMeta, abstractmethod
from typing import Iterable

from PIL import Image
from ..config import config
import numpy as np
import cv2 as cv

# FIXME: `PIL.Image.Image` and `np.ndarray` question will eliminate the dependence on PIL and solve.


class AbstractFilter(metaclass=ABCMeta):
    """ Filter Interface """

    @abstractmethod
    def char_filter(self, verify: object, char: 'Image.Image', *args, **kwargs) -> 'Image.Image':
        """ filter of char, add some actions to background. """

    @abstractmethod
    def back_filter(self, verify: object, back: 'Image.Image', *args, **kwargs) -> 'Image.Image':
        """ filter of background, add some actions to background. """

    @abstractmethod
    def frame_filter(self, verify: object, *args, **kwargs) -> 'Image.Image':
        """ filter of frame, add some actions to background. """


class FilterBase(object):
    """ Filter public code block. """

    @staticmethod
    def write_line(img: 'np.ndarray', points: tuple) -> None:
        """ writer lines for img. """
        length = len(points)
        index = 0

        while index < length - 1:
            cv.line(img=img, pt1=points[index], pt2=points[index+1],
                    color=config.CHAR_COLOR, thickness=1, )
            index += 1

    @staticmethod
    def deform(img: 'np.ndarray') -> 'np.ndarray':
        """
        Deform the picture as a sine function.
        :param img: np.ndarray.
        :return:np.ndarray
        """
        x, y, a = img.shape  # get the size of image.

        deform = int(0.8 * x / config.DEFORM_NUMBER)  # get deform size.

        length = y + deform * config.DEFORM_NUMBER

        images = np.zeros((x, length, a), np.uint8)

        for index, line in enumerate(img):
            width = int(config.DEFORM_OFFSET * (np.sin(index * np.pi / deform) + 1))
            images[index] = 255  # fill the background.
            images[index, width:y + width] = line  # fill the pattern information into the target array.

        return images

    @staticmethod
    def cut_off_char(img: 'np.ndarray') -> 'np.ndarray':
        """ CHAR_CUT、CHAR_CUT_NUMBER control the size and amount of cut off elements. """

        x, y = img.shape[:2]
        present = float(config.CHAR_CUT_PRESENT)

        # FIXME: should check the config.

        row = int(x * present)
        col = int(y * present)

        for index in range(config.CHAR_CUT_NUMBER):
            site_x = random.randint(0, x - row)
            site_y = random.randint(0, y - col)
            img[site_x:site_x + row, site_y:site_y + col] = 0

        return img

    @staticmethod
    def get_content(img: 'np.ndarray') -> 'np.ndarray':
        """
        Find the character boundary by iterating from the two ends of the row and column to the middle
        to cut out the smallest character pattern.
        :param img: Original character picture object.
        :return: Picture objects that contain only character parts.
        """
        # TODO: should try this code block!!! No Q/A:
        x, y, z = img.shape

        site = [None] * 4

        i = 0

        # search the char index side.
        while not all([site[1], site[3]]):

            if not site[1] and np.any(img[i, :, z - 1]):
                site[1] = i
            if not site[3] and np.any(img[x - i - 1, :, z - 1]):
                site[3] = x - i - 1

            i += 1

        i = 0

        while not all([site[0], site[2]]):
            if not site[0] and np.any(img[:, i, z - 1]):
                site[0] = i

            if not site[2] and np.any(img[:, y - i - 1, z - 1]):
                site[2] = y - i - 1

            i += 1

        img = img[site[1]:site[3], site[0]:site[2]]
        return img

    @staticmethod
    def add_noise(img: 'np.ndarray', *args, **kwargs) -> 'np.ndarray':
        """ Add background noise to enhance the difficulty of machine recognition. """

        rows, cols, z = img.shape
        noise_type = kwargs.get('noise_type', None) or config.BACK_NOISE_TYPE  # Noise type
        noise_number = kwargs.get('noise_number', None) or config.BACK_NOISE_NUMBER

        for i in range(noise_number):
            x = np.random.randint(0, rows)
            y = np.random.randint(0, cols)
            img[x:x + random.randint(1, noise_type), y:y + random.randint(1, noise_type), :] = config.CHAR_COLOR
        return img

    def add_lines(self, img: 'np.ndarray', line_iter: 'Iterable', *args, **kwargs) -> 'np.ndarray':
        """ Add background noise lines to enhance the difficulty of machine recognition."""

        for line in line_iter:
            self.write_line(img=img, points=line)
        return img

    @staticmethod
    def add_circle(img: 'np.ndarray') -> 'np.ndarray':
        """ Add background circle lines to enhance the difficulty of machine recognition."""
        x, y, a = img.shape

        sep = y // config.CIRCLE_NUMBER

        center = lambda start: (random.randint(start, start + sep), random.randint(1, x))  # Circle center site
        r = lambda : random.randint(2, 12)

        for index in range(config.CIRCLE_NUMBER):
            start = index * sep
            cv.circle(img, center(start), r(), config.CHAR_COLOR)

        return img

    @staticmethod
    def get_contours(img: 'np.ndarray') -> 'np.ndarray':

        binary_img = cv.Canny(img, 50, 200)  # binary image.
        # get contours.
        h = cv.findContours(binary_img, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
        contours = h[0]  # get contours.

        # create char image of background.
        char_img = np.zeros(img.shape, np.uint8)

        for cloud in contours:
            for elem in cloud:
                char_img[elem[0][1], elem[0][0]] = config.CHAR_COLOR

        return char_img


class GifFilter(FilterBase, AbstractFilter, ):
    """ GifVerify filter. """

    def char_filter(self, verify: object, char: 'Image.Image', *args, **kwargs) -> 'Image.Image':
        """
        It will be called after generating the character picture.
        Cut off some pixel block of char,deform the char picture,
        add some noise and cut off full pixel.
        """

        char: np.ndarray = np.array(char)
        char = self.get_contours(img=char)
        char = self.deform(img=char)
        char = self.get_content(img=char)
        char = self.cut_off_char(img=char)

        return Image.fromarray(np.uint8(char))

    def back_filter(self, verify: object, back: 'Image.Image', *args, **kwargs) -> 'Image.Image':
        """
        It will be called after generating the background layer.
        Add some noise and lines to background.
        """

        back: np.ndarray = np.array(back)

        back = self.add_noise(img=back, *args, **kwargs)


        return Image.fromarray(np.uint8(back))

    def frame_filter(self, verify: 'object', *args, **kwargs) -> 'Image.Image':
        """  """
        frame = verify.frame
        line_iter = verify.line_iter

        frame: np.ndarray = np.array(frame)   # transform to np.ndarray.

        self.add_lines(img=frame, line_iter=line_iter)

        return Image.fromarray(np.uint8(frame))


class PngFilter(FilterBase, AbstractFilter):
    """ PngVerify filter. """

    def char_filter(self, verify: object, char: 'Image.Image', *args, **kwargs) -> 'Image.Image':
        """
        It will be called after generating the character picture.
        Deform the char picture, add some noise, cut off full pixel.
        """
        char: np.ndarray = np.array(char)

        char = self.get_contours(img=char)
        char = self.deform(img=char)
        char = self.get_content(img=char)

        return Image.fromarray(np.uint8(char))

    def back_filter(self, verify: object, back: 'Image.Image', *args, **kwargs) -> 'Image.Image':
        """ Add some lines for background. """
        return back

    def frame_filter(self, verify: object, *args, **kwargs) -> 'Image.Image':
        """ """
        frame = verify.frame
        line_iter = verify.line_iter

        frame: np.ndarray = np.array(frame)

        frame = self.add_circle(frame)
        frame = self.add_noise(frame)
        frame = self.add_lines(frame, line_iter)

        return Image.fromarray(np.uint8(frame))