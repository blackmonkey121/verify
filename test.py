#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"
# —————————————————— storage
# from verify.config import config
# from verify.core.storage import GifStorage
#
# from PIL import Image
#
# config.STORAGE_DIR = 'result'   # define save dir
#
# gif = [Image.new('RGBA', (40, 40), color=config.NULL_COLOR) for i in range(10)]
# test_gif = GifStorage(instance=gif, string='xxxx')
#
# test_gif.save_file()

# ——————————————————— safe

# from verify.core.safe import Safe
#
# safe = Safe()
#
# en_str = safe.coding('monkey', method='fast', verify_type='png')
# print(en_str)
# de_str = safe.parse(en_str)
# print(de_str)
#
# en_str = safe.coding('m324', method='Rsa')
# print(en_str)
# de_str = safe.parse(en_str)
# print(de_str)
#
# # en_str = safe.coding([1,1,1], method='sa')
# # print(en_str)
# # de_str = safe.parse(en_str)
# # print(de_str)
#
#
# en_str = safe.coding(method={})
# print(en_str)
# de_str = safe.parse(en_str)
# print(de_str)

# —————————————————————————— verify


from verify.core.verify import VerifyGif, PngVerify


gif = VerifyGif()
a = gif('Mn3y')
a.save_file()
# png = PngVerify()
# b = png('Png1')
# b.save_file()
import numpy as np
import cv2 as cv
# p=np.array([[0,0.],[0,1],[1,1],[1,0]])
# q=np.array([[0.3,0.3],[0,1],[1,1],[1,0]])
# import matplotlib.image as py
# img=py.imread('/Users/ms/Desktop/Gif/Verify986649.png')
# # img = cv.imread('/Users/ms/Desktop/Gif/Verify986649.png')
# u,v=img.shape[:2]
# def f(i,j):
#     return i
# def g(i,j):
#     return j+0.01*np.sin( 3*np.pi*i)
# M=[]
# N=[]
# for i in range(u):
#     for j in range(v):
#         i0=i/u
#         j0=j/v
#         u0=int(f(i0,j0)*u)
#         v0=int(g(i0,j0)*v)
#         M.append(u0)
#         N.append(v0)
# m1,m2=max(M),max(N)
# n1,n2=min(M),min(N)
# r=np.zeros((m1-n1,m2-n2,4))
# for i in range(u):
#     for j in range(v):
#         i0=i/u
#         j0=j/v
#         u0=int(f(i0,j0)*u)-n1-1
#         v0=int(g(i0,j0)*v)-n2-1
#         print(r[u0,v0], img[i,j])
#         r[u0,v0]=img[i,j]
# py.imsave('/Users/ms/Desktop/Gif/reVerify986649.png',r)
# cv.imwrite('/Users/ms/Desktop/Gif/reVerify986649.png',r)


# img = cv.imread('/Users/ms/Desktop/Gif/Verify986649.png')
# DEFORM_NUMBER = 3
#
# DEFORM_OFFSET = 10

# def deform(img):
#
#     x, y = img.shape[:2]    # get the size of image.
#
#     deform = int(0.8 * x / DEFORM_NUMBER)   # get deform size.
#
#     length = y + deform * DEFORM_NUMBER // 2
#
#     images = np.zeros((x, length, 3), np.uint8)
#
#     for index, line in enumerate(img):
#         width = int(DEFORM_OFFSET * (np.sin(index * np.pi / deform) + 1))
#         images[index] = 255
#         images[index, width:y + width] = line
#
#     return images
#
# image = deform(img)
#
# cv.imwrite('test.png', image)