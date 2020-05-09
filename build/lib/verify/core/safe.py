#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

import rsa
import json
import base64
from abc import ABCMeta, abstractmethod

from .errors import SecretKeyError, SafeEngineError, StringError
from .verify import StringMixin
from ..config import config
from .cache import cache, Cache
import itsdangerous


class SafeEngine(metaclass=ABCMeta):

    @abstractmethod
    def encrypt(self, info: str) -> str:
        """
        Encrypt the plain text. `str` -> `str`.
        :param info: will encrypt str
        :return:Encrypted secret
        """

    @abstractmethod
    def decrypt(self, info_encrypted: str) -> str:
        """
        Decrypt the encrypted data，`str` -> `str`
        :param info_encrypted:encrypted string.
        :return:decrypted string.
        """

    @abstractmethod
    def get_key(self) -> dict:
        """ get key """


class AbstractSafe(metaclass=ABCMeta):

    @abstractmethod
    def coding(self, string: str = None, method: str = 'RSA', verify_type: str = 'gif') -> str:
        """
        After RSA encryption of str, json serialize the dictionary src to convert the serialized json string to
        base64 encoding
        """

    @abstractmethod
    def parse(self, obj: str) -> dict:
        """ Disassemble the obj object and get the decrypted request dictionary """

    @abstractmethod
    def update_key(self, method: str, *args, **kwargs) -> None:
        """ Update key ."""

    @abstractmethod
    def tell_key(self, method: str) -> str:
        """ Get key ."""

    @abstractmethod
    def create_string(self) -> str:
        """ create a random string. """


class RsaEngine(SafeEngine):
    """ RSA encryption and decryption """

    def __init__(self, number: int, pub_path: str = None, priv_path: str = None, cache: 'Cache' = cache) -> None:
        # def __init__(self, number, pub_path='public_key.pem', priv_path='private_key.pem'):
        """

        :param pub_path: the path to public key, default its path is public_key.pem
        :param priv_path: the path to private key, default its path is private_key.pem
        """
        # Generate the public and private keys, and returns them

        self.cache = cache

        if not all((pub_path, priv_path)):  # get the keys filename <*.pem>
            pub_path = 'public_key.pem'
            priv_path = 'private_key.pem'

        from os import path, mkdir
        folder = config.RSA_KEY_DIR  # Get the storage address of the key
        self.public_key_path = path.join(folder, pub_path)  # Splice key address and file name
        self.private_key_path = path.join(folder, priv_path)

        if not path.isdir(folder):  # Check if this address exists
            mkdir(folder)  # Make the dir if it is not existed.
            self.update_key(number)

        elif not all((path.isfile(self.public_key_path), path.isfile(self.private_key_path))):
            self.update_key(number)

        else:
            pub = open(self.public_key_path, 'rb')
            self.pub = pub.read()
            pub.close()

            pri = open(self.private_key_path, 'rb')
            self.pri = pri.read()
            pri.close()

    def update_key(self, number: int) -> None:
        """ Update or Create key """
        pub_key, pri_key = rsa.newkeys(number)

        self.pub = pub_key.save_pkcs1('PEM')
        self.pri = pri_key.save_pkcs1('PEM')

        with open(self.public_key_path, mode='wb') as f_pub:
            f_pub.write(self.pub)

        with open(self.private_key_path, mode='wb') as f_pri:
            f_pri.write(self.pri)

        self.cache.set('pri_key', self.pri)
        self.cache.set('pub_key', self.pub)

    def encrypt(self, info: str) -> str:
        """
        encrypt information
        :param info: the original string information to be encrypted
        :return:info_encrypted str
        """
        # read the public key from the file
        pub = cache.get('pub_key', None)
        if not pub:
            with open(self.public_key_path, mode='rb') as f:
                pub = f.read()

        public_key = rsa.PublicKey.load_pkcs1(pub)

        # use the public key to encrypt the content, which must be binary
        info_encrypted = rsa.encrypt(info.encode('ISO-8859-1'), public_key)
        return info_encrypted.decode('ISO-8859-1')

    def decrypt(self, info_encrypted: str) -> str:
        """
        decrypt information
        :param info_encrypted: encrypted information
        :return: info
        """
        info_encrypted = info_encrypted.encode('ISO-8859-1')
        pri = cache.get('pri_key')
        if not pri:
            # read the private key from the file
            with open(self.private_key_path, 'rb') as f:
                pri = f.read()
                # convert pri to original state
        private_key = rsa.PrivateKey.load_pkcs1(pri)

        # decrypt with private key to obtain the decrypted content
        msg = rsa.decrypt(info_encrypted, private_key)
        info = msg.decode('ISO-8859-1')  # decode
        return info

    def get_key(self) -> dict:
        return {'pub': self.pub, 'pri': self.pri}


class FastEngine(SafeEngine):
    """ Example based on improved AES encryption algorithm """

    def __init__(self, timeout: int) -> None:
        self.secret_key = config.SECRET_KEY
        self.timeout = timeout
        self.fast_instance = itsdangerous.TimedJSONWebSignatureSerializer(secret_key=self.secret_key,
                                                                          expires_in=self.timeout)

    def encrypt(self, info: str) -> str:
        ret = {'str': info}
        res = self.fast_instance.dumps(ret)
        token = res.decode('utf8')  # code method.
        return token

    def decrypt(self, info_encrypted: str) -> str:
        res = self.fast_instance.loads(info_encrypted)
        return res['str']

    def get_key(self) -> dict:
        return {'fast': self.secret_key}


class Safe(StringMixin, AbstractSafe):

    def __init__(self, number: int=512, cache: 'Cache'=cache) -> None:
        """
        Entrance to the security module.
        :param number: RSA key length
        :param cache: cache instance， must be provide three methods< get 、set、clear>
        """
        self._rsa = RsaEngine(number=number, cache=cache)
        self._fast = FastEngine(timeout=60 * 5)
        self._default = getattr(self, config.SAFE_ENGINE, self._rsa)
        self.cache = cache

    @staticmethod
    def _to_safe_string(obj: str) -> str:
        obj = base64.urlsafe_b64encode(obj.encode("ISO-8859-1"))  # bytes
        return obj.decode("ISO-8859-1")  # str

    @staticmethod
    def _to_safe_bytes(obj: str) -> bytes:
        obj = obj.encode('ISO-8859-1')  # str
        return base64.urlsafe_b64decode(obj).decode("ISO-8859-1")  # byte

    def coding(self, string: str = None, method: str = 'RSA', verify_type: str = 'gif') -> str:
        """
        After RSA encryption of str, json serialize the dictionary src to convert the serialized json
        string to base64 encoding
        """

        if string is None:
            string = self.create_string()

        if isinstance(string, (str, int)):
            string = str(string)
        else:
            raise StringError(string)

        if not isinstance(method, str):
            raise SafeEngineError(method)

        safe_instance = getattr(self, '_%s' % method.lower(), self._default)

        src = json.dumps({
            'str': safe_instance.encrypt(string),  # encrypted string
            'mtd': method,  # encryption method
            'vt': verify_type,  # Verification code type
        })
        return self._to_safe_string(json.dumps(src))

    def parse(self, obj: str) -> dict:
        """ Disassemble the obj object to get the decrypted request dictionary. """
        data = self._to_safe_bytes(obj)  # decode base64

        data = eval(json.loads(data))  # parse json

        method = data.get('mtd', 'RSA')  # get encrypt method.

        safe_instance = getattr(self, '_%s' % method.lower(), self._default)  # get decrypted object

        data['str'] = safe_instance.decrypt(data.get('str'))  # Get the decrypted dict

        return data

    def update_key(self, method: str, *args, **kwargs) -> None:
        """ Update the secret key. """
        if method.lower() == 'rsa':

            safe_instance = self._rsa
            number = kwargs.get('number', 512)
            safe_instance.update_key(number)

        elif method.lower() == 'fast':
            key = kwargs.get('key', None)
            if key is not None:
                config.SECRET_KEY = key
            else:
                raise SecretKeyError('Secret key is not null!')
        else:
            raise SafeEngineError(method)

    def tell_key(self, method: str) -> str:

        safe_instance = getattr(self, '_%s' % method.lower(), None)
        if safe_instance:
            return safe_instance.get_key()
        else:
            raise SafeEngineError(method)
