#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

import random
from abc import ABCMeta, abstractmethod
from math import sqrt

from PIL import Image, ImageDraw
from ..config import config
import numpy as np


class AbstractFilter(metaclass=ABCMeta):
    """ Filter Interface """

    @abstractmethod
    def char_filter(self, char: Image.Image, *args, **kwargs):
        """ filter of char, add some actions to background. """

    @abstractmethod
    def back_filter(self, back: Image.Image, line_iter, *args, **kwargs):
        """ filter of background, add some actions to background. """

    @abstractmethod
    def frame_filter(self, frame: Image.Image, *args, **kwargs):
        """ filter of frame, add some actions to background. """


class Bezier2(object):
    """
    Draw interference lines.
    """

    def __init__(self, draw, points, line_width, line_color):
        """
        :param draw: layer bound objects.
        :param points: points data ((x1,y1), (x2,y2), (x3,y3))
        :param line_width: line bind
        :param line_color: line color
        """
        self.draw = draw
        self.points = points
        self.line_width = line_width
        self.line_color = line_color
        self.current_point = (0, 0)

    def moveto(self, p):
        self.current_point = p

    def lineto(self, p):
        self.draw.line((self.current_point, p), width=self.line_width, fill=self.line_color)
        self.current_point = p

    def render(self):
        NO = 3
        KT = 5
        m = NO - 1
        p = {}  # p[3][2]
        for i in range(0, NO, 2):
            p[i] = self.points[i]

        l1 = 1.0 * (self.points[0][0] - self.points[1][0])
        ll = 1.0 * (self.points[0][1] - self.points[1][1])
        l1 = sqrt(l1 * l1 + ll * ll)

        l2 = 1.0 * (self.points[2][0] - self.points[1][0])
        ll = 1.0 * (self.points[2][1] - self.points[1][1])
        l2 = sqrt(l2 * l2 + ll * ll)

        p[1] = (
            ((l1 + l2) * (l1 + l2) * self.points[1][0] - l2 * l2 * self.points[0][0] - l1 * l1 * self.points[2][0]) / (
                    2 * l1 * l2),
            ((l1 + l2) * (l1 + l2) * self.points[1][1] - l2 * l2 * self.points[0][1] - l1 * l1 * self.points[2][1]) / (
                    2 * l1 * l2)
        )
        '''
        # Draw a tangent
        self.moveto(p[0])
        for i in range(1, m+1):
            self.lineto(p[i])
        '''

        pk = {}  # pk[129][2]
        for i in range(m + 1):
            pk[i] = p[i]

        pt = {}  # pt[129][2]
        for k in range(KT + 1):
            for i in range(0, m + 1, 2):
                pt[2 * i] = pk[i]
            for i in range(m):
                pt[2 * i + 1] = (
                    int(pk[i][0] + pk[i + 1][0]) >> 1,
                    int(pk[i][1] + pk[i + 1][1]) >> 1
                )
            for i in range(1, m):
                pt[2 * i] = (
                    int(pt[2 * i - 1][0] + pt[2 * i + 1][0]) >> 1,
                    int(pt[2 * i - 1][1] + pt[2 * i + 1][1]) >> 1
                )
            for i in range(2 * m + 1):
                pk[i] = pt[i]

            if k == KT:
                break
            m <<= 1
        self.moveto(pk[0])
        for i in range(1, 2 * m + 1):
            self.lineto(pk[i])


class FilterBase(object):
    """ Filter public code block. """

    @staticmethod
    def deform(img: Image.Image):
        """
        Deform the picture as a sine function.
        :param img: Image.Image.
        :return:Image.Image.
        """

        img = np.array(img)    # transform numpy array.
        x, y, a = img.shape   # get the size of image.

        deform = int(0.8 * x / config.DEFORM_NUMBER)  # get deform size.

        length = y + deform * config.DEFORM_NUMBER

        images = np.zeros((x, length, a), np.uint8)

        for index, line in enumerate(img):
            width = int(config.DEFORM_OFFSET * (np.sin(index * np.pi / deform) + 1))
            images[index] = 255   # fill the background.
            images[index, width:y + width] = line   # fill the pattern information into the target array.

        return Image.fromarray(np.uint8(images))   # transform np.array to Image.Image.

    @staticmethod
    def cut_off_char(char):
        """ CHAR_NOISE、CHAR_NOISE_NUMBER control the size and amount of cut off elements. """

        img = np.array(char)

        x, y = img.shape[:2]
        present = float(config.CHAR_NOISE_PRESENT)

        # FIXME: should check the config.

        row = int(x * present)
        col = int(y * present)

        for index in range(config.CHAR_NOISE_NUMBER):
            site_x = random.randint(0, x - row)
            site_y = random.randint(0, y - col)
            img[site_x:site_x + row, site_y:site_y + col] = 0

        return Image.fromarray(np.uint8(img))

    @staticmethod
    def get_content(char, k):
        """
        Find the character boundary by iterating from the two ends of the row and column to the middle
        to cut out the smallest character pattern.
        :param char: Original character picture object.
        :return: Picture objects that contain only character parts.
        """
        # TODO: should try this code block!!! No Q/A:
        img = np.array(char)
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

        # Add some noise to improve human eye recognition.
        img = Image.fromarray(np.uint8(img))

        white = []
        x, y = img.size
        for i in range(x):
            for j in range(y):
                point = (i, j)
                color = img.getpixel(point)

                if color == config.NULL_COLOR:
                    pass
                elif color == config.BACK_COLOR:
                    white.append((i, j))
                else:
                    img.putpixel(point, config.CHAR_COLOR)
        if len(white) <= k:
            k = len(white)
        tmp = random.choices(white, k=k)  # Selected noise coordinates.

        for i in tmp:
            img.putpixel(i, config.CHAR_COLOR)

        return img

    @staticmethod
    def add_back_noise(back, *args, **kwargs):
        """ Add background noise to enhance the difficulty of machine recognition. """

        frame = np.array(back)
        rows, cols, z = frame.shape
        NOISE_TYPE = config.BACK_NOISE_TYPE  # Noise type

        for i in range(config.BACK_NOISE_NUMBER):
            x = np.random.randint(0, rows)
            y = np.random.randint(0, cols)
            frame[x:x + random.randint(1, NOISE_TYPE), y:y + random.randint(1, NOISE_TYPE), :] = config.CHAR_COLOR
        return Image.fromarray(np.uint8(frame))

    @staticmethod
    def add_back_lines(back, line_iter, *args, **kwargs):
        """ Add background noise lines to enhance the difficulty of machine recognition."""
        for line in line_iter:
            draw = ImageDraw.Draw(back)
            tmp = Bezier2(draw, line, 1, (0, 0, 0, 255))
            tmp.render()
            del draw
        return back

    @staticmethod
    def add_back_circle(back):
        """ Add background circle lines to enhance the difficulty of machine recognition."""


class GifFilter(FilterBase, AbstractFilter,):
    """ GifVerify filter. """

    def char_filter(self, char: Image.Image, *args, **kwargs):
        """
        It will be called after generating the character picture.
        Cut off some pixel block of char,deform the char picture,
        add some noise and cut off full pixel.
        """
        char = self.cut_off_char(char=char)
        char = self.deform(img=char)
        return self.get_content(char, k=config.CHAR_POINT_NUMBER)

    def back_filter(self, back: Image.Image, line_iter, *args, **kwargs):
        """
        It will be called after generating the background layer.
        Add some noise and lines to background.
        """
        back = self.add_back_noise(back, *args, **kwargs)
        return self.add_back_lines(back, line_iter, *args, **kwargs)  # add noise lines

    def frame_filter(self, frame: Image.Image, *args, **kwargs):
        """  """


class PngFilter(FilterBase, AbstractFilter):
    """ PngVerify filter. """

    def char_filter(self, char: Image.Image, *args, **kwargs):
        """
        It will be called after generating the character picture.
        Deform the char picture, add some noise, cut off full pixel.
        """
        char = self.deform(img=char)
        return self.get_content(char, k=config.CHAR_POINT_NUMBER)

    def back_filter(self, back: Image.Image, line_iter, *args, **kwargs):
        """ Add some lines for background. """
        return self.add_back_noise(back, *args, **kwargs)

    def frame_filter(self, frame: Image.Image, *args, **kwargs):
        """ """