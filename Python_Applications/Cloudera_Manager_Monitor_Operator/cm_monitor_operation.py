#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description:
:Owner: jiajing_qu
:Create time: 2019/9/10 17:10
"""
import requests
import re
import time
from requests import ConnectionError
from requests.auth import HTTPBasicAuth


class CMOperation:
    def __init__(self, auth, ip):
        """
        :param auth: 登陆用户名密码 (from requests.auth import HTTPBasicAuth)  auth =HTTPBasicAuth('用户名', '密码')
        :param ip: 角色CM节点IP地址
        """
        self._ip = ip
        self._auth = auth

    def get_role_name_state(self, service):
        """
        根据主机器IP和服务获取该服务下所有组件的role_name
        :param service: 服务名  hbase,yarn,spark等...
        :return: role_urls_ha_stat 一个list包含多个str   格式role_name&&status  如果是高可用的角色则以ACTIVE或者STANDBY结尾,否则以no_ha结尾
        """
        session = requests.session()
        res = session.get('http://{ip}:7180/api/v18/clusters/Cluster%201/services/{service}/roles'.format(ip=self._ip, service=service), auth=self._auth)
        if res.status_code == 200:
            role_list = res.json()['items']
            role_urls_ha_stat = []
            for i in range(len(role_list)):
                all_url = role_list[i]['roleUrl'].encode('utf-8')
                if 'haStatus' in role_list[i]:
                    ha_stat = role_list[i]['haStatus'].encode('utf-8')   # ACTIVE or STANDBY
                else:
                    ha_stat = 'no_ha'
                role_urls_ha_stat.append(all_url+'&&'+ha_stat)
            role_urls_ha_stat = map(lambda x: re.findall('.*roleRedirect/(.*)', x)[0], role_urls_ha_stat)
            # 获得角色所在机器IP
            # for i in range(len(role_name)):
            #     r = session.get('http://{ip}:7180/api/v18/timeseries?query=select+mem_rss+where+entityName%3D%22{rn}%22'.format(ip=ip,rn=role_name[i]), auth=AUTH)
            #     if r.status_code == 200:
            #         hostname = r.json()['items'][0]['timeSeries'][0]['metadata']['attributes']['hostname']
            #         ip_addr = socket.getaddrinfo(hostname, None, 0, socket.SOCK_STREAM)[0][4][0]
            #         role_ip[role_name[i]] = ip_addr
            return role_urls_ha_stat
        else:
            raise Exception('主机IP地址或服务名有误')

    def get_used_memory(self, role_name):
        """
        CM组件驻留内存监控
        :param:role_name 角色名 HBASETHRIFTSERVER,NODEMANAGER,JOBHISTORY等...
        :return:驻留内存 单位 MB
        """
        session = requests.session()
        res = session.get('http://{ip}:7180/api/v18/timeseries?query=select+mem_rss+where+entityName%3D%22{rn}%22'.format(ip=self._ip, rn=role_name), auth=self._auth)
        if res.status_code == 200:
            try:
                info_json= res.json()['items'][0]['timeSeries'][0]['data']
                if len(info_json) != 0:
                    return int(info_json[3]['value'])/1048576
                else:
                    return 0
            except Exception as e:
                print(e)
            finally:
                session.close()

    def roles_operate(self, role_name, command='restart'):
        """
        根据主机ip和role_name对指定的role进行操作,默认操作是restart
        :param command: 默认重启角色,command支持start,stop,refresh,restart,lsof,jstack,zooKeeperCleanup,zooKeeperInit等,具体见CM官网-restAPI
        :param role_name: 角色名 HBASETHRIFTSERVER,NODEMANAGER,JOBHISTORY等...
        """
        service = re.findall('(.*)-.*-.*', role_name)[0]
        request_url = 'http://{ip}:7180/api/v18/clusters/Cluster%201/services/{service}/roleCommands/{command}'.format(ip=self._ip, service=service, command=command)
        sess = requests.session()
        try:
            res = sess.request('post', request_url, json={'items': [role_name]}, auth=self._auth)
            if res.status_code == 200:
                print('正在%s %s为主节点的%s服务的%s角色'  % (command, self._ip, service, role_name))
                print(res.text)
            else:
                print('%s未%s' % (role_name, command))
        except ConnectionError as e:
            print(e)
        finally:
            sess.close()

    def oom_roles_operate(self, service, role, command='restart', mem=0, active=False):
        """
        对OOM的角色或对ACTIVE状态角色进行操作
        :param role: 角色名 HBASETHRIFTSERVER,NODEMANAGER,JOBHISTORY等(全部大写)...
        :param service:服务名 hbase,yarn,spark等(全部小写)...
        :param mem: 驻留内存阈值 MB 默认0表示不需要判断阈值,直接执行命令
        :param active: 是否只重启active状态的角色(默认重启全部,如果设为True,请确定角色做了高可用)
        :param command: 默认重启角色,command支持start,stop,refresh,restart,lsof,jstack,zooKeeperCleanup,zooKeeperInit等,具体见官网restAPI
        :return:
        """
        role_names = self.get_role_name_state(service)  # 得到任务和ha状态
        filtered_dict = {}
        for role_name in role_names:
            if re.findall('.*%s.*' % role, role_name):
                tmp = role_name.split('&&')
                filtered_dict[tmp[0]] = tmp[1]
        for name, state in filtered_dict.items():
            if mem == 0:
                if not active:
                    self.roles_operate(name, command)
                    time.sleep(120)
                else:
                    if state == 'ACTIVE':
                        self.roles_operate(name, command)
            elif self.get_used_memory(name) >= mem:
                if not active:
                    self.roles_operate(name, command)
                    time.sleep(120)
                else:
                    if state == 'ACTIVE':
                        self.roles_operate(name, command)

    def auto_restart_active_rm(self, warn_timeout=10, restart_timeout=20, used_resource=0.8):
        """
        处理有yarn资源但一直处于Accepted状态的情况
        :param restart_timeout: 重启时间阈值 默认20分钟
        :param warn_timeout: 报警时间阈值  默认10分钟
        :param used_resource: yarn内存资源占用比例  默认0.8
        :return:
        """
        accepted_apps = YarnSpider.get_accepted_apps()
        resource = YarnSpider.get_resource()
        allocated_mb = resource["allocatedMB"]
        total_mb = resource["totalMB"]
        allocated_vcores = resource['allocatedVirtualCores']
        total_vcores = resource['totalVirtualCores']
        vcore_status = float(allocated_vcores) / float(total_vcores)
        mem_status = float(allocated_mb) / float(total_mb)
        content = []
        resource_free = mem_status <= used_resource and vcore_status <= used_resource  # 资源是否空闲
        restart_list = filter(lambda x: x['elapsedTime']/1000 >= restart_timeout*60, accepted_apps)
        warn_list = filter(lambda x: x['elapsedTime']/1000 >= warn_timeout*60, accepted_apps)
        if restart_list and resource_free:
            content = reduce(lambda x, y: x+"\n"+y, map(lambda x: x.get('name'), restart_list)) + \
                      "\n任务处于accepted状态超过%s分钟，重启Active RM" % restart_timeout
        elif warn_list and resource_free:
            content = reduce(lambda x, y: x + "\n" + y, map(lambda x: x.get('name'), warn_list)) + \
                      "\n任务处于accepted状态超过%s分钟" % warn_timeout
        if content:
            alarm("weixin", 'to_who-1,to_who-2,to_who-3', content)
            if 'Active RM' in content:
                self.oom_roles_operate('yarn', 'RESOURCEMANAGER', active=True)


@auto_batch2()
def main(para=None):
    """
    主方法入口
    :param para:
    :return:
    """
    ip = para.get('ip')
    timeout = para.get('timeout')
    used_resource = para.get('used_resource')
    auth = HTTPBasicAuth('admin', '123456')
    cm_operation = CMOperation(auth, ip)
    cm_operation.auto_restart_active_rm(timeout, used_resource)

    # monitor_dict={CM的ip:(服务名,角色名,内存阈值不需要时设置为0,命令)}  比如stop start等命令不需要设置内存阈值直接执行时 内存阈值设为0
    monitor_dict = {'192.168.1.101': ('hbase', 'HBASETHRIFTSERVER', 1024, 'restart')}
    for ip, values in monitor_dict.items():
        service = values[0]
        role = values[1]
        mem = values[2]
        comm = values[3]
        cm_operation = CMOperation(auth, ip)
        cm_operation.oom_roles_operate(service, role, comm, mem)



if __name__ == '__main__':
    main()