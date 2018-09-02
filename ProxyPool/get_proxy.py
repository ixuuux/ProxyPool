'''
用来从网络获取免费的代理ip
'''

import re
from lxml import etree
import requests
import logging
import proxies
logging.captureWarnings(True)

max_req = 1  # 最大重试次数
class GetHtml(object):
    # 自己写的一个http类，如果不喜欢可以重写或另写，返回只能两种情况，状态码为200的response，其他情况返回False或None
    num = 0
    header = {
       'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36"
            }
    def get_one_page(self, url, headers=header, proxies=None, timeout=5):
        if self.num < max_req:
            try:
                response = requests.get(url=url, headers=headers, timeout=timeout, verify=False, proxies=proxies)
                if response.status_code == 200:
                    self.num = 0
                    return response
                return None
            except TimeoutError:
                self.num += 1
                time.sleep(self.num)
                return self.get_one_page(url=url, timeout=timeout * self.num)
            except Exception:
                self.num += 1
                time.sleep(self.num)
                return self.get_one_page(url=url, timeout=timeout * self.num)
        return False
       
       
class GetProxy(object):
    '''
    从网络获取免费代理ip的类。获得的结果统一使用PROXY_LIST.append(ip)添加到PROXY_LIST变量中。
    PROXY_LIST在proxies.py文件中
    '''
    def __init__(self):
        self.get = GetHtml()
        self.page = 2
        
    def get_1(self):
        pass
        
    def get_2(self):
        pass
