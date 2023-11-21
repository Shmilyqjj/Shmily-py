#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import re
import time

if __name__ == '__main__':
    path = sys.argv[1]
    if os.path.exists(path):
        for root, dirs, filenames in os.walk(path):
            path = [os.path.join(root, name) for name in filenames]
            for file in path:
                file_name = str(file.rsplit("/", 1)[1])
                if file_name.startswith("mmexport"):
                    try:
                        readable_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(int(re.findall("mmexport([0-9]+).*", file_name)[0]) / 1000)))
                        target_file = file.replace("mmexport", f'{readable_time} mmexport')
                        print(f"Rename {file} to {target_file}")
                        os.rename(file, target_file)
                    except Exception as e:
                        print(e)
    else:
        print(f'Path {path} does not exists.')
