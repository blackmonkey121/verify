#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
__author__ = "monkey"

from abc import ABCMeta, abstractmethod
import time
import os
from io import BytesIO
import random
# from pymysql import connect

from ..config import config
from ..core.errors import StoragePathError, StoragePermissionError


class AbstractStorage(metaclass=ABCMeta):

    @abstractmethod
    def bytes_instance(self, instance, string):
        """ bytes format instance """

    @abstractmethod
    def save_file(self):
        """ save verify to file system. """

    @abstractmethod
    def save_db(self):
        """ save verify to database. """

    @abstractmethod
    def get_binary(self):
        """ Get the binary type verify. """

    class _meta:    # FIXME check the meta subclass attribute before running.
        extend_name = None


class StorageCommonMixin(object):
    """ Include some common methods. """
    def __init__(self, instance, string, *args, **kwargs):
        """
        Get verify object, transform to binary object.
        :param instance: verify object
        :param string: verify chars
        """
        self.string = string
        self.instance = self.bytes_instance(instance)

    def asset_file(self, path=None, filename=None):
        """ Check storage path (config.STORAGE_DIR)is valid <It's exist & writable> """

        path = path or config.STORAGE_DIR
        # Make sure the file exists and has write permission.
        if not os.path.isdir(path):
            raise StoragePathError(path)

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
        return file, filename   # file: path + filename

    def save_file(self, path=None, filename=None, *args, **kwargs):
        """ Save the verify to file system. """

        file, filename = self.asset_file(path=path, filename=filename)

        verify = self.instance.read()   # get filename binary data.

        with open(file, 'wb') as f:
            f.write(verify)

        return file, filename   #

    def get_binary(self, **kwargs):
        """ Get the verify format binary. """

        img_bytes = self.instance.read()

        return img_bytes    # binary object of verify.

    # def get_db_connection(self):
    #     """ Get database connection. """
        # db_dict = config.DATABASE
        # if db_dict:
        #     try:
        #         conn = connect(**db_dict)
        #     except Exception as e:
        #         raise DataBaseConfigError('Your `config.DATABASE` have some error(s).')
        #     return conn.cursor()
        #
        # else:
        #     raise DataBaseNotConfigError('If you use %s.save_db() method, you must config `DATABASE` \n'
        #                                  'in your config.py or param:config' % (self.__class__.__name__))

    def save_db(self):
        """ Save format binary verify object into MySQL. """
        return False
        # create_table_sql = """
        #  CREATE TABLE {} (
        #  id INT auto_increment PRIMARY KEY ,
        #  verify_code CHAR(10) NOT NULL UNIQUE,
        #  context BINARY NOT NULL,
        #  )ENGINE=innodb;
        #  """.format(self._meta.table_name)
        #
        # create_record_sql = """
        #  INSERT INTO {}(VERIFY_CODE,CONTEXT)
        # VALUES ('%s', '%s')"
        #  """ .format(self._meta.table_name)
        #
        # cursor = self.get_db_connection()
        #
        # try:
        #     cursor.execute(create_record_sql, (self.string, self.instance))
        # except Exception as e:
        #     print(e)
        #     try:
        #         cursor.execute(create_table_sql)
        #     except Exception as e_msg:
        #         print(e_msg)


class GifStorage(StorageCommonMixin, AbstractStorage):
    """ GifVerify storage class. """

    def bytes_instance(self, instance: list, **kwargs):
        """
        Accept a list of `PIL.Image.Image`
        :param instance: Verify list object
        :return: BytesIO object include verify format bytes
        """

        temp = BytesIO()   # get memory-file object.
        instance[0].save(temp, save_all=True, append_images=instance, duration=1, format='GIF')
        temp.seek(0)
        return temp

    class _meta:
        extend_name = 'gif'
        table_name = 'GIF'


class PngStorage(StorageCommonMixin, AbstractStorage):
    """ developing ..."""

