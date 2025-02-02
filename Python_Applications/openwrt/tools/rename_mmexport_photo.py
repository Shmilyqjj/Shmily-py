#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import re
import time
from datetime import datetime
MIN_TIMESTAMP = 884793600


def gen_target_file_name(fn: str):
    match = re.search(r'\d{10,13}', fn)
    if fn.startswith("mmexport"):
        # 微信mmexport图片文件
        readable_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(int(re.findall("mmexport([0-9]+).*", fn)[0]) / 1000)))
        return fn.replace("mmexport", f'{readable_time}_mmexport')
    elif match:
        # 含时间戳的其他文件
        timestamp_str = match.group()
        if len(timestamp_str) == 10:
            timestamp = int(timestamp_str)
        elif len(timestamp_str) == 13:
            timestamp = int(timestamp_str) / 1000
        else:
            return fn
        if timestamp > time.time() or timestamp < MIN_TIMESTAMP:
            return fn
        dt = datetime.fromtimestamp(timestamp)
        time_str = dt.strftime('%Y-%m-%d %H:%M:%S')
        return fn if (time_str in fn or dt.strftime('%Y%m%d') in fn) else f"{time_str}_{fn}"
    else:
        return fn


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print()
        print('An mmexport photos rename tool')
        print('USAGE: python rename_mmexport_photo.py /path/to/photos')
        print()
        exit(1)
    path = sys.argv[1]
    if os.path.exists(path):
        for root, dirs, filenames in os.walk(path):
            path = [os.path.join(root, name) for name in filenames]
            for file in path:
                file_name = str(file.rsplit("/", 1)[1])
                target_file_name = gen_target_file_name(file_name)
                if file_name != target_file_name:
                    target_file = file.replace(file_name, target_file_name)
                    try:
                        print(f"Rename {file} to {target_file}")
                        os.rename(file, target_file)
                    except Exception as e:
                        print(e)
    else:
        print(f'Path {path} does not exists.')
