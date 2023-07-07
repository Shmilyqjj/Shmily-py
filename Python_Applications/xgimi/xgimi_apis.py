#!/usr/bin/env python
# encoding: utf-8
"""
:Author: shmily
:Create Time: 2023/7/3 下午2:18
:@File: xgimi_apis.py
:@Software: PyCharm
:@Site: shmily-qjj.top
"""

# pip install asyncudp asyncio
# Reference from https://github.com/manymuch/Xgimi-4-Home-Assistant.git

import asyncudp
import asyncio
import sys

MY_GIMI_LOCAL_IP="192.168.8.179"
COMMAND_PORT = 16735
ADVANCE_PORT = 16750
ALIVE_PORT = 554
command_dict = {
            "ok": "KEYPRESSES:49",
            "play": "KEYPRESSES:49",
            "pause": "KEYPRESSES:49",
            "power": "KEYPRESSES:116",
            "back": "KEYPRESSES:48",
            "home": "KEYPRESSES:35",
            "menu": "KEYPRESSES:139",
            "right": "KEYPRESSES:37",
            "left": "KEYPRESSES:50",
            "up": "KEYPRESSES:36",
            "down": "KEYPRESSES:38",
            "volumedown": "KEYPRESSES:114",
            "volumeup": "KEYPRESSES:115",
            "poweroff": "KEYPRESSES:30",
            "volumemute": "KEYPRESSES:113",
        }

opr = ""
if len(sys.argv) == 1:
    raise Exception(f"No arg.Available args:{command_dict.keys()}")
else:
    opr = sys.argv[1]
if opr == "":
    raise Exception(f"Arg is null.Available args:{command_dict.keys()}")
opr = opr.lower()
msg = command_dict.get(opr)
if msg is None:
    raise NameError("Arg is not supported.")
remote_addr = (MY_GIMI_LOCAL_IP, COMMAND_PORT)


async def send():
    sock = (await asyncudp.create_socket(remote_addr=remote_addr))
    sock.sendto(msg.encode("utf-8"))
asyncio.run(send())
