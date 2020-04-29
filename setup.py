#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
__author__ = "monkey"

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='verify-python',
      version='0.1',
      description='An elegant verification code generator.',
      author='BlackMonkey',
      author_email='3213322480@qq.com',
      url='https://github.com/blackmonkey121/verify',
      packages=find_packages(),
      long_description=long_description,
      long_description_content_type="text/markdown",
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent"],
      python_requires='>=3.3',
      )
