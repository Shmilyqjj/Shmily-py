#!/usr/bin/env python
# encoding: utf-8
"""
:Description:
:Author: 佳境Shmily
:Create Time: 2021/12/25 10:10
:File: read_parquet
:Site: shmily-qjj.top
"""

from fastparquet import ParquetFile


def read_local_parquet(file_name):
    """
    Read Local ParquetFile
    :param file_name:
    :return:
    """
    pf = ParquetFile(file_name)
    print(pf.columns)
    print(len(pf.columns))
    print(pf.to_pandas())


if __name__ == '__main__':
    file_name: str = "F:\\Downloads\\6dc150c9-60d2-419f-9d86-008c7433b155-r-0-6-SG-50-50"
    file_name: str = "/home/shmily/Downloads/Temp/000000_0"
    read_local_parquet(file_name)