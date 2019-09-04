#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: 监控Streaming程序是否卡住并报警
:Owner: jiajing_qu
:Create time: 2019/8/19
"""
import requests
import time
import os
import datetime
import shutil
from tesla.business.cluster_manage.yarn_monitor import YarnSpider, YarnMonitor
from tesla.common.alarm.alarm_interface import alarm
from tesla.common.utility.para_deal import auto_batch2
from tesla.common.utility.ioUtil import mkdir

LOG_DIR_PATH = '/data/logs/streaming_monitor'
LOG_FILE_PATH = '/data/logs/streaming_monitor/monitor.log'
HISTORY_LOG_PATH = '/data/logs/streaming_monitor/history'
MAX_LOG_SIZE = 10485760
YARN_SITE = 'http://centos-bigdata-namenode-10-2-5-102.intsig.internal:8088/proxy'
streaming_monitor_dict = {
    'streaming.zdao_company_visitorlist': (1800, 'tong_fu,bella_lu,sha_wang'),
    'streaming.zdao_user_click_streaming': (600, ',bella_lu'),
    'streaming.cdb_10min_to_hdfs_streaming': (1200, 'tong_fu'),
    'streaming.qxb_company_view_and_monitor_streaming': (100, 'bella_lu,sha_wang'),
    'streaming.zdao_recmd_click_streaming': (180, ',bella_lu'),
    'app_radar_streaming.zdao_register_user': (600, 'xiang_ji'),
    'streaming.zdao_online_user_streaming': (180, ',bella_lu'),
    'streaming.zdao_user_real_time_behavior': (600, ',bella_lu'),
}


def get_streaming_info(application_id):
    """
    根据application_id获得streaming详细信息
    :param application_id: streaming程序ID
    :return: 返回streaming详细信息 JSON格式
    """
    session = requests.session()
    res = session.get('%s/%s/api/v1/applications/%s/jobs' % (YARN_SITE, application_id, application_id))
    if res.status_code == 200:
        return res.json()
    else:
        print("没有拿到对应%s任务的信息！" % application_id)


def get_running_time(streaming_info):
    """
    获得最新的Streaming Job的运行时间
    :param streaming_info: Spark Rest API获取的信息
    :return: 返回已运行时间 单位:秒
    """
    if streaming_info != None:
        new_job_id = streaming_info[0]['jobId']  # 获取最新JobId
        submission_time = streaming_info[0]['submissionTime']
        start_time = time.mktime(time.strptime(submission_time, '%Y-%m-%dT%H:%M:%S.%fGMT')) + 8 * 60 * 60
        now_time = long(time.time())
        run_time = now_time - start_time
        return new_job_id, submission_time, run_time  # 精确到秒
    else:
        return '0', '0', 0


def get_applications_by_name(application_name):
    """
    根据application_name获得ApplicationID
    :param application_name: 待监控的应用名称
    :return: 返回application id列表 list
    """
    running_list = YarnSpider.get_running_apps()
    application_id_list = filter(lambda x: x['name'] == application_name, running_list)
    return application_id_list


def check_is_jam(application_name, limit_time, contact):
    """
    判断Streaming程序是否重复运行或卡住并报警
    :param application_name: Streaming程序名称
    :param limit_time:  超时阈值
    :param contact: 报警给谁
    """
    application_id_list = get_applications_by_name(application_name)
    if len(application_id_list) > 1:
        content = '%s streaming 任务重复运行，KILL并重启此任务！' % application_name
        alarm('weixin', contact, content)
        YarnMonitor.kill_app_by_name(application_name)
        print(content)
    elif len(application_id_list) == 1:
        new_job_id, submission_time, run_time = get_running_time(get_streaming_info(application_id_list[0]['id']))
        print("%s任务%sjob的启动时间是%s，运行了%s秒，阈值是%s" % (
            application_name, new_job_id, submission_time, str(run_time), str(limit_time)))
        if run_time > limit_time:
            content = '%s streaming 任务卡住，KILL并重启此任务！' % application_name
            alarm('weixin', contact, content)
            YarnMonitor.kill_app_by_name(application_name)
            print(content)
    else:
        print("%s任务未运行！" % application_name)


def logs_manager():
    """
    管理日志文件（自动清理）
    日志文件位置LOG_FILE_PATH = '/data/logs/streaming_monitor/monitor.log'
    达到10M时移入HISTORY_LOG_PATH = '/data/logs/streaming_monitor/history'
    七天后删除HISTORY_LOG
    """
    now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    mkdir(LOG_DIR_PATH)
    if os.path.exists(LOG_FILE_PATH):
        file_size = os.path.getsize(LOG_FILE_PATH)
        if file_size >= MAX_LOG_SIZE:
            shutil.move(LOG_FILE_PATH, '%s/%s_monitor.log' % (HISTORY_LOG_PATH, now_time))
            print('日志达到%d字节，移入%s' % (MAX_LOG_SIZE, HISTORY_LOG_PATH))
    if len(os.listdir(HISTORY_LOG_PATH)) != 0:  # 文件数不为0
        for name in os.listdir(HISTORY_LOG_PATH):
            now_timestamp = time.time()
            alter_timestamp = os.path.getmtime('%s/%s' % (HISTORY_LOG_PATH, name))
            if now_timestamp - alter_timestamp >= 604800:
                os.remove('%s/%s' % (HISTORY_LOG_PATH, name))
                print('历史日志文件过期,删除%s文件' % name)


@auto_batch2()
def main(para=None):
    logs_manager()
    print('当前时间为：%s' % datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    application_name = para.get('application_name')
    limit_time = para.get('limit_time')
    contact = para.get('contact')
    if application_name and limit_time:
        check_is_jam(application_name, limit_time, contact)
    else:
        for application_name, key_value in streaming_monitor_dict.items():
            check_is_jam(application_name, key_value[0], key_value[1])


if __name__ == '__main__':
    main()
