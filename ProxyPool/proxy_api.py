'''
对外提供接口，目前只准备进行简单开发，接口够用就好
'''
from random import choice
from proxies import *

def proxy():
    if PROXY_LIST:
        c = list(set(PROXY_LIST))
        # 随机返回一个ip
        return choice(c)
    else:
        return None
