#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

import random
from abc import ABCMeta, abstractmethod
from math import sqrt

from PIL import Image, ImageDraw
from ..config import config
import numpy as np
import cv2 as cv


class AbstractFilter(metaclass=ABCMeta):
    """ Filter Interface """

    @abstractmethod
    def char_filter(self, verify, char: Image.Image, *args, **kwargs):
        """ filter of char, add some actions to background. """

    @abstractmethod
    def back_filter(self, verify, back: Image.Image, *args, **kwargs):
        """ filter of background, add some actions to background. """

    @abstractmethod
    def frame_filter(self, verify, frame: Image.Image, line_iter, *args, **kwargs):
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
    def deform(img: np.ndarray):
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
    def cut_off_char(img):
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
    def get_content(img):
        """
        Find the character boundary by iterating from the two ends of the row and column to the middle
        to cut out the smallest character pattern.
        :param char: Original character picture object.
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
    def add_noise(img, *args, **kwargs):
        """ Add background noise to enhance the difficulty of machine recognition. """

        frame = np.array(img)
        rows, cols, z = frame.shape
        noise_type = kwargs.get('noise_type', None) or config.BACK_NOISE_TYPE  # Noise type
        noise_number = kwargs.get('noise_number', None) or config.BACK_NOISE_NUMBER

        for i in range(noise_number):
            x = np.random.randint(0, rows)
            y = np.random.randint(0, cols)
            frame[x:x + random.randint(1, noise_type), y:y + random.randint(1, noise_type), :] = config.CHAR_COLOR
        return Image.fromarray(np.uint8(frame))

    @staticmethod
    def add_lines(img, line_iter, *args, **kwargs):
        """ Add background noise lines to enhance the difficulty of machine recognition."""
        for line in line_iter:
            draw = ImageDraw.Draw(img)
            tmp = Bezier2(draw, line, 1, (0, 0, 0, 255))
            tmp.render()
            del draw
        return img

    @staticmethod
    def add_circle(img):
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
    def get_contours(img):

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

    def char_filter(self, verify, char: Image.Image, *args, **kwargs):
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

    def back_filter(self, verify, back: Image.Image, *args, **kwargs):
        """
        It will be called after generating the background layer.
        Add some noise and lines to background.
        """
        return self.add_noise(img=back, *args, **kwargs)

    def frame_filter(self, verify, frame: Image.Image = None, line_iter=None, *args, **kwargs):
        """  """
        frame = frame or verify.frame
        line_iter = line_iter or verify.line_iter
        verify.frame = self.add_lines(img=frame, line_iter=line_iter)


class PngFilter(FilterBase, AbstractFilter):
    """ PngVerify filter. """

    def char_filter(self, verify, char: Image.Image, *args, **kwargs):
        """
        It will be called after generating the character picture.
        Deform the char picture, add some noise, cut off full pixel.
        """
        char: np.ndarray = np.array(char)

        char = self.get_contours(img=char)
        char = self.deform(img=char)
        char = self.get_content(img=char)

        return Image.fromarray(np.uint8(char))

    def back_filter(self, verify, back: Image.Image, *args, **kwargs):
        """ Add some lines for background. """
        return back

    def frame_filter(self, verify, frame: Image.Image = None, *args, **kwargs):
        """ """
        frame = verify.frame or frame
        frame: np.ndarray = np.array(frame)
        frame = self.add_circle(frame)
        frame = self.add_noise(frame)
        verify.frame = Image.fromarray(np.uint8(frame))