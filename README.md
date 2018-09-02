# ProxyPool
免费IP代理池。本着便于使用、最少依赖库。没有使用Redis或MongoDB，ip数据在变量中保存。

还不知道什么时候能完成，先就此挖个坑吧，一周内

### 大致思路：
- `get_proxy.py`文件获取新的代理ip 
- `while_verify.py`文件循环验证新获得的和已验证过的代理ip 
- `proxies.py`文件中存放新获得的和已验证过的代理ip。（数据交互中心） 
- `proxy_api.py`文件主要对外实现接口

### 使用方法(暂定)
运行`ProxyPool/main.py`文件

在你的spider文件中使用
```python
# 导入时请确认proxy_api的实际位置
from proxy_api import proxy

def get_page():
    ip = proxy()
    proxies = {'https': 'https://{}'.format(ip), 'http': 'http://{}'.format(ip)}
    r = requests.get(url, proxies=proxies)
    ...
```

### TODO
- [] 持续循环验证现有和新获得的代理ip
- [] 添加更多的免费代理ip网站
- [] 多样化api接口
