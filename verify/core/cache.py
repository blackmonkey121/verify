#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

import contextlib
import time
from abc import ABCMeta, abstractmethod
from collections import OrderedDict
from threading import Lock

lock = Lock()


@contextlib.contextmanager   # register context manager.
def my_lock(**kwargs):
    lock.acquire()
    try:
        yield lock
    except Exception as exc:
        """deal with exception"""
    finally:
        lock.release()
        return


class AbstractCache(metaclass=ABCMeta):

    @abstractmethod
    def get(self, k, v):
        """  """

    @abstractmethod
    def set(self, k, v):
        """  """

    @abstractmethod
    def clear(self):
        """  """


class Cache(object):
    """ This is a thread-safe cache instance. """
    __cur = lambda self: int(time.time())

    def __init__(self, contain=1024, expiration=60 * 60 * 24, *args, **kwargs):
        """

        :param contain: The max number of cache storage elements
        :param expiration: elements time out
        """

        self.contain = contain
        self.expiration = expiration

        self._cache = {}
        self._visit_records = OrderedDict()  # record visit time
        self._expire_records = OrderedDict()  # record expire time

    def __setitem__(self, k, v):

        current = self.__cur()
        self.__delete__(k)
        with my_lock():
            self._cache[k] = v
        self._expire_records[k] = current + self.expiration
        self._visit_records[k] = current

        self.clear()

    def __getitem__(self, k):

        current = self.__cur()
        del self._visit_records[k]
        self._visit_records[k] = current
        self.clear()
        with my_lock():
            ret = self._cache[k]

        return ret

    def __contains__(self, k):

        self.clear()
        return k in self._cache

    def __delete__(self, k):
        if k in self._cache:
            del self._cache[k]
            del self._expire_records[k]
            del self._visit_records[k]

    def clear(self):
        """ achieve clear method """
        if self.expiration is None:
            return None
        delete_key = []
        current = self.__cur()

        for k, v in self._expire_records.items():
            if v < current:
                delete_key.append(k)

        [self.__delete__(del_k) for del_k in delete_key]

        while self._cache.__len__() > self.contain:
            for k in self._visit_records:
                self.__delete__(k)
                break

    def get(self, k, v=None):
        """ achieve get method """
        try:
            ret = self.__getitem__(k)
        except KeyError:
            return v
        return ret

    def set(self, k, v):
        """ achieve set method """
        self.__setitem__(k, v)


cache = Cache(contain=1024, expiration=60 * 60)    # default timeout : one hour


if __name__ == "__main__":
    cache = Cache()

    cache.set('name', 'monkey', )

    print(cache.get('name'))

    print(cache.get('gender'))