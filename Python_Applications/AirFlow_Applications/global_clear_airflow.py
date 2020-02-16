#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: 获取AirFlow的tasks的上游和下游以及sensor相关tasks,实现airflow的全局clear
:Owner: jiajing_qu
:Create time: 2019/9/19 16:39
"""
import commands
import datetime
from airflow import models
from airflow import settings
from tesla.common.utility.para_deal import auto_batch_original
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
dag_bag = models.DagBag(settings.DAGS_FOLDER)
results = set()  # 用于暂存结果
clear_tasks = {}


def get_streams(current_task, down=True):
    """
    递归获取一个task_id上游或者下游的所有task_id - 不直接调用,要调用get_dependencies(dag_id, task_id, down=True)
    :param current_task: 当前task对象
    :param down: default->downstream  False->upstream
    :return: downstream or upstreams  set()
    """
    if down:
        ti_list = current_task.downstream_list  # 获取下游所有task实例的列表
        task_id_set = current_task.downstream_task_ids
        results.update(task_id_set)  # 先更新当前task下游的task_id
        for ti in ti_list:
            sets = ti.downstream_task_ids  # 二级下游task_id的set
            results.update(sets)
            if len(ti.downstream_list) > 0:
                get_streams(ti, down)
        return results
    else:
        ti_list = current_task.upstream_list  # 获取上游所有task实例的列表
        task_id_set = current_task.upstream_task_ids
        results.update(task_id_set)  # 先更新当前task下游的task_id
        for ti in ti_list:
            sets = ti.upstream_task_ids  # 二级下游task_id的set
            results.update(sets)
            if len(ti.upstream_list) > 0:
                get_streams(ti, down)
        return results


def get_dependencies(dag_id, task_id, down=True):
    """
    默认获取指定dag_id的task_id下游依赖 down=False时获取上游所有依赖
    :param dag_id: DAG_ID
    :param task_id: TASK_ID
    :param down:    默认True  False->upstream
    :return: 上游或下游依赖 set()
    """
    results.clear()
    dag = dag_bag.get_dag(dag_id)
    if dag is not None:
        current_task = dag.task_dict[task_id]
        res = get_streams(current_task, down).copy()
        return res


def get_all_dags():
    """
    返回一个dict k:dag_id   v:dag_instance
    """
    return dag_bag.dags


def find_whole_tasks_and_dag():
    """
    获取整个系统中全部的dag:tasks
    :return: dict
    """
    dic = {}
    results.clear()
    dag_dic = get_all_dags()
    for dag in dag_dic.keys():
        all_tasks_list = dag_bag.get_dag(dag).task_ids
        dic[dag] = all_tasks_list
    return dic


def find_related_tasks(dep_list, whole_dag_tasks):
    """
    递归获取有关的sensor
    :param dep_list: 依赖的task的列表
    :param whole_dag_tasks: 全局的{dag:[tasks]}
    :return:
    """
    dep_sensor_list = map(lambda x: x + '_sensor', dep_list)  # 依赖拼_sensor
    for dep_sensor in dep_sensor_list:   # 检索sensor是否存在
        dags = filter(lambda key: dep_sensor in whole_dag_tasks[key], whole_dag_tasks)  # 得到sensor对应的dag_id的列表
        for dag in dags:
            next_dep_list = get_dependencies(dag, dep_sensor)  # sensor的downstream tasks列表
            if next_dep_list:
                if dag in clear_tasks:
                    clear_tasks[dag].append(dep_sensor)
                else:
                    clear_tasks[dag] = [dep_sensor]
                if not ''.endswith("_sensor"):  # 如果_sensor结尾的task,忽略
                    find_related_tasks(next_dep_list, whole_dag_tasks)


def run_and_return(cmd, dag, task):
    """
    运行airflow clear命令并打印结果
    :param cmd:  airflow clear命令
    :return:
    """
    (status, output) = commands.getstatusoutput(cmd)
    if status != 0:
        logger.error(output)
    elif output.__contains__('\nNothing to clear.'):
        logger.warn("DAG %s 中的 %s 无相关任务被Clear" % (dag, task))
    else:
        logger.info(cmd)


@auto_batch_original()
def main(para=None):
    """
    clear该dag下所有的task以及与sensor有关的task
    :param para:
    :return:
    """
    dag_id = para.get('dag_id')
    task_id = para.get('task_id')
    dep_list = get_dependencies(dag_id, task_id, down=True)
    dep_list.add(task_id)  # 添加自身，防止找不到自身sensor
    date = (datetime.datetime.now()+datetime.timedelta(days=-1)).strftime("%Y-%m-%d")  # 当前日期减一天
    # 先clear该task
    # airflow clear daily_task_online -t time.time_sensor_08_00 -d -s 2019-09-21 -e 2019-09-21
    """
    -s start_date  -e end_date 时间默认是0点00分 是指task的启动时间和结束时间，如果 -s 2020-01-16 -e 2020-01-16z则任务启动时间为17日0点时才会检测到要被clear的任务
    这种情况一旦任务不是17日0点启动，就不能被clear  这时设置-s 2020-01-16 -e 2020-01-17才能被读取到并clear
    -c参数： 命令强制执行无需确认
    """
    cmd = 'airflow clear %s -t %s -d -c -s %s' % (dag_id, task_id, date)
    run_and_return(cmd, dag_id, task_id)
    whole_dag_tasks = find_whole_tasks_and_dag()
    clear_tasks.clear()
    find_related_tasks(dep_list, whole_dag_tasks)   # 有关的sensor列表保存再clear_tasks
    # 再clear与_sensor相关的clear_tasks
    for dag in clear_tasks:
        for task in clear_tasks[dag]:
            # airflow clear daily_task_online -t time.time_sensor_08_00 -d -s 2019-09-21 -e 2019-09-21
            cmd = 'airflow clear %s -t %s -d -c -s %s' % (dag, task, date)   # -c是 命令强制执行无需确认
            run_and_return(cmd, dag_id, task_id)


if __name__ == '__main__':
    main()













