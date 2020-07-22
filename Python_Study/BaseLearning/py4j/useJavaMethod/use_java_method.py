#!/usr/bin/env python
# encoding: utf-8
"""
:Description:调用java自带方法
:Author: 佳境Shmily
:Create Time: 2020/7/22 22:25
:File: use_java_method
:Site: shmily-qjj.top

因为py4j不会去启动Java Server所以需要先运行JavaServer.java 启动后才可以使用python调用
"""
from py4j.java_gateway import JavaGateway
gateway = JavaGateway()  # 连接javaServer并进行交互的入口


random = gateway.jvm.java.util.Random()  # 调用Java自带方法
print(random.nextInt(100))
print(random.nextInt(10))

java_class = gateway.entry_point    # 获取Java的类
print(java_class.javaMethod(1, 2))    # 调用Java类方法

new_jvm = gateway.new_jvm_view("aa")  # 一个新的Jvm实例
a = new_jvm.java.util.Random()
print(a.nextInt(100))

# 更多用法见官网：http://www.py4j.org/
