#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description:
:Owner: jiajing_qu
:Create time: 2019/9/5 17:10
"""
import requests, re, time
from requests import ConnectionError
from requests.auth import HTTPBasicAuth
AUTH = HTTPBasicAuth('admin', 'admin') # 登陆用户名密码
MONITOR_DICT = {
    '10.2.5.72': ('hbase', 'HBASETHRIFTSERVER', 1024)
}


def get_role_name(ip, service):
    """
    根据主机器IP和服务获取该服务下所有组件的role_names
    :param service: 服务名
    :param ip: 主机器IP
    :return: role_names
    """
    session = requests.session()
    res = session.get('http://{ip}:7180/api/v18/clusters/Cluster%201/services/{service}/roles'.format(ip=ip,service=service), auth=AUTH)
    if res.status_code == 200:
        role_list = res.json()['items']
        role_urls = []
        for i in range(len(role_list)):
            all_url = role_list[i]['roleUrl'].encode('utf-8')
            role_urls.append(all_url)
        role_names = map(lambda x: re.findall('.*roleRedirect/(.*)', x)[0], role_urls)
        # 获得角色所在机器IP
        # for i in range(len(role_name)):
        #     r = session.get('http://{ip}:7180/api/v18/timeseries?query=select+mem_rss+where+entityName%3D%22{rn}%22'.format(ip=ip,rn=role_name[i]), auth=AUTH)
        #     if r.status_code == 200:
        #         hostname = r.json()['items'][0]['timeSeries'][0]['metadata']['attributes']['hostname']
        #         ip_addr = socket.getaddrinfo(hostname, None, 0, socket.SOCK_STREAM)[0][4][0]
        #         role_ip[role_name[i]] = ip_addr
        return role_names
    else:
        print('主机IP地址或服务名有误')


def get_used_memory(role_name,ip):
    """
   CM组件驻留内存监控
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


def restart_roles(role_name,ip):
    """
    根据主机ip和role_name重启指定的role
    :param ip: 主机IP
    :param role_name: 角色名
    """
    service = re.findall('(.*)-.*-.*',role_name)[0]
    request_url = 'http://{ip}:7180/api/v18/clusters/Cluster%201/services/{service}/roleCommands/restart'.format(ip=ip,service=service)
    sess = requests.session()
    try:
        res = sess.request('post', request_url,json={'items':[role_name]}, auth=AUTH)
        if res.status_code == 200:
            print('正在重启%s机器上%s服务的一个%s角色'  % (ip,service,role_name))
            print(res.text)
        else:
            print('HBase Thrift Server未重启')
    except ConnectionError as e:
        print(e)
    finally:
        sess.close()


def restart_oom_roles(ip,service,role,mem):
    """
    滚动重启超内存阈值的角色
    :param role: 角色类型 HBASETHRIFTSERVER,NODEMANAGER,JOBHISTORY等...
    :param service:服务类型 hbase,yarn,spark等...
    :param mem: 驻留内存阈值 MB
    :param ip: 主机器IP
    :return:
    """
    role_names = get_role_name(ip,service)
    filtered_list = []
    for role_name in role_names:
        if re.findall('.*%s.*' % role, role_name):
            filtered_list.append(role_name)
    for name in filtered_list:
        if get_used_memory(name, ip) >= mem:
            restart_roles(name,ip)
            time.sleep(120)


@auto_batch2()
def main(para=None):
    for ip,values in MONITOR_DICT.items():
        service = values[0]
        role = values[1]
        mem = values[2]
        restart_oom_roles(ip, service, role, mem)


if __name__ == '__main__':
    main()