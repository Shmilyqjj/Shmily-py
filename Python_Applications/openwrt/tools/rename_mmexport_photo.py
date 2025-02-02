#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import re
import time


def gen_target_file_name(fn: str):
    if fn.startswith("mmexport"):
        readable_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(int(re.findall("mmexport([0-9]+).*", fn)[0]) / 1000)))
        return fn.replace("mmexport", f'{readable_time} mmexport')
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
                    try:
                        target_file = file.replace(file_name, target_file_name)
                        print(f"Rename {file} to {target_file}")
                        os.rename(file, target_file)
                    except Exception as e:
                        print(e)
    else:
        print(f'Path {path} does not exists.')