# ProxyPool
免费IP代理池。本着便于使用、最少依赖库。没有使用Redis或MongoDB，ip数据在变量中保存。

还不知道什么时候能完成，先就此挖个坑吧

### 大致思路：
- `get_and_verify.py`包含获取新代理，验证新代理，验证已验证代理，调用接口

### 使用方法(暂定)
运行`ProxyPool/get_and_verify.py`文件

在你的spider文件中使用
```python
def get_page():
    ip = requests.get('http://127.0.0.1:5000/get').text
    proxies = {'https': 'https://{}'.format(ip), 'http': 'http://{}'.format(ip)}
    r = requests.get(url, proxies=proxies)
    ...
```
