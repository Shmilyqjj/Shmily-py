#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: Thrift内存监控和重启Thrift Server接口  (通过POST模拟页面点击来实现)
:Owner: jiajing_qu
:Create time: 2019/8/28 10:55
"""
import requests,socket,re
from requests import ConnectionError
from requests.auth import HTTPBasicAuth
import sys
sys.setdefaultencoding('utf-8')


THRIFT_SERVER_RESTART_URLS = {
'5063':'http://centos-bigdata-test-cdh-5063.intsig.internal:7180/cmf/services/26/instances/168/do?id=168&confirm=on&command=Restart',
'5064':'http://centos-bigdata-test-cdh-5063.intsig.internal:7180/cmf/services/26/instances/105/do?id=105&confirm=on&command=Restart',
'5065':'http://centos-bigdata-test-cdh-5063.intsig.internal:7180/cmf/services/26/instances/136/do?id=136&confirm=on&command=Restart'
}
AUTH =  HTTPBasicAuth('admin', 'admin') # 登陆用户名密码

request_url = 'http://192.168.1.63:7180/api/v1/clusters/Cluster%201/services/hbase/roleCommands/restart'

def get_role_ip(ip):  # ip = '192.168.1.72'  URL = 'http://192.168.1.72:7180/api/v6/timeseries?query=select+mem_rss+where+entityName%3D%22hbase-HBASETHRIFTSERVER-069864e2c5350de72b0b2c13f67db2fa%22'
    """
    从主机器ip获取所有组件的role_name和对应机器的IP地址
    :param ip: 主机器IP
    :return:
    """
    session = requests.session()
    res = session.get('http://{}:7180/api/v1/clusters/Cluster%201/services/hbase/roles'.format(ip), auth=AUTH)
    if res.status_code == 200:
        role_list = res.json()['items']
        role_urls = []
        role_ip = {}
        for i in range(len(role_list)):
            all_url = role_list[i]['roleUrl'].encode('utf-8')
            # if all_url.find('HBASETHRIFTSERVER') != -1: # 只获得ThriftServer的地址
            #     role_urls.append(all_url)
            role_urls.append(all_url)
        role_name = map(lambda x: re.findall('.*roleRedirect/(.*)', x)[0], role_urls)
        for i in range(len(role_name)):
            r = session.get('http://{ip}:7180/api/v6/timeseries?query=select+mem_rss+where+entityName%3D%22{rn}%22'.format(ip=ip,rn=role_name[i]), auth=AUTH)
            if r.status_code == 200:
                hostname = r.json()['items'][0]['timeSeries'][0]['metadata']['attributes']['hostname']
                ip_addr = socket.getaddrinfo(hostname, None, 0, socket.SOCK_STREAM)[0][4][0]
                role_ip[role_name[i]] = ip_addr  # 得到role名和ip地址之间的关系dict
        return role_ip
    else:
        print('主机IP地址有误')


def get_used_memory(role_name,ip):
    """
    HBase Thrift Server驻留内存监控
    :param:role_name角色名
    :return:驻留内存 单位 B
    """
    session = requests.session()
    res = session.get('http://{ip}:7180/api/v6/timeseries?query=select+mem_rss+where+entityName%3D%22{rn}%22'.format(ip=ip,rn=role_name),auth=AUTH)
    if res.status_code == 200:
        return res.json()['items'][0]['timeSeries'][0]['data'][3]['value']   # 最新时间的驻留内存 单位b

def get_cm_session_and_cookie(cm_ip,username,password):
    """
    模拟登陆Cloudera Manager 获取cookie
    :param cm_ip: cm机器IP地址
    :param username: cm登录名
    :param password: cm登录密码
    :return: session和cookie
    """
    session = requests.session()
    data = {'j_username': username, 'j_password': password}  # CM账号密码
    res = session.post('http://%s:7180/j_spring_security_check'%cm_ip, data=data)  # 登陆
    if res.status_code == 200:
        cookie = session.cookies.get_dict()  # 获取cookie
        return session,cookie
    else:
        print('Cloudera Manager参数错误或登陆用户名密码错误')


def restart_hbase_thrift_server(request_url,session,cookie,username='admin',password='admin'):
    """
    重启HBase Thrift Server
    :param password: cm登录密码
    :param username: cm登录名
    :param session: 登录后的session会话
    :param cookie: 登录后的cookie
    :param request_url: 重启thrift server的请求链接
    :return: None
    """
    if request_url:
        # 开始执行重启Thrift Server操作
        req_head = {'Accept': '*/*',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'Connection': 'keep-alive',
                    'Content-Length': '26',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'Host': '192.168.1.63:7180',
                    'Origin': 'http://192.168.1.63:7180',
                    'Referer': 'http://192.168.1.63:7180/cmf/services/26/instances/168/status',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
                    'X-Requested-With': 'XMLHttpRequest'
                    }
        login_info = {'username': username, 'password': password}  # 必须加json=login_info 否则post请求无响应  CM账号密码
        try:
            res = session.request('post', request_url, json=login_info, headers=req_head, cookies=cookie)
            if res and res.status_code == 200 and res.text.find('正在加载') >= 0:
                print(res.text)
            else:
                print('[ERROR]some problem before do in request_url.')
        except ConnectionError as e:
            print('Connection ERROR 可能是ip/hostname/port有误',e)
        finally:
            session.close()


@auto_batch2()
def main(para=None):
    # THRIFT_RESTART_URL = 'http://centos-bigdata-test-cdh-5063.intsig.internal:7180/cmf/services/26/instances/168/do?id=168&confirm=on&command=Restart'
    # restart_hbase_thrift_server(THRIFT_RESTART_URL)
    ip = str(para.get('ip'))
    pass


if __name__ == '__main__':
    main()