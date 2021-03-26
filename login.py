# -*- coding: utf-8 -*-
# @Date    : 2021/3/25
# @Author  : wmh
import codecs
import configparser
import json
import os
import time
from sys import exit
import requests

from crypto import DataCrypt

class UserNameOrPasswordError(Exception):
    pass

class LoginBcyy(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.cnt = 0
        self.__BEAUTIFULSOUPPARSE = 'html5lib'  # or use 'lxml'
        self.session = requests.session()
        self.token = None
        self._login_init()

    def _login_init(self):
        self.url = {
            'base_url': 'http://bcyy.iie.ac.cn/',
            'login_url': 'http://bcyy.iie.ac.cn/dataForward'
        }
        self.headers = {
            "Content-Type": "application/json",
            #"Host": "bcyy.iie.ac.cn",
            #"Connection": "keep-alive",
            #"Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
            "X-Token": None,
            "Accept": "*/*",
            #"Accept-Encoding": "gzip, deflate",
            #"Accept-Language": "zh-CN,zh;q=0.9",
        }
        self.post_data = {
            # how to calculate item
            "item": None
            #"idserial":idserial,
            #"password":password,
        }

    def login_Bcyy(self):
        r = self.session.get(url=self.url['base_url'])
        if r.status_code == 200:
            print('Access to Welcome page!')
        else:
            print('Failed to Welcome page!')
        data_crypt = DataCrypt()
        datastr = '{"idserial":"'+self.username+'","password":"'+self.password+'","method":"/mobile/login/userLoginCheck"}'
        self.post_data = {
            "item": data_crypt.encrypt(datastr)
        }
        response = self.session.post(url=self.url['login_url'], headers=self.headers, data=json.dumps(self.post_data))
        if response.status_code == 200:
            code = json.loads(response.text).get("code")
            if code == 500:
                print("Account cann't match password!")
            else:
                token = json.loads(response.text).get("data").get("token")
                print("token:"+token)
                self.token = token
        return self