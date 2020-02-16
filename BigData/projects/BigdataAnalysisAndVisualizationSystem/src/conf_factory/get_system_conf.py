#!/usr/bin/env python
# encoding: utf-8
"""
:Description:获取conf系统参数
:Author: jiajing_qu
:Create Time: 2020/2/16 20:24
:File: get_system_conf.py
:Site: shmily-qjj.top
"""

"""
配置文件结构需要注意一下几点：
键值对可用=或者:进行分隔
section的名字是区分大小写的,而key的名字是不区分大小写的
键值对中头部和尾部的空白符会被去掉
值可以为多行
配置文件可以包含注释，注释以#或者;为前缀
"""
import os
import traceback
import platform
try:
    import ConfigParser    # python2中的名字是ConfigParser
except:
    import configparser as ConfigParser    # python3中的名字是configparser


def get_project_abs_path():
    """
    获取项目的根路径
    兼容linux和win
    :return:
    """
    return os.getcwd().replace("src/conf_factory", "").replace("src\conf_factory", "")


def get_all_properties(conf_path=None):
    """
    获取conf目录下所有conf信息以及项目根路径  兼容Linux和Win
    :param conf_path: 其他需要解析的conf目录，默认为None
    :return: dict
    {'test': {'test': 'test'}, 'project_abs_path': '/opt/module/BigdataAnalysisAndVisualizationSystem/', 'system': {'mysql_default_user': 'root', 'worker_hosts': '192.168.1.102,192.168.1.103', 'mysql_port': '3306', 'log_path': 'default', 'master_host': '192.168.1.101', 'mysql_host': '192.168.1.101'}, 'user': {'tmp_path': 'default', 'log_level': 'warn'}}
    """
    try:
        platform_name = platform.system()
        project_abs_path = get_project_abs_path()
        conf_path = conf_path if conf_path else project_abs_path + "conf"
        con_str = '/' if platform_name == 'Linux' else "\\"
        file_key_dict={
            # conf需要加什么参数，需要在这注册一下
            conf_path + con_str + "system_conf.properties": "system,user",
            conf_path + con_str + "test.properties": "test",
        }
        property_dict = {}
        if os.path.exists(conf_path):
            for root, dirs, filenames in os.walk(conf_path):
                path_list = [os.path.join(root, name) for name in filenames]
                parser = ConfigParser.ConfigParser()
                for property_file in path_list:
                    if "__init__" not in property_file and parser.read(property_file):
                        keys = file_key_dict[property_file].split(',')
                        for key in keys:
                            conf_dict = {}
                            for conf in [{i[0]:i[1]} for i in parser.items(key)]:
                                conf_dict.update(conf)
                            property_dict.update({key: conf_dict})
            property_dict.update({"project_abs_path": project_abs_path})
            property_dict.update({"platform_name": platform_name})
            return property_dict
        else:
            raise Exception("Properties Path is Invalid.")
    except:
        raise Exception(traceback.format_exc())


if __name__ == '__main__':
    abs_path = get_project_abs_path()
    print(abs_path)
    print("-------------------------------------")
    all_properties_dict = get_all_properties()
    print(all_properties_dict)