#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: zookeeper操作
:Owner: jiajing_qu
:Create time: 2024/8/21 14:24
"""

from kazoo.client import KazooClient
from kazoo.exceptions import NodeExistsError, NoNodeError


class ZookeeperUtil:
    def __init__(self, hosts='127.0.0.1:2181', timeout=10):
        """
        初始化Zookeeper连接。
        :param hosts: Zookeeper主机列表, 格式为'host1:port,host2:port'
        :param timeout: 连接超时时间
        """
        self.zk = KazooClient(hosts=hosts, timeout=timeout)
        self.zk.start()

    def create_node(self, path, value=b"", ephemeral=False, makepath=False):
        """
        创建Zookeeper节点。
        :param path: 节点路径
        :param value: 节点初始值
        :param ephemeral: 是否为临时节点
        :param makepath: 是否递归创建父节点
        """
        try:
            self.zk.create(path, value, ephemeral=ephemeral, makepath=makepath)
            print(f"Node created: {path}")
        except NodeExistsError:
            print(f"Node already exists: {path}")

    def get_node(self, path):
        """
        获取Zookeeper节点数据。
        :param path: 节点路径
        :return: 节点的数据
        """
        try:
            data, stat = self.zk.get(path)
            return data
        except NoNodeError:
            print(f"Node does not exist: {path}")
            return None

    def set_node(self, path, value):
        """
        设置Zookeeper节点数据。
        :param path: 节点路径
        :param value: 新的节点值
        """
        try:
            self.zk.set(path, value)
            print(f"Node set: {path}")
        except NoNodeError:
            print(f"Node does not exist: {path}")

    def delete_node(self, path, recursive=False):
        """
        删除Zookeeper节点。
        :param path: 节点路径
        :param recursive: 是否递归删除子节点
        """
        try:
            self.zk.delete(path, recursive=recursive)
            print(f"Node deleted: {path}")
        except NoNodeError:
            print(f"Node does not exist: {path}")

    def node_exists(self, path):
        """
        检查Zookeeper节点是否存在。
        :param path: 节点路径
        :return: 节点是否存在
        """
        exists = self.zk.exists(path)
        return exists is not None

    def close(self):
        """
        关闭Zookeeper连接。
        """
        self.zk.stop()
        self.zk.close()

    def traverse_zk_nodes(self, path):
        """
        定义一个递归函数来遍历所有节点
        :param path:
        :return:
        """
        try:
            # 获取当前路径下的所有子节点
            children = self.zk.get_children(path)
            if not children:
                return
            for child in children:
                child_path = f"{path}/{child}" if path != "/" else f"/{child}"
                print(f"Node: {child_path}")

                # 递归遍历子节点
                self.traverse_zk_nodes(child_path)
        except Exception as e:
            print(f"Failed to traverse {path}: {str(e)}")


if __name__ == '__main__':
    # 连接到 Zookeeper
    zk_utils = ZookeeperUtil(hosts='localhost:2181')
    # 遍历节点
    zk_utils.traverse_zk_nodes("/zookeeper")

    # 创建节点
    zk_utils.create_node("/qjj/test", b'test', makepath=True)

    # 节点是否存在
    print(zk_utils.node_exists("/qjj/test"))

    # 获取节点数据
    print(zk_utils.get_node("/qjj/test"))

    # 设置节点数据
    zk_utils.set_node("/qjj", b'qjj')
    print(zk_utils.get_node("/qjj"))

    # 删除节点 递归
    zk_utils.delete_node("/qjj", True)

    # 关闭 释放资源
    zk_utils.close()

