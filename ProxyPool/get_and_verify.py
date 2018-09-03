'''
用来从网络获取免费的代理ip
对新获得ip和已有验证ip进行验证
'''

import re
import threading
import requests
import grequests
import logging
import proxies
import config
import time
from flask import Flask

app = Flask(__name__)
logging.captureWarnings(True)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

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
       
PROXY_LIST = []
OK_PROXY = []
class GetProxy(object):
    '''
    从网络获取免费代理ip的类。获得的ip统一PROXY_LIST.append(ip)添加到PROXY_LIST变量中。
    '''
    def __init__(self):
        self.get = GetHtml()
        self.page = 5
        
    def get_1(self):
        for page in range(1, self.page):
        url = 'http://ip.jiangxianli.com/?page={}'.format(page)
        html = self.get.get_one_page(url)
        if html:
            ips = re.findall('(\d{2,3}([.]\d{1,3}){3}:\d{2,5})', html.text, re.S)
            if len(ips) > 0:
                for ip in set(ips):
                    if ip not in PROXY_LIST:
                        PROXY_LIST.append(ip[0])
                        # print(PROXY_LIST)
        else:
            break
        
    def get_2(self):
        pass
    
    
    class VerifyProxy(object):
        def t_verify_ok_proxies(self, ip, verify_url=config.VERIFY_ADDRESS):
            try:
                proxies = {'http': 'http://{}'.format(ip), 'https': 'https://{}'.format(ip)}
                r = requests.get(random.choice(verify_url), headers=config.HEADERS, proxies=proxies, verify=False,
                                 timeout=config.TIMEOUT)
                if r.status_code == 200:
                    return
                else:
                    OK_PROXY.remove(ip)
            except:
                try:
                    OK_PROXY.remove(ip)
                except:
                    pass
        def verify_ok_proxies(self):
            while True:
                if OK_PROXY:
                    logging.info("正在对现有ip进行再次验证(thread)....现有{}个".format(len(OK_PROXY)))
                    # 对已验证过的ip进行循环验证，间隔config.OK_IP_VERIFY_TIME秒
                    for ip in OK_PROXY:
                        t1 = threading.Thread(target=self.t_verify_ok_proxies, args=(ip,))
                        t1.start()
                    time.sleep(config.OK_IP_VERIFY_TIME)
                else:
                    time.sleep(2)
        def verify_proxies(self, verify_url=config.VERIFY_ADDRESS):
            while True:
                if PROXY_LIST:
                    try:
                        L = PROXY_LIST
                        for u in L:
                            PROXY_LIST.remove(u)
                        logging.info("正在对新获得ip进行验证....共{}个".format(len(set(L))))
                        reqs = []
                        for i in set(L):
                            if i in OK_PROXY:
                                continue
                            else:
                                proxies = {"http": 'http://{}'.format(i), "https": 'https://{}'.format(i)}
                                reqs.append(grequests.get(random.choice(verify_url), headers=config.HEADERS, proxies=proxies,
                                                      verify=False, timeout=config.TIMEOUT))
                            resps = grequests.map(reqs)
                            num = 0
                            for j, ii in enumerate(resps):
                                if ii is not None and ii.status_code == 200:
                                    num += 1
                                    OK_PROXY.append(L[j])
                            L.clear()
                            logging.info("新获得ip验证结束....有效{}个".format(num))
                            # print(OK_PROXY)
                        except:
                            time.sleep(3)
                        if len(OK_PROXY) < 10:
                            time.sleep(3)
                        else:
                            time.sleep(10)
                    else:
                        time.sleep(2)

@app.route("/get")
def index():
    if len(OK_PROXY) > 0:
        ip = random.choice(OK_PROXY)
        return ip
    return 'no proxy'
@app.route("/count")
def count():
    return '{}'.format(len(OK_PROXY))
@app.route("/get_all")
def all():
    if OK_PROXY:
        return '<div>'+'<br>'.join(OK_PROXY)+'</div>'
    return 'no proxy'
def main():
    vp = VerifyProxy()
    t1 = threading.Thread(target=vp.verify_proxies)
    t1.start()
    t2 = threading.Thread(target=vp.verify_ok_proxies)
    t2.start()
    while True:
        if not PROXY_LIST:
            get = GetProxy()
            get.get_1()
        else:
            time.sleep(2)

if __name__ == '__main__':
    t1 = threading.Thread(target=main)
    t1.start()
    app.run()
