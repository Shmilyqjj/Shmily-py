#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: 集群监控 包括 白天的资源报警 晚上23点自动kill 和0点到6点的资源监控
"""

import datetime
import requests
import json
import time

from tesla.common.utility.send_mail import send as send_email
from tesla.common.alarm.alarm_interface import alarm
from tesla.service.public.config.conf_mysql import airflow_online,big_data
from tesla.service.public.lib import clib_mysql

NAMENODE = 'http://centos-bigdata-namenode-10-2-5-102.intsig.internal:8088'

# 用户单个任务不受限制内存大小
USER_MEMORY = 409600
# 用户总任务不受限制内存大小
USER_MEMORY_TOTAL = 819200
# 超过此资源占比才开始进行资源管控
RESOURCE_OCCUPANCY = 0.85


mail_ToWho = ["tong_fu@intsig.net", "shikai_jiang@intsig.net"]
mail_ToWho_xu = ["shikai_jiang@intsig.net", "544740987@qq.com", "764452708@qq.com",
                 "jie_xu@intsig.net", "tong_fu@intsig.net", "289829293@qq.com"]
mail_ToWho_jsk = ["shikai_jiang@intsig.net", "544740987@qq.com", "tong_fu@intsig.net"]

permanent = [
    "person_push_data",
]

black_list = [
    '',
    'core_adm',
]

white_user = [
    "core_adm",
    "serving",
    "core_test",
    "thrift",
    "kylin",
    "wei_chen",
]

# 为防止非法用户在白名单队列跑，而导致晚上资源不会释放，白名单队列的资源要设置的尽量小
white_queue = [

]

def get_white_list():
    """
    获取本地白名单信息
    :return: 返回list
    """
    user_path = "/data/tesla/day_list" if datetime.datetime.now().strftime("%H%M") < "2300" else "/data/tesla/white_list"
    with open(user_path) as f:
        f = f.read()
        user_white_list = [i.strip() for i in f.split("\n") if i.strip()]
        user_white_list = filter(lambda x: x != "one line one task", user_white_list)
    adm_path = "/data/tesla/adm_user_list"
    with open(adm_path) as f:
        f = f.read()
        adm_user_list = [i.strip() for i in f.split("\n") if i.strip()]
        adm_user_list = filter(lambda x: x != "one line one user", adm_user_list)
    white_user.extend(adm_user_list)
    return user_white_list


def clear_airflow_variable():
    """
    晚上11点删除airflow人为传参，'once_task.'开头的task_id不会被清空
    """
    white_variable = [
        'common.copy_table_data',
        'common.copy_table_data_bak',
        'common.soft_delete_table',
        'common.recover_table',
        'common.create_online_table',
        'common.create_online_table',
        'common.create_online_table',
        'common.hive_to_hbase',
        'common.hive_to_hbase_bak',
        'system.hdfs_small_file_merge_task',

        'person.push_external_interface',
        'person.push_external_interface_bak',
        'person.gen_push_mysql_data',
        'person.gen_push_mysql_data_bak',
    ]
    query = clib_mysql.SimpleQuery("d_airflow_1_10", "variable", airflow_online)
    white_variable = "','".join(white_variable)
    result = query.query("delete from variable where `key` not in('%s') and `key` not like 'once_task.%%'" % white_variable)
    if not result:
        raise Exception(query.error)


class YarnSpider:
    """
    通过rest api获取yarn的信息
    """
    session = requests.session()

    def __init__(self):
        pass

    @classmethod
    def get_running_apps(cls):
        """
        获取正在跑的任务列表，按占用内存倒序排列
        :return:
        """
        running_list = json.loads(cls.session.get(NAMENODE + "/ws/v1/cluster/apps?states=RUNNING").text)
        if running_list["apps"]:
            running_list = running_list["apps"]["app"]
        else:
            return
        running_list = sorted(running_list, key=lambda x: int(x["allocatedMB"]), reverse=True)
        return running_list

    @classmethod
    def get_resource(cls):
        """
        获取当前集群的资源情况
        :return:
        """
        resource = cls.session.get(NAMENODE + "/ws/v1/cluster/metrics").text
        resource = json.loads(resource)["clusterMetrics"]
        return resource


class YarnMonitor:
    """
    通过rest api对集群上的任务进行操作
    """
    session = requests.session()
    apps = YarnSpider.get_running_apps()

    def __init__(self, code_time):
        """
        kill黑名单，初始化集群资源信息，获取白名单，获取超出资源的任务
        """
        self.__kill_black_list()
        self.code_time = code_time
        self.resource = YarnSpider.get_resource()
        self.white_list = get_white_list()
        self.bad_apps = self.__filter_bad_apps()
        self.bad_users = self.__filter_bad_users()
        self.resource_occupancy = self.__get_resource_occupancy()

    @classmethod
    def kill_app_by_name(cls, name):
        """
        通过任务名kill任务
        :param name:
        """
        target_apps = filter(lambda x: x.get('name') == name, cls.apps)
        for app in target_apps:
            cls.session.put(NAMENODE + "/ws/v1/cluster/apps/%s/state" % app["id"], json={"state": "KILLED"})

    def auto_kill(self):
        """
        工作时间和晚上23点两种kill方式
        工作时间：bad_apps中的任务如果不加白名单（day_list），超过4次自动kill
        晚上23点：不在白名单（white_list）的并且非白名单用户（white_user中core_test晚上会被清除）的任务，自动kill
        """
        # 晚上kill方式
        if self.code_time >= "2300":
            white_user.remove("core_test")
            for app in self.apps:
                if (app["name"] not in self.white_list
                        and app["name"] not in permanent
                        and app["user"] not in white_user) \
                        or app["name"] in black_list:
                    self.session.put(NAMENODE + "/ws/v1/cluster/apps/%s/state" % app["id"], json={"state": "KILLED"})
                    print "kill " + str(app)
            # 清理airflow上的variable
            clear_airflow_variable()
        # 工作时间kill方式
        else:
            # 针对单个应用进行处理
            query = clib_mysql.SimpleQuery("d_bigdata", "resource_exceeded_record", big_data)
            # 先删除数据库中白名单任务，再将非白名单任务写入数据库
            query.delete(condition="name in ('%s')" % "','".join(self.white_list))
            for app in self.bad_apps:
                query.query(
                    "insert into resource_exceeded_record(id,name,user) values('%(id)s','%(name)s','%(user)s')" % app)
            # 取出超过4次还没加白名单的applicationId
            ids = query.query("select id from resource_exceeded_record group by id having count(1)>4")["fetch"]
            ids = map(lambda x: x.get("id"), ids)
            for app_id in ids:
                self.session.put(NAMENODE + "/ws/v1/cluster/apps/%s/state" % app_id, json={"state": "KILLED"})
                query.delete(condition="id in ('%s')" % "','".join(ids))

            # 针对用户总使用资源进行处理
            query = clib_mysql.SimpleQuery("d_bigdata", "user_exceeded_record", big_data)
            for user in self.bad_users.keys():
                query.query(
                    "insert into user_exceeded_record(user, memory) values('%s', '%s')" % (user, self.bad_users[user]))
            # 取出第二次依然超过指定资源的用户
            users = query.query("select user from user_exceeded_record group by user having count(1)>1")["fetch"]
            users = map(lambda x: x.get("user"), users)
            # 取出上次超出资源，但是这次并未超出的用户
            users1 = query.query("select user from user_exceeded_record group by user having count(1)=1")["fetch"]
            users1 = map(lambda x: x.get("user"), users1)
            users1 = filter(lambda x: x not in monitor.bad_users, users1)
            for app in self.apps:
                if app['user'] in users:
                    self.session.put(NAMENODE + "/ws/v1/cluster/apps/%s/state" % app['id'], json={"state": "KILLED"})
            users.extend(users1)
            query.delete(condition="user in ('%s')" % "','".join(users))

        # kill完重新刷新资源和apps信息
        self.__init__(self.code_time)

    def clean_record(self):
        """
        清理超出任务资源的记录
        """
        query = clib_mysql.SimpleQuery("d_bigdata", "resource_exceeded_record", big_data)
        query.delete(condition="1=1")
        query = clib_mysql.SimpleQuery("d_bigdata", "user_exceeded_record", big_data)
        query.delete(condition="1=1")

    def reserved_check(self):
        """
        集群异常状态check
        """
        reservedMB = self.resource["reservedMB"]
        reservedVirtualCores = self.resource["reservedVirtualCores"]
        lostNodes = self.resource["lostNodes"]
        if reservedMB > 0:
            self.__deal_warning("reservedMB has problem", reservedMB)
        elif reservedVirtualCores > 0:
            self.__deal_warning("reservedVirtualCores has problem", reservedVirtualCores)
        elif lostNodes > 0:
            self.__deal_warning("lostNodes has problem", lostNodes)

    def day_check(self):
        """
        当前集群使用情况check
        """
        if self.resource_occupancy > 0.90 and '2399' > self.code_time > '1000':
            msg = []
            for i, app in enumerate(self.apps):
                msg.append(str({"( NUMBER " + str(i + 1) + " ) " + app["name"]: app["allocatedMB"]}))
            self.__deal_warning("memory out 90%", "目前的资源占比::" + str( self.resource_occupancy * 100) + " %" +
                                "   资源超过90%，不用资源的退一下，或者适当把资源调小，大家好才是真的好哦   !!!!!!!!!!!!!!!!  "
                                "资源使用降序排序如下(MB)::" + '<p>' + '<p>'.join(msg))
        else:
            print("DAY_CODE:IS_NORMAL")

    def night_check(self):
        """
        晚上集群资源情况check
        """
        availableMB = self.resource["availableMB"]
        availableVirtualCores = self.resource["availableVirtualCores"]
        memory_THR = 3228307
        core_THR = 600
        if availableMB < memory_THR or availableVirtualCores < core_THR:
            # self.apps.sort(key=lambda r:r["allocatedMB"],reverse=True)
            self.__deal_warning("memory too less", "Av:" + str(availableMB/1024)+"G," + str(availableVirtualCores) +"cores"
                                " THR:" + str(memory_THR/1024)+"G," + str(core_THR) +"cores||" +
                                ";||".join([" ".join([ap["user"],ap["name"],str(ap["allocatedMB"]/1024)+"G" ]) for ap in self.apps[:4]]) )
        else:
            print("NIGHT_CODE:IS_NORMAL")

    def memory_judgment(self):
        """
        工作时间超出资源使用人员警告
        """
        msg = ""
        msg1 = ""
        if self.bad_apps or self.bad_users:
            for app in self.bad_apps:
                msg += "user: %(user)s, name: %(name)s, id: %(id)s <p>" % app
                msg_weixin = "你的任务超过{0}G，超过{0}G请在如下目录中添加你的任务名(name的值)：\n".format(str(USER_MEMORY/1024))  + \
                             "/data/tesla/day_list （10.2.5.37）\n" \
                              "user: %(user)s, name: %(name)s, id: %(id)s " % app
                mail_ToWho.append(app["user"] + "@intsig.net")
                alarm('weixin', app["user"], msg_weixin)
            for user in self.bad_users:
                msg1 += "user: %s, memory: %s " % (user, self.bad_users[user])
                msg_weixin = "你总的任务资源超过%sG，10分钟后依然超过(且集群总可用资源小于15%%)会kill你的全部任务！\n" % str(USER_MEMORY_TOTAL/1024) + \
                       "真有需要请联系付同、曾政，并告知原因，谢谢配合！\n" \
                        "user: %s, memory: %s" % (user, self.bad_users[user])
                mail_ToWho.append(user + "@intsig.net")
                alarm('weixin', user, msg_weixin)
            msg = "<font color='red'>如下任务不加白名单超过4次自动kill !!!</font><p>" \
                  "下面这些家伙资源超过{0}G啦，我们没资源用啦!!!如果实在需要过{0}G" \
                  "资源，在机器下的/data/tesla/day_list （10.2.5.37）中添加你的任务名(name的值)<p>{1}<p>".format(str(USER_MEMORY/1024), msg) if msg else ''
            msg1 = "<font color='red'>下面这些家伙总资源开超了%sG，10分钟后依然超过(且集群总可用资源小于%s%%)，kill这些家伙全部任务!!!" \
                   "（真有需要请联系付同、曾政，并告知原因）</font><p>%s<p>" % (str(USER_MEMORY_TOTAL/1024), str(100-RESOURCE_OCCUPANCY*100), msg1) if msg1 else ''
            self.__deal_warning("memory out of %sG, or user total memory out of %sG" % (str(USER_MEMORY/1024), str(USER_MEMORY_TOTAL/1024)), msg + msg1)

    def insert_mysql(self):
        """
        记录凌晨集群资源信息
        """
        query = clib_mysql.SimpleQuery("d_summary", "Yarn_resource", big_data)
        for app in self.apps:
            sql = "insert into Yarn_resource(name,memory,runningContainers,allocatedVCores) " \
                  "values('%(name)s','%(allocatedMB)s','%(runningContainers)s','%(allocatedVCores)s')" % app
            print sql
            query.query(sql)

    def __filter_bad_apps(self):
        """
        筛选超出资源，且不在客户端白名单和代码白名单的app
        :return: 超出资源的app
        """
        bad_apps = []
        for app in self.apps:
            if app["allocatedMB"] > USER_MEMORY \
                    and app["name"] not in permanent \
                    and app["name"] not in self.white_list \
                    and app["user"] not in white_user:
                bad_apps.append(app)
        return bad_apps

    def __get_resource_occupancy(self):
        """
        获取集群内存占用率
        :return:
        """
        allocatedMB = self.resource["allocatedMB"]
        totalMB = self.resource["totalMB"]
        return float(allocatedMB) / float(totalMB)

    def __filter_bad_users(self):
        """
        筛选总使用资源超过指定总资源的用户
        :return:
        """
        users_cost = {}
        for app in self.apps:
            if app["user"] not in white_user:
                if app["user"] not in users_cost:
                    users_cost[app["user"]] = int(app["allocatedMB"])
                else:
                    users_cost[app["user"]] = users_cost[app["user"]] + int(app["allocatedMB"])
        for user in users_cost.keys():
            if users_cost[user] < USER_MEMORY_TOTAL:
                del users_cost[user]
        return users_cost

    def __kill_black_list(self):
        """
        kill黑名单任务任务
        """
        for name in black_list:
            self.kill_app_by_name(name)
        self.apps = YarnSpider.get_running_apps()

    def __deal_warning(self, title, obj):
        """
        根据不同的警告信息，将邮件发给不同的人
        :param title: 邮件主题
        :param obj: 邮件内容
        """
        global mail_ToWho, mail_ToWho_xu, mail_ToWho_jsk
        mail_ToWho = list(set(mail_ToWho))
        mail_ToWho_xu = list(set(mail_ToWho_xu))
        mail_ToWho_jsk = list(set(mail_ToWho_jsk))
        if title == "memory too less":
            alarm('weixin', 'tong_fu,shikai_jiang', "memory or core to less " + str(obj))
            send_email(mail_ToWho_xu, title, str(obj))
        elif (
                title == "reservedMB has problem" or title == "reservedVirtualCores has problem" or title == "lostNodes has problem"):
            send_email(mail_ToWho_jsk, title, str(obj))
        else:
            send_email(mail_ToWho, title, str(obj))


if __name__ == "__main__":
    now = datetime.datetime.now()
    code_time = now.strftime("%H%M")
    weekend = time.strftime("%w", time.localtime())
    monitor = YarnMonitor(code_time)
    if code_time >= '2300':
        monitor.auto_kill()
        monitor.night_check()
    if code_time < "0600":
        monitor.insert_mysql()
    if '0558' < code_time < '0609':
        monitor.clean_record()
        with open('/data/tesla/white_list', 'wb+') as e:
            print 'cleaning white_list ...'
            e.write('one line one task')
        with open('/data/tesla/day_list', 'wb+') as e:
            print 'cleaning day_list ...'
            e.write('one line one task')
        with open('/data/tesla/adm_user_list', 'wb+') as e:
            print 'cleaning adm_user_list ...'
            e.write('one line one user')
    if (("1000" < code_time < "1200") or ("1400" < code_time < "1800")) and weekend != '6' and weekend != '0':
        monitor.day_check()
        monitor.reserved_check()
        print weekend
        print "memory_judgment::::::::::"
        # 集群资源使用小于RESOURCE_OCCUPANCY不做kill
        if monitor.resource_occupancy < RESOURCE_OCCUPANCY:
            query = clib_mysql.SimpleQuery("d_bigdata", "user_exceeded_record", big_data)
            query.delete(condition="1=1")
        else:
            monitor.auto_kill()
            monitor.memory_judgment()
