# coding: utf8

"""
   简单的过滤日志
"""

import subprocess as sub

import redis
import gevent
import time
import json

from util.common import send_mail


class LogParser:
    def __init__(self, config):
        self.redis = redis.Redis(config['redis_host'], config['redis_port'])
        self.log = config['log_path']

    def do_parse_log(self):
        cmd = '/bin/grep -n "lua call" %s' % self.log
        print("grep cmd: %s" % cmd)
        ret = sub.Popen(cmd, shell=True, stdout=sub.PIPE).stdout.read()
        if ret == '':
            return
        s = [i for i in ret.split('\n') if len(i) > 0]
        l, c = s[-1].split(':', 1)
        to_handle = False
        # 校对数据
        ot = self.redis.hgetall('traceback-log')
        if ot:
            if l != ot['line']:
                t_now = int(time.time())
                if t_now - ot['time'] > 7200:
                    to_handle = True
        else:
            to_handle = True
        if to_handle:
            self.redis.hmset('traceback-log', {'line': l, 'error': c, 'time': int(time.time())})
            send_mail(json.dumps({'line': l, 'error': c}))


def run():
    loop = gevent.get_hub().loop
    t = loop.timer(0.0, 30)
    l = LogParser({
        'redis_host': "127.0.0.1",
        'redis_port': 6379,
        'log_path': 'data/gameserver-stdout---supervisor-RPLVwW.log.1'
    })
    t.start(l.do_parse_log)
    loop.run()
