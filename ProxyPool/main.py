'''
程序启动主入口
运行后会启动get_proxy.py和while_verify.py
'''

import while_verify
import get_proxy


if __name__ == '__main__':
    get_proxy.main()
    while_verify.main()
