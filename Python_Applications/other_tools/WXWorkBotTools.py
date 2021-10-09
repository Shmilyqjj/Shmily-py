#!/usr/bin/python3
# encoding: utf-8
"""
:Description: 企业微信机器人 工具
:Author: Shmily
:Create Time: 2021/10/9 10:47
:File: WXWorkBotTools.py
:Site: shmily-qjj.top
"""

import requests
import hashlib
import base64

KEY = "xawdawdadawdawdawdawda"
HOOK = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={KEY}"
FILES_TEMP = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={KEY}&type=file"
HEADERS = {'Content-Type': 'application/json'}


def send_words(words):
    """
    curl 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxxxx' \
   -H 'Content-Type: application/json' \
   -d '
   {
        "msgtype": "text",
        "text": {
            "content": "兄弟们，干饭啦 @所有人"
        }
   }'
    :param words:
    :return:
    """
    data = """
    {
        "msgtype": "text",
        "text": {
            "content": "%s"
        }
   }
    """ % words
    data = str(data).encode("utf-8")
    print(requests.post(url=HOOK, headers=HEADERS, data=data).json())


def send_pics(pic_path):
    img = open(pic_path, 'rb').read()
    b = str(base64.b64encode(img), encoding='utf-8')
    my_md5 = hashlib.md5()
    my_md5.update(base64.b64decode(b))
    m = my_md5.hexdigest()
    data = {"msgtype": "image", "image": {"base64": b, "md5": m}}
    print(data)
    print(requests.post(url=HOOK, headers=HEADERS, json=data).json())


def send_file(file_path):
    mess = requests.post(url=FILES_TEMP, files={'media': open(file_path, 'rb')})
    media_id = mess.json()['media_id']
    data = {"msgtype": "file", "file": {"media_id": media_id}}
    print(requests.post(url=HOOK, headers=HEADERS, json=data).json())

# send_words("兄弟们，干饭了🍚 @所有人")
# send_pics("C://Users//q00885//Downloads//大恶人.png")
# send_file("C://Users//q00885//Sync-win//ide-eval-resetter-2.1.6.zip")

