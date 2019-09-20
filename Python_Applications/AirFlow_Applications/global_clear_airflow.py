#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: 获取AirFlow的tasks的上游和下游,实现airflow的全局clear
:Owner: jiajing_qu
:Create time: 2019/9/18 16:39
"""
from airflow import models
from airflow import settings


dag_bag = models.DagBag(settings.DAGS_FOLDER)
results = set()  # 用于暂存结果


def get_streams(current_task, down=True):
    """
    递归获取一个task_id上游或者下游的所有task_id
    :param current_task: 当前task对象
    :param down: default->downstream  False->upstream
    :return: downstream or upstreams  set() 用完要手动清空
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


def get_dag_id_by_tasks(task_id, whole_dag_tasks):      # 需要改改改
    """
    根据task_id获取dag_id
    :param task_id:
    :param whole_dag_tasks:
    :return: dag_id
    """
    for dag in whole_dag_tasks:
        if task_id in whole_dag_tasks[dag]:
            return dag


def find_sensors(tasks):
    """
    筛选所有sensor task
    :param tasks: set/list
    :return:sensor_list
    """
    res = []
    if tasks is not None:
        for t in tasks:
            if '_sensor' in t:
                res.append(t)
        return res


clear_tasks = {}


def find_related_tasks(dep_list):
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
                    find_related_tasks(next_dep_list)


if __name__ == '__main__':
    results.clear()
    dag_id = 'behavior_dag_online'
    task_id = 'behavior.cdbp_done_dummy'

    whole_dag_tasks = find_whole_tasks_and_dag()
    dep_list = get_dependencies(dag_id, task_id, down=True)
    # 先kill本dag上游或下游的tasks

    # 然后加_sensor相关的









