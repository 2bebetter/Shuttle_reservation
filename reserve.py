# -*- coding: utf-8 -*-
# @Date    : 2021/3/25
# @Author  : wmh

import configparser
import json
import requests
import datetime

import login

from login import LoginBcyy
from crypto import DataCrypt

class UcasBcyy():
    def __init__(self, weeks, start_time, goods):
        self.session = requests.session()
        self.headers = None
        self.url = None
        self.post_data = None
        self.token = None
        self.weeks = weeks
        self.start_time = start_time
        self.goods = goods
        self._init_session()

    def _init_session(self):
        self.username, self.password = self.read_username_and_password()
        l = LoginBcyy(self.username, self.password).login_Bcyy()
        self.token = l.token
        self.session = l.session
        self.headers = l.headers
        self.url = {
            'base_url': 'http://bcyy.iie.ac.cn/',
            'dataforward_url': "http://bcyy.iie.ac.cn/dataForward"
        }

    def read_username_and_password(self):
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        username = password = None
        if config.get('user', 'username'):
            username = config.get('user', 'username')
        if config.get('user', 'password'):
            password = config.get('user', 'password')
        return username, password

    def reserve_now(self, selldate):
        data_crypt = DataCrypt()
        datastr = '{"selldate":"'+selldate+'","enddate":"'+selldate+'","method":"/mobile/home/queryHomeGoods"}'
        self.post_data = {
            "item": data_crypt.encrypt(datastr)
        }
        self.headers = {
            "Content-Type": "application/json",
            #"Host": "bcyy.iie.ac.cn",
            #"Connection": "keep-alive",
            #"Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
            "X-Token": data_crypt.encrypt(self.token),
            "Accept": "*/*",
            #"Accept-Encoding": "gzip, deflate",
            #"Accept-Language": "zh-CN,zh;q=0.9",
        }
        response = self.session.post(url=self.url['dataforward_url'], headers=self.headers, data=json.dumps(self.post_data))
        if response.status_code == 200:
            infos = json.loads(response.text).get("data")
            info = list(filter(lambda i: i['goodsdetail']==self.goods and i['selldate']==selldate and i['starttime']==self.start_time, infos))[0]
            info["method"] = "/mobile/pay/toPaySelf"
            self.post_data = {
                "item": data_crypt.encrypt(str(info))
            }
            response = self.session.post(url=self.url['dataforward_url'], headers=self.headers, data=json.dumps(self.post_data))
            if response.status_code == 200:
                code = json.loads(response.text).get("code")
                msg = json.loads(response.text).get("msg")
                if code == 200 and msg == "success":
                    print("Success! Date: ")
                    print(selldate, self.start_time)
                else:
                    print("Faild!", "code:", code, "error message:", msg)
        else:
            print("Failed to get shuttle info!")

    def reserve_shuttle(self):
        data_crypt = DataCrypt()
        datastr = '{"method":"/mobile/home/queryGoodsAuxDate"}'
        self.post_data = {
            "item": data_crypt.encrypt(datastr)
        }
        self.headers = {
            "Content-Type": "application/json",
            #"Host": "bcyy.iie.ac.cn",
            #"Connection": "keep-alive",
            #"Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
            "X-Token": data_crypt.encrypt(self.token),
            "Accept": "*/*",
            #"Accept-Encoding": "gzip, deflate",
            #"Accept-Language": "zh-CN,zh;q=0.9",
        }
        response = self.session.post(url=self.url['dataforward_url'], headers=self.headers, data=json.dumps(self.post_data))
        if response.status_code == 200:
            code = json.loads(response.text).get("code")
            if code == 50008:
                print("Login time out")
            else:
                selldatemin = json.loads(response.text).get("data").get("selldatemin")
                selldatemax = json.loads(response.text).get("data").get("selldatemax")
                print("Time interval:", selldatemin, "---", selldatemax)

                date_obj = datetime.datetime.strptime(selldatemax, "%Y-%m-%d")
                week = int(datetime.datetime.strftime(date_obj, "%w"))
        
                if str(week) in set(self.weeks):
                    self.reserve_now(selldatemax)
                    print("reserve shuttle done")
        else:
            print("Failed to get time interval!")