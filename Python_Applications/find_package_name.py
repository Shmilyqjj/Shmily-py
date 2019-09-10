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
'rsa',
'pysqlContext',
'gc',
'signal',
'cPickle',
'MySQLdb',
'unicodedata',
'pymysql',
'psyco',
'company_word_split_new',
'fcntl',
'stop_words',
'ods_edw_company',
'matplotlib',
'get_business_keyword',
'relation_calculate',
'IndustryProductGraph',
'get_address_detail',
'marshal',
'udf_register',
'find_and_classify',
'pgdb',
'binascii',
'bertModule',
'zhtools',
'calculate_multi',
'DBUtils',
'Pickle',
'get_child_code',
'neo4j-driver']


version_list =[
'avro (1.8.2)',
'backports.functools-lru-cache (1.5)',
'backports.ssl-match-hostname (3.4.0.2)',
'beautifulsoup4 (4.7.1)',
'boto (2.48.0)',
'boto3 (1.5.23)',
'botocore (1.8.37)',
'bs4 (0.0.1)',
'bz2file (0.98)',
'certifi (2018.1.18)',
'chardet (3.0.4)',
'clickhouse-cityhash (1.0.2.2)',
'configobj (4.7.2)',
'confluent-kafka (0.11.4)',
'crypto (1.4.1)',
'Cython (0.27.3)',
'deap (1.2.2)',
'decorator (4.3.0)',
'dnspython (1.15.0)',
'docopt (0.6.2)',
'docutils (0.14)',
'elasticsearch (6.3.0)',
'fastavro (0.17.7)',
'fasttext (0.9.1)',
'flashtext (2.7)',
'future (0.17.1)',
'futures (3.2.0)',
'gensim (3.3.0)',
'Geohash (1.0)',
'greenlet (0.4.13)',
'happybase (1.1.0)',
'hdfs (2.2.2)',
'idna (2.6)',
'importlib (1.0.4)',
'influxdb (5.2.2)',
'iniparse (0.4)',
'iotop (0.6)',
'ipaddr (2.1.11)',
'ipaddress (1.0.16)',
'jieba (0.39)',
'jmespath (0.9.3)',
'kitchen (1.1.1)',
'langdetect (1.0.7)',
'langid (1.1.6)',
'libvirt-python (4.5.0)',
'lxml (4.4.0)',
'marisa-trie (0.7.5)',
'Morfessor (2.0.4)',
'mysql (0.0.1)',
'MySQL-python (1.2.5)',
'Naked (0.1.31)',
'neo4j (1.7.4)',
'neobolt (1.7.13)',
'neotime (1.7.4)',
'networkx (2.1)',
'numpy (1.14.0)',
'pandas (0.22.0)',
'pathlib (1.0.1)',
'perf (0.1)',
'pip (9.0.1)',
'ply (3.11)',
'polyglot (16.7.4)',
'pyahocorasick (1.1.4)',
'pybind11 (2.3.0)',
'pycld2 (0.31)',
'pycrypto (2.6.1)',
'pycurl (7.19.0)',
'pyddq (4.1.1)',
'pyfarmhash (0.2.2)',
'pygobject (3.22.0)',
'pygpgme (0.3)',
'PyHive (0.6.1)',
'PyICU (2.2)',
'pyliblzma (0.5.3)',
'pyltp (0.2.1)',
'python-dateutil (2.6.1)',
'python-Levenshtein (0.12.0)',
'python-linux-procfs (0.4.9)',
'pytz (2017.3)',
'pyudev (0.15)',
'pyxattr (0.5.1)',
'PyYAML (3.12)',
'pyzmq (17.0.0)',
'redis (2.10.6)',
'requests (2.18.4)',
's3transfer (0.1.12)',
'sasl (0.2.1)',
'schedutils (0.4)',
'scikit-learn (0.19.1)',
'scipy (1.0.0)',
'scoop (0.7.1.1)',
'setuptools (38.4.0)',
'shellescape (3.4.1)',
'simhash (1.8.0)',
'simplejson (3.13.2)',
'six (1.11.0)',
'sklearn (0.0)',
'slip (0.4.0)',
'slip.dbus (0.4.0)',
'smart-open (1.5.6)',
'soupsieve (1.9.1)',
'thrift (0.11.0)',
'thrift-sasl (0.3.0)',
'thriftpy (0.3.9)',
'ua-parser (0.8.0)',
'ujson (1.35)',
'urlgrabber (3.10)',
'urllib3 (1.22)',
'user-agents (2.0)',
'wheel (0.32.2)',
'yum-metadata-parser (1.1.4)',
'zhconv (1.4.0)',
'pyhive (0.6.1)',
'python-Levenshtein (0.12.0)'
]
tran=(('yaml','PyYAML==3.12'),
 ('confluent_kafka','confluent-kafka'),
 ('Crypto','pycrypto==2.6.1'),
 ('sklearn','scikit-learn==0.19.2'),)

maps = {
    'Levenshtein':'python-Levenshtein',
    'pyhive':'PyHive',
    'dateutil':'python-dateutil',
    'farmhash':'pyfarmhash',
    'gensim':'gensim # NumPy and SciPy are dependencies of gensim!'
}

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
                            # print(lines)
                            for line in lines:
                                if re.match('^\s*import.*', line) or re.match('^\s*from.*import.*', line):
                                    line = line.lstrip()
                                    # print(line)   no problem
                                    package_list = line.split(' ')[1].split('.')[0].strip().strip('*').strip('=').split(',')
                                    if len(package_list) == 1:
                                        if package_list[0]:
                                            all_pack_name.add(package_list[0])
                                    else:
                                        for pack in package_list:
                                            if pack:
                                                all_pack_name.add(pack)

    packs = []
    for pack_name in all_pack_name:
        if pack_name not in PYTHON_INNER_LIB and pack_name not in find_file_name(project_path):
            # print(pack_name)
            packs.append(pack_name)
    return packs

def filters(packs,version_list):
    packs1=[]
    for w in packs:
        for key in maps:
            if w == key:
                packs.remove(key)
                packs.append(maps.get(key))
    for i in range(len(packs)):
        flag = 0
        for j in range(len(version_list)):
            if packs[i] in version_list[j]:
                res = re.match(r".*\((.*)\).*", version_list[j]).group(1)
                packs1.append(packs[i] + "==" + res)
                flag = 1
        if not flag:
            packs1.append(packs[i])

    for i in range(len(packs1)): # pip install %s 版本号
        for it in tran:
            if re.match(".*%s.*"%it[0],packs1[i]):
                packs1[i] = it[1]
        packs1[i] = 'pip install ' + packs1[i]
    for result in packs1:
        if result != 'pip install avro==0.17.7':
            print(result)


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
    packs = find_package_name(project_path)
    filters(packs, version_list)
    # s = find_file_name(project_path)
    # print(s)



