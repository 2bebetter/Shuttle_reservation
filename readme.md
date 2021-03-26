# Readme

For UCAS IIE's Bcyy

给国科大信工所写的班车预约系统= =

## Requirements

Python 3.6.9 

Linux

## For use

```bash
$ pip3 install virtualenv
$ virtualenv resenv --python=python3.6
$ source resenv/bin/activate
$ pip install -r requirements.txt -i https://pypi.douban.com/simple
$ nohup python ./reserve_timer.py &
```

## 文件说明



├─Shuttle_reservation
│      config.ini 配置文件，主要是你的证件号和密码，默认密码为111111
│      crypto.py 加解密功能
│      login.py 登录
│      readme.md
│      requirements.txt
│      reserve.py 预约班车
│      reserve_timer.py 定期触发班车预约功能

