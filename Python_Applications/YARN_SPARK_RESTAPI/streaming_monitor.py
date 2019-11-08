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


LOG_DIR_PATH = '/data/logs/streaming_monitor'
# LOG_FILE_PATH = '/data/logs/streaming_monitor/monitor.log'
HISTORY_LOG_PATH = '/data/logs/streaming_monitor/history'
MAX_LOG_SIZE = 10  # 10MB
YARN_SITE = 'http://yarn-ip:8088/proxy'
streaming_monitor_dict = {
# dict说明: key为Streaming任务名,Value为一个元组(超时阈值-秒, 报警给谁, Streaming未运行是否报警-默认否)
    'streaming.app_name_1': (1800, 'to_who', True),
    'streaming.app_name_2': (600, ',to_who'),
    'streaming.app_name_3': (1200, 'to_who'),
    'streaming.app_name_4': (100, 'to_who,to_who'),
    'streaming.app_name_5': (180, ',to_who', True),
    'streaming.app_name_6': (600, 'to_who'),
    'streaming.app_name_7': (180, ',to_who'),
    'streaming.app_name_8': (600, ',to_who'),
}

def get_streaming_info(application_id):
    """
    根据application_id获得streaming详细信息
    :param application_id: streaming程序ID
    :return: 返回streaming详细信息 JSON格式    status_code不是200则返回False
    """
    session = requests.session()
    res = session.get('%s/%s/api/v1/applications/%s/jobs' % (YARN_SITE, application_id, application_id))
    if res.status_code == 200:
        return res.json()
    else:
        print("没有拿到对应%s任务的信息！" % application_id)
        return False


def get_running_time(streaming_info):
    """
    获得最新的Streaming Job的运行时间
    :param streaming_info: Spark Rest API获取的信息
    :return: 返回已运行时间 单位:秒
    """
    if streaming_info:
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
    根据application_name获得ApplicationID 如果任务未运行,则返回空列表
    :param application_name: 待监控的应用名称
    :return: 返回application id列表 list
    """
    running_list = YarnSpider.get_running_apps()
    application_id_list = filter(lambda x: x['name'] == application_name, running_list)
    return application_id_list


def check_is_jam(application_name, limit_time, contact, running=False):
    """
    判断Streaming程序是否重复运行或卡住并报警
    :param running: 默认False不检测是否在运行  True则开启未运行报警
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
        if running and new_job_id == '0':
            alarm('weixin', contact, "从Spark UI获取不到Streaming任务%s的信息" % application_name)
        elif run_time > limit_time:
            content = '%s streaming 任务卡住，KILL并重启此任务！' % application_name
            # if application_name == 'streaming.qxb_company_view_and_monitor_streaming':
            #     print("streaming.qxb_company_view_and_monitor_streaming排错")
            #     content = "streaming.qxb_company_view_and_monitor_streaming卡住，排错中，暂时不自动重启！"
            # else:
            YarnMonitor.kill_app_by_name(application_name)
            alarm('weixin', contact, content)
            print(content)

    else:
        print("%s任务未运行！" % application_name)
        if running:
            alarm('weixin', contact, "Streaming任务%s未运行" % application_name)


# def logs_manager():
#     """
#     管理日志文件（自动清理）
#     日志文件位置LOG_FILE_PATH = '/data/logs/streaming_monitor/monitor.log'
#     达到10M时移入HISTORY_LOG_PATH = '/data/logs/streaming_monitor/history'
#     七天后删除HISTORY_LOG
#     """
#     now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
#     mkdir(LOG_DIR_PATH)
#     if os.path.exists(LOG_FILE_PATH):
#         file_size = os.path.getsize(LOG_FILE_PATH)
#         if file_size >= MAX_LOG_SIZE:
#             shutil.move(LOG_FILE_PATH, '%s/%s_monitor.log' % (HISTORY_LOG_PATH, now_time))
#             print('日志达到%d字节，移入%s' % (MAX_LOG_SIZE, HISTORY_LOG_PATH))
#     if len(os.listdir(HISTORY_LOG_PATH)) != 0:  # 文件数不为0
#         for name in os.listdir(HISTORY_LOG_PATH):
#             now_timestamp = time.time()
#             alter_timestamp = os.path.getmtime('%s/%s' % (HISTORY_LOG_PATH, name))
#             if now_timestamp - alter_timestamp >= 604800:
#                 os.remove('%s/%s' % (HISTORY_LOG_PATH, name))
#                 print('历史日志文件过期,删除%s文件' % name)
logs_manager(LOG_DIR_PATH, 7, MAX_LOG_SIZE, LOG_FILES)  # 7天自动清理


@auto_batch2()
def main(para=None):
    """
    主方法入口
    :param para:
    :return:
    """
    logs_manager('/data/logs/streaming_monitor/', 7, 10, ['monitor.log'])
    print('当前时间为：%s' % datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    application_name = para.get('application_name')
    limit_time = para.get('limit_time')
    contact = para.get('contact')
    running = para.get('running')
    if application_name and limit_time:
        check_is_jam(application_name, limit_time, contact, running)
    else:
        for application_name, key_value in streaming_monitor_dict.items():
            if len(key_value) == 3:
                check_is_jam(application_name, key_value[0], key_value[1], key_value[2])
            else:
                check_is_jam(application_name, key_value[0], key_value[1])


if __name__ == '__main__':
    main()
