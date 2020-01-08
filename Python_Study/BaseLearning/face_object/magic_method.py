#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: Python魔术方法和魔术变量
:Owner: jiajing_qu
:Create time: 2019/9/8 23:12
"""
import time


def func1():
    """
    常用魔术变量
    :return:
    """
    print(func1.__name__)  # 函数名获取
    print(func1.__module__)  # 获取所在模块
    from Python_Study.BaseLearning.Exception_Logging.logging_test import logging_print
    print(logging_print.__module__) # 获取所在模块
    print(logging_print.__doc__)  # 类、函数的文档帮助  没有则None

    from Python_Study.BaseLearning.face_object.ClassTest import child
    print(child.__bases__)  # 得到当前类的所有父类 tuple
    parent = child.__bases__[0]()  # 初始化它的父类parent
    parent.parentMethod()  # 调用其父类的方法

    print(parent.__dict__,type(parent.__dict__))  # 类或者实例的属性

    print(dir(child))  # 返回类或者对象的所有成员名称列表

    return


"""
Python中对象的创建，初始化是__new__ 和  __init__  销毁是 __del__

__new__的功能是在生成对象之前所做的动作，接受的参数是cls 类，负责对象的创建。对象生成是在 new 里面 的return （返回一个对象）。

__init__是在对象生成之后完善对象的属性，它接受的是self 对象，负责对象的初始化。

__del__为析构方法，对象删除时，自动调用，注意：当程序运行结束之后，会自动释放变量信息，会自动调用析构方法。

"""

class A(object):
    def __new__(cls, *args, **kwargs):
        print('正在new一个A类的对象')
        time.sleep(2)
        # 直接返回父类的new方法 对象生成是在 new 里面 的return （返回一个对象）
        return  super(A, cls).__new__(cls)

    def __init__(self):
        print("正在初始化和完善对象")
        time.sleep(2)

    def __del__(self):
        print("正在删除对象")
        time.sleep(2)


"""
__str__和__repr__  __str__与__repr__ 是在类(对象)中对类(对象)本身进行字符串处理。 
注意：__repr__在交互式python环境中产生作用  str()和repr()是格式化字符串
"""
class ClassWithoutStr(object):
    def __init__(self):
        print("ClassWithoutStr")

class ClassWithStr(object):

    def __init__(self, name):
        print("ClassWithStr")
        self.name = name

    # 如果没有__str__, 才自动返回__repr__的内容
    # 对象的字符串打印
    def __str__(self):
        return "<ClassWithStr: %s>" % (self.name)

    # 在交互式python环境中产生作用
    def __repr__(self):
        return self.name

if __name__ == '__main__':
    func1()
    a = A()

    cwos = ClassWithoutStr()
    cws = ClassWithStr('qjj')
    print(cwos)
    print(cws)


