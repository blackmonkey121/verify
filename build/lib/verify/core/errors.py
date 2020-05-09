#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"


class Error(Exception):
    """ Verify errors class base. """


class ConfigNotExist(Error):
    """ Config not exist error. """

    def __init__(self, key):
        self.key = key

    def __str__(self):
        return "(The `%s` attribute was not found in the `Config` instance.\n" \
               "Lowercase variables are not collected by config.)" % self.key


class ConfigFileNotFoundError(Error):
    """ Config file not found . """

    def __init__(self, fname):
        self.fname = fname

    def __str__(self):
        return "(The `%s.py` file not found in your project.)" % self.fname


class SubclassError(Error):
    """ Subclass constraint error. """

    cls: str = ''

    def __init__(self, sub_cls):
        self.sub_cls = sub_cls

    def __str__(self):
        return '`%s` must be subclass `%s`.' % (self.sub_cls, self.__class__.cls)


class ConfigError(SubclassError):
    cls = 'Config'


class FilterError(SubclassError):
    cls = 'Filter'


class StyleError(SubclassError):
    cls = 'Style'


class StorageError(SubclassError):
    cls = 'Storage'


class BuilderError(SubclassError):
    cls = 'Builder'


class StoragePathError(Error):
    """ storage path is not exist error. """

    def __init__(self, path):
        self.path = path

    def __str__(self):
        return "(The Storage path: `%s`\n does not exist.)" % self.path


class StoragePermissionError(Error):
    """No write permission Error """

    def __int__(self, path):
        self.path = path

    def __str__(self):
        return "(No write permission for %s .)" % self.path


class SecretKeyError(Error):
    """ SecretKeyError is not null! """


class SafeEngineError(Error):
    """ SafeEngineError is not existed! """

    def __init__(self, safe):
        self.safe = safe

    def __str__(self):
        return '`%s` SafeEngine is not existed!' % self.safe.upper()


class StringError(Error):

    def __init__(self, string):
        self.string = string

    def __str__(self):
        return '(`%s` is must be string or int , is not `%s`)' % (self.string, type(self.string))


class CleanParaError(Error):
    def __init__(self, func):
        self.func = func

    def __str__(self):
        return "(The `%s` method does not accept any parameters)" % self.func
