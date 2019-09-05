#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: 
:Owner: jiajing_qu
:Create time: 2019/8/22
"""
import os
import re
from collections import deque  # List插入慢 用deque优化插入删除效率


PYTHON_INNER_LIB = ['abc',
'aifc',
'antigravity',
'anydbm',
'argparse',
'ast',
'asynchat',
'asyncore',
'select',
'atexit',
'audiodev',
'base64',
'BaseHTTPServer',
'Bastion',
'bdb',
'binhex',
'bisect',
'bsddb',
'calendar',
'cgi',
'CGIHTTPServer',
'cgitb',
'chunk',
'cmd',
'code',
'codecs',
'codeop',
'collections',
'colorsys',
'commands',
'compileall',
'compiler',
'ConfigParser',
'contextlib',
'Cookie',
'cookielib',
'copy',
'client',
'copy_reg',
'cProfile',
'csv',
'ctypes',
'curses',
'dbhash',
'decimal',
'difflib',
'dircache',
'dis',
'distutils',
'doctest',
'desensitization_func_c',
'desensitization_spark_udf_c',
'pyspark',
'tesla',
'math',
'random',
'datetime',
'DocXMLRPCServer',
'dumbdbm',
'dummy_thread',
'dummy_threading',
'email',
'encodings',
'filecmp',
'fileinput',
'fnmatch',
'formatter',
'fpformat',
'fractions',
'ftplib',
'functools',
'genericpath',
'getopt',
'getpass',
'gettext',
'glob',
'gzip',
'hashlib',
'heapq',
'hmac',
'hotshot',
'htmlentitydefs',
'htmllib',
'HTMLParser',
'httplib',
'idlelib',
'ihooks',
'imaplib',
'imghdr',
'importlib',
'imputil',
'inspect',
'io',
'json',
'keyword',
'lib-tk',
'lib2to3',
'linecache',
'locale',
'logging',
'macpath',
'macurl2path',
'mailbox',
'mailcap',
'markupbase',
'md5',
'mhlib',
'mimetools',
'mimetypes',
'MimeWriter',
'mimify',
'modulefinder',
'msilib',
'multifile',
'multiprocessing',
'mutex',
'netrc',
'new',
'nntplib',
'ntpath',
'nturl2path',
'numbers',
'oci.dll',
'opcode',
'optparse',
'operator',
'orannzsbb10.dll',
'oraociicus10.dll',
'os',
'os2emxpath',
'pdb',
'pickle',
'pickletools',
'pipes',
'pkgutil',
'platform',
'plistlib',
'popen2',
'poplib',
'posixfile',
'posixpath',
'pprint',
'profile',
'pstats',
'pty',
'lbr',
'pydoc',
'pydoc_data',
'py_compile',
'Queue',
'quopri',
'random',
're',
'requests',
'repr',
'rexec',
'rfc822',
'rlcompleter',
'robotparser',
'runpy',
'sched',
'sets',
'sgmllib',
'sha',
'shelve',
'shlex',
'shutil',
'SimpleHTTPServer',
'SimpleXMLRPCServer',
'service',
'select',
'pysqlContext ',
'site-packages',
'site',
'smtpd',
'smtplib',
'sndhdr',
'socket',
'sys',
'SocketServer',
'sqlite3',
'sre',
'sre_compile',
'sre_constants',
'sre_parse',
'ssl',
'stat',
'statvfs',
'string',
'StringIO',
'stringold',
'stringprep',
'struct',
'subprocess',
'sunau',
'sunaudio',
'symbol',
'symtable',
'sysconfig',
'tabnanny',
'tarfile',
'telnetlib',
'tempfile',
'test',
'textwrap',
'this',
'threading',
'timeit',
'toaiff',
'token',
'tokenize',
'trace',
'traceback',
'tty',
'types',
'tornado',
'time',
'unittest',
'urllib',
'urllib2',
'urlparse',
'user',
'UserDict',
'UserList',
'UserString',
'uu',
'uuid',
'itertools',
'warnings',
'wave',
'weakref',
'webbrowser',
'whichdb',
'wsgiref',
'xdrlib',
'xml',
'xmllib',
'airflow',
'NER_CompanyAndPerson',
'xmlrpclib',
'zipfile',
'_abcoll',
'_LWPCookieJar',
'_MozillaCookieJar',
'_osx_support',
'_pyio',
'_strptime',
'_threading_local',
'_weakrefset',
'__future__',
'__phello__.foo',
'datetime',
'email',
'html',
'http',
'queue',
'misc',
'socket',
'socketserver',
'test',
'total_ordering',
'urllib',
'xmlrpc',
'_markupbase',
'whoosh',
'synonyms',
'table_conf',
'odps',
'pykafka',
'xlwt',
'snakebite',
'pymongo',
'webdm',
'xlrd',
'CRFPP',
'flask',
'tableauserverclient',
'graphframes',
'bson',
'BeautifulSoup',
'pg',
'tensorflow',
'pyhs2',
'py2neo',
'graphframe',
'xgboost',
'paramiko',
'openpyxl',
'kombu',
'rsa',]


def find_package_name(project_path):
    """
    找到所有包/库的名称，存入无重复set集合
    :param project_path:
    :return:
    """
    all_pack_name = set()   # s.add(package_name)
    if os.path.exists(project_path):
        for root, dirs, filenames in os.walk(project_path):
            path = [os.path.join(root, name) for name in filenames]
            for files in path:
                if files:
                    if re.match('.*py$', files):
                        # print(files)
                        with open(files, 'r') as f:
                            lines = f.readlines()
                            for line in lines:
                                if re.match('^\s*import.*', line) or re.match('^\s*from.*import.*', line):
                                    line = line
                                    package_list = line.split(' ')[1].split('.')[0].strip().strip('*').strip('=').split(',')
                                    if len(package_list) == 1:
                                        all_pack_name.add(package_list[0])
                                    else:
                                        for pack in package_list:
                                            all_pack_name.add(pack)
    for pack_name in all_pack_name:
        if pack_name not in PYTHON_INNER_LIB and pack_name not in find_file_name(project_path):
            print(pack_name)




# def find_file_name(project_path):
#     """
#     所有py文件的文件名
#     :param project_path: 项目文件夹路径
#     :return: file_name_list 所有文件名 list
#     """
#     file_name_list = []
#     if os.path.exists(project_path):
#         for root, dirs, filenames in os.walk(project_path):
#             for files in filenames:
#                 if files:
#                     if re.match('.*py$', files): # 正确
#                         files = files.rstrip('.py')
#                         file_name_list.append(files)
#     return file_name_list


def find_file_name(project_path):
    """
    所有py文件的文件名
    :param project_path: 项目文件夹路径
    :return: file_name_list 所有文件名 list
    """
    file_name_list = deque()
    if os.path.exists(project_path):
        for root, dirs, filenames in os.walk(project_path):
            for files in filenames:
                if files:
                    if re.match('.*py$', files): # 正确
                        files = files.rstrip('.py')
                        file_name_list.append(files)
    return file_name_list


if __name__ == '__main__':
    project_path = r'D:\svn\tesla_branch\tesla'
    find_package_name(project_path)
    # s = find_file_name(project_path)
    # print(s)

# result:
"""
unicodedata
gc
yaml
langdetect
confluent_kafka
happybase
gensim
signal
Levenshtein
pyddq
networkx
flashtext
MySQLdb
neo4j
dateutil
hdfs
ujson
redis
pathlib
user_agents
Crypto
influxdb
jieba
elasticsearch
marshal
polyglot
farmhash
binascii
bs4
numpy
cPickle
simplejson
pytz
Geohash
pyhive
sklearn
deap
lxml
six
simhash
pandas
pysqlContext
scoop
"""