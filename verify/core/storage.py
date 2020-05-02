#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
__author__ = "monkey"

from abc import ABCMeta, abstractmethod
import time
import os
from io import BytesIO
import random
from PIL.Image import Image


from ..config import config
from ..core.errors import StoragePathError, StoragePermissionError


class AbstractStorage(metaclass=ABCMeta):

    @abstractmethod
    def bytes_instance(self, instance: list) -> 'BytesIO':
        """ bytes format instance """

    @abstractmethod
    def save_file(self) -> tuple:
        """ save verify to file system. """

    @abstractmethod
    def get_binary(self) -> bytes:
        """ Get the binary type verify. """

    class _meta:  # FIXME check the meta subclass attribute before running.
        extend_name = None


class StorageCommonMixin(object):
    """ Include some common methods and rely method. """

    def __init__(self, instance: list, string: str, *args, **kwargs) -> None:
        """
        Get verify object, transform to binary object.
        :param instance: verify object
        :param string: verify chars
        """
        self.string = string
        self.instance = self.bytes_instance(instance)

    def asset_file(self, path: str = None, filename: str = None) -> tuple:
        """ Check storage path (config.STORAGE_DIR)is valid <It's exist & writable> """

        path = path or config.STORAGE_DIR
        # Make sure the file exists and has write permission.

        if not os.path.isdir(path):
            try:
                os.mkdir(path)   # create the default dir.
            except FileNotFoundError:
                raise StoragePathError(path)
        # check permission.
        if not os.access(path, os.W_OK):
            raise StoragePermissionError(path)

        # create a unique file name.
        filename = filename or 'Verify%s.%s' % (str(time.time())[11:], self._meta.extend_name)

        file = os.path.join(path, filename)
        # Make sure there are no files with the same name in the storage directory.
        while True:
            # if the filename is existed, add a random char in the filename head.
            if os.path.exists(file):
                filename = random.choice(config.VERIFY_CODE_SET) + filename
            else:
                file = os.path.join(path, filename)
                break
        return file, filename  # file: path + filename

    def save_file(self, path: str = None, filename: str = None, *args, **kwargs) -> tuple:
        """ Save the verify to file system. """

        file, filename = self.asset_file(path=path, filename=filename)

        verify = self.instance.read()  # get filename binary data.

        with open(file, 'wb') as f:
            f.write(verify)

        return file, filename  #

    def get_binary(self, **kwargs) -> bytes:
        """ Get the verify format binary. """

        img_bytes = self.instance.read()
        return img_bytes  # binary object of verify.


class GifStorage(StorageCommonMixin, AbstractStorage):
    """ GifVerify storage class. """

    def bytes_instance(self, instance: list, **kwargs) -> BytesIO:
        """
        Accept a list of `PIL.Image.Image`
        :param instance: Verify list object
        :return: BytesIO object include verify format bytes
        """

        temp = BytesIO()  # get memory-file object.
        instance[0].save(temp, save_all=True, append_images=instance, duration=1, format='GIF')
        temp.seek(0)
        return temp

    class _meta:
        extend_name = 'gif'


class PngStorage(StorageCommonMixin, AbstractStorage):
    """
    Accept a `PIL.Image.Image` object.
    :return BytesIO object include verify format bytes
    """

    def bytes_instance(self, instance: 'Image') -> BytesIO:

        temp = BytesIO()

        if instance and isinstance(instance, Image):
            instance.save(temp, self._meta.extend_name)
            temp.seek(0)
        else:
            raise Exception('`%s` should be a instance of `PIL.Image.Image` not a %s' % (instance, instance.__class__))

        return temp

    class _meta:
        extend_name = 'png'
