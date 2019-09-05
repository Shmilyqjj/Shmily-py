#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
:Description: Thrift内存监控和重启Thrift Server接口
:Owner: jiajing_qu
:Create time: 2019/8/29 10:55
"""
import requests,re,time
from requests import ConnectionError
from requests.auth import HTTPBasicAuth
AUTH =  HTTPBasicAuth('admin', 'admin') # 登陆用户名密码


def get_role_name(ip):  # ip = '10.2.5.72'  URL = 'http://10.2.5.72:7180/api/v18/timeseries?query=select+mem_rss+where+entityName%3D%22hbase-HBASETHRIFTSERVER-069864e2c5350de72b0b2c13f67db2fa%22'
    """
    从主机器ip获取所有组件的role_name
    :param ip: 主机器IP
    :return: role_names
    """
    session = requests.session()
    res = session.get('http://{}:7180/api/v18/clusters/Cluster%201/services/hbase/roles'.format(ip), auth=AUTH)
    if res.status_code == 200:
        role_list = res.json()['items']
        role_urls = []
        for i in range(len(role_list)):
            all_url = role_list[i]['roleUrl'].encode('utf-8')
            role_urls.append(all_url)
        role_names = map(lambda x: re.findall('.*roleRedirect/(.*)', x)[0], role_urls)
        # 获取ThriftServer所在机器的IP
        # for i in range(len(role_name)):
        #     r = session.get('http://{ip}:7180/api/v6/timeseries?query=select+mem_rss+where+entityName%3D%22{rn}%22'.format(ip=ip,rn=role_name[i]), auth=AUTH)
        #     if r.status_code == 200:
        #         hostname = r.json()['items'][0]['timeSeries'][0]['metadata']['attributes']['hostname']
        #         ip_addr = socket.getaddrinfo(hostname, None, 0, socket.SOCK_STREAM)[0][4][0]
        #         role_ip[role_name[i]] = ip_addr
        return role_names
    else:
        print('主机IP地址有误')


def get_used_memory(role_name,ip):
    """
    HBase Thrift Server驻留内存监控
    :param:role_name角色名
    :param: ip 主机器IP
    :return:驻留内存 单位 MB
    """
    session = requests.session()
    res = session.get('http://{ip}:7180/api/v18/timeseries?query=select+mem_rss+where+entityName%3D%22{rn}%22'.format(ip=ip,rn=role_name),auth=AUTH)
    if res.status_code == 200:
        try:
            return int(res.json()['items'][0]['timeSeries'][0]['data'][3]['value'])/1048576
        except Exception as e:
            print(e)
        finally:
            session.close()


def restart_hbase_thrift_server(role_name,ip):
    """
    根据主机ip和role_name重启指定的Thrift Server
    :param ip: 主机IP
    :param role_name: 角色名
    """
    req_head = {'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Content-Length': '26',
                'Content-Type': 'application/json',
                'Host': '10.2.5.63:7180',
                'Origin': 'http://10.2.5.63:7180',
                'Referer': 'http://10.2.5.63:7180/cmf/services/26/instances/168/status',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest'
                }
    request_url = 'http://{ip}:7180/api/v18/clusters/Cluster%201/services/hbase/roleCommands/restart'.format(ip=ip)
    sess = requests.session()
    try:
        res = sess.request('post', request_url,json={'items':[role_name]}, headers=req_head,auth=AUTH)
        if res.status_code == 200:
            print('正在重启 %s 上的一个ThriftServer' % ip)
            print(res.text)
        else:
            print('HBase Thrift Server未重启')
    except ConnectionError as e:
        print(e)
    finally:
        sess.close()


def restart_oom_thrift(ip,mem):
    """
    对超内存的Thrift角色滚动重启
    :param mem: 驻留内存阈值 MB
    :param ip: 主机器IP
    :return:
    """
    role_names = get_role_name(ip)
    thrift_names = []
    for role_name in role_names:
        if re.findall('.*HBASETHRIFTSERVER.*', role_name):
            thrift_names.append(role_name)
    for name in thrift_names:
        if get_used_memory(name, ip) >= mem:
            restart_hbase_thrift_server(name,ip)
            time.sleep(120)


@auto_batch2()
def main(para=None):
    ip = str(para.get('ip'))  # 主机器IP
    ip = '10.2.5.72'
    mem = 400
    restart_oom_thrift(ip, mem)


if __name__ == '__main__':
    main()