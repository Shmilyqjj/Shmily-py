#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
Description: 单例模式学习
Author:曲佳境
Date: 2019/12/16 22:59
"""
class Singleton(object):
    """
    单例模式：整个程序仅有一个实例化对象
    """
    #如果该类已经有了一个实例则直接返回,否则创建一个全局唯一的实例  饿汉
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls,'_instance'):
            cls._instance = super(Singleton,cls).__new__(cls)
        return cls._instance


class Person(Singleton):
    pass