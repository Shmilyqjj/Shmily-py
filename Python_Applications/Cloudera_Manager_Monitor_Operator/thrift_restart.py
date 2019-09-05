#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
:Description: Thrift内存监控和重启Thrift Server接口
:Owner: jiajing_qu
:Create time: 2019/8/28 10:55
"""
import requests,socket,re
from requests import ConnectionError
from requests.auth import HTTPBasicAuth
AUTH =  HTTPBasicAuth('admin', 'admin') # 登陆用户名密码
IP_MEM_DICT = {
    '10.2.5.63':1024,
    '10.2.5.64':1536,
    '10.2.5.65':1536
}


def get_role_ip(ip):  # ip = '10.2.5.72'  URL = 'http://10.2.5.72:7180/api/v6/timeseries?query=select+mem_rss+where+entityName%3D%22hbase-HBASETHRIFTSERVER-069864e2c5350de72b0b2c13f67db2fa%22'
    """
    从主机器ip获取所有组件的role_name和对应机器的IP地址
    :param ip: 主机器IP
    :return: role_ip 一个dict返回role_name:thrift_server_ip
    """
    session = requests.session()
    res = session.get('http://{}:7180/api/v1/clusters/Cluster%201/services/hbase/roles'.format(ip), auth=AUTH)
    if res.status_code == 200:
        role_list = res.json()['items']
        role_urls = []
        role_ip = {}
        for i in range(len(role_list)):
            all_url = role_list[i]['roleUrl'].encode('utf-8')
            role_urls.append(all_url)
        role_name = map(lambda x: re.findall('.*roleRedirect/(.*)', x)[0], role_urls)
        for i in range(len(role_name)):
            r = session.get('http://{ip}:7180/api/v6/timeseries?query=select+mem_rss+where+entityName%3D%22{rn}%22'.format(ip=ip,rn=role_name[i]), auth=AUTH)
            if r.status_code == 200:
                hostname = r.json()['items'][0]['timeSeries'][0]['metadata']['attributes']['hostname']
                ip_addr = socket.getaddrinfo(hostname, None, 0, socket.SOCK_STREAM)[0][4][0]
                role_ip[role_name[i]] = ip_addr
        return role_ip
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
    res = session.get('http://{ip}:7180/api/v6/timeseries?query=select+mem_rss+where+entityName%3D%22{rn}%22'.format(ip=ip,rn=role_name),auth=AUTH)
    if res.status_code == 200:
        return int(res.json()['items'][0]['timeSeries'][0]['data'][3]['value'])/1048576


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
            print(res.text)
        else:
            print('HBase Thrift Server未重启')
    except ConnectionError as e:
        print(e)
    finally:
        sess.close()


@auto_batch2()
def main(para=None):
    ip = str(para.get('ip'))  # 主机器IP
    role_ip  = get_role_ip(ip)
    for role_name,thrift_server_ip in role_ip.items():
        # if role_name.find('HBASETHRIFTSERVER') != -1: # 只获得ThriftServer的地址
        #     role_urls.append(all_url)
        if re.findall('.*HBASETHRIFTSERVER.*',role_name):
            if IP_MEM_DICT[thrift_server_ip]<=get_used_memory(role_name,ip):
                restart_hbase_thrift_server(role_name, ip)


if __name__ == '__main__':
    main()