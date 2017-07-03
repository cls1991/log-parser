# coding: utf8

import os
# 切换工作目录到项目根目录
project = os.path.split(os.path.realpath(__file__))[0]
os.chdir(project)

from util.common import send_mail

if __name__ == '__main__':
    send_mail("card game traceback")
