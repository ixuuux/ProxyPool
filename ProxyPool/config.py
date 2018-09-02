'''
配置文件

以下暂定 2018-9-2
'''


# ip验证地址（需列表，并从中随机选取地址进行验证）
VERIFY_ADDRESS = [
    # 'http://httpbin.org/ip',
    'https://news.163.com/',
    'https://news.qq.com/',
    'https://news.sina.com.cn/']
    
# 对已验证过的ip重复验证时间间隔
OK_IP_VERIFY_TIME = 3*60


# 请求头
HEADERS = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36"}

# 请求超时
TIMEOUT = 10
