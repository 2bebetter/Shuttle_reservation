# -*- coding: utf-8 -*-
# @Date    : 2021/3/25
# @Author  : wmh

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import algorithms
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import json

#AES/ECB/PKCS7Padding encrypt decrypt
#pip3 install pycryptodome


key = '0102030405060708'
iv = '0102030405060708'
mode = AES.MODE_CBC

class DataCrypt(object):

    def __init__(self):
        self.key = key.encode('utf-8')
        self.mode = AES.MODE_CBC
        self.iv = iv.encode('utf-8')
        # block_size 128bit

    # fill text with blank, n*16bit
    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.iv)
        text = text.encode('utf-8')

        # key's length must statisfy 16 (AES-128), 24 (AES-192). or 32 (AES-256) Bytes
        # using AES-128

        text=self.pkcs7_padding(text)

        self.ciphertext = cryptor.encrypt(text)

        # Observe the encryption and decryption mode of the website
        # function c(e) {
        #     var n = o.enc.Utf8.parse(e)
        #       , t = o.AES.encrypt(n, r, {
        #         iv: i,
        #         mode: o.mode.CBC,
        #         padding: o.pad.Pkcs7
        #     });
        #     return t.ciphertext.toString().toUpperCase()
        return b2a_hex(self.ciphertext).decode().upper()

    @staticmethod
    def pkcs7_padding(data):
        if not isinstance(data, bytes):
            data = data.encode()

        padder = padding.PKCS7(algorithms.AES.block_size).padder()

        padded_data = padder.update(data) + padder.finalize()

        return padded_data

    @staticmethod
    def pkcs7_unpadding(padded_data):
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        data = unpadder.update(padded_data)

        try:
            uppadded_data = data + unpadder.finalize()
        except ValueError:
            raise Exception('Invaild!')
        else:
            return uppadded_data

    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.iv)
        plain_text = cryptor.decrypt(a2b_hex(text))
        plain_text = self.pkcs7_unpadding(plain_text)

        # Observe the encryption and decryption mode of the website
        # var o = t("4e10")
        #   , r = o.enc.Utf8.parse("0102030405060708")
        #   , i = o.enc.Utf8.parse("0102030405060708");
        # function a(e) {
        #     var n = o.enc.Hex.parse(e)
        #       , t = o.enc.Base64.stringify(n)
        #       , a = o.AES.decrypt(t, r, {
        #         iv: i,
        #         mode: o.mode.CBC,
        #         padding: o.pad.Pkcs7
        #     })
        #       , c = a.toString(o.enc.Utf8);
        #     return c.toString()
        # }
        return plain_text

if __name__ == '__main__':
    data_crypt = DataCrypt()
    
    ciphertext = "94CBAC47B5EEB4BD7FA78938E3AF0DF48E9FFBCF7747B9FBE4704A439EF69BB5DC813B68C1D6EBE780A421C35851D85E"
    print(data_crypt.decrypt(ciphertext))

    ciphertext = "41F17A72A96C0A27478B8BF22A1E82C0A308F52D7EE135529D83ADEEB27ADD62AE38F864A64A3FAE185DC9B0545E6BC90BDB2B07309A4B330771B2C20BF8DAE579E42C6645362B4CB36D2DC657D2531F0FAD47D81E303623B3535F25A58C2A38"
    print(data_crypt.decrypt(ciphertext))