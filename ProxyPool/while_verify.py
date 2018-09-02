'''
循环验证已有和新获得的代理ip
留下可用的，剔除不可用的
'''
import threading
import time
import random
import grequests

def t_verify_ok_proxies():
    # 多线程验证ip可用性，依附于verify_ok_proxies()
    pass

def verify_ok_proxies():
    # 对已验证过的ip进行循环验证，间隔config.OK_IP_VERIFY_TIME秒
    # TODO
    pass


def verify_proxies():
    # 对新获得的ip进行验证
    pass
