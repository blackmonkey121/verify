#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
__author__ = "monkey"

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='verify-python',
      version='0.0.2',
      description='An elegant verification code generator.',
      author='BlackMonkey',
      author_email='3213322480@qq.com',
      url='https://github.com/blackmonkey121/verify',
      packages=find_packages(),
      long_description=long_description,
      long_description_content_type="text/markdown",
      license="GPLv3",
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Operating System :: OS Independent"],

      python_requires='>=3.3',
      install_requires=[
          "itsdangerous>=1.1.0",
          "numpy>=1.11.3",
          "opencv-python>=3.4",
          "Pillow>=7.0",
          "rsa>=4.0", ]
      )
