# coding: utf8

import json
import time
import datetime
import sys

import requests

from share import const

mail_conf = json.load(open("conf/conf.json", "r"))


def time_now_str(format_str="%Y-%m-%d"):
    """
    获取当天时间
    :param format_str:
    :return:
    """
    return time.strftime(format_str, time.localtime())


def datetime_to_str(dt, format_str="%Y-%m-%d"):
    """
    datetime转换字符串
    :param format_str:
    :param dt:
    :return:
    """
    return dt.strftime(format_str)


def send_mail(traceback_data):
    """
    发送邮件通知
    :param traceback_data:
    :return:
    """
    receivers = mail_conf["mail_to"].split(";")
    request_date = datetime_to_str(datetime.datetime.now())
    request_date_list = list()
    traceback_data_list = list()
    nickname_list = list()
    for receiver in receivers:
        request_date_list.append(request_date)
        traceback_data_list.append(traceback_data)
        nickname_list.append(receiver.split("@")[0])
    # 发送邮件
    sub_vars = {
        'to': receivers,
        'sub': {
            "%nickname%": nickname_list,
            "%traceback_data%": traceback_data_list,
            "%send_date%": request_date_list
        }
    }
    params = {
        "api_user": const.SEND_CLOUD_API_USER,
        "api_key": const.SEND_CLOUD_API_KEY,
        "template_invoke_name": "cardgame_traceback_notify",
        "substitution_vars": json.dumps(sub_vars),
        "from": mail_conf["mail_from"],
        "resp_email_id": "true",
    }

    r = requests.post(const.SEND_CLOUD_API_URL, data=params)
    res = r.text
    if sys.version_info < (3, 0):
        res = res.encode("utf8")
    response = json.loads(res)
    if response['message'] == 'success':
        return True
    print('send_mail_fail:', r.text)
    return False
