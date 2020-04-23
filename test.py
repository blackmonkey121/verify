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


from verify.core.verify import VerifyGif


gif = VerifyGif()
a = gif('Mn3y')
a.save_file()