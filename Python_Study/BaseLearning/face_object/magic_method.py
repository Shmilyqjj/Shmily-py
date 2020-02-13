#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: Python魔术方法和魔术变量
:Owner: jiajing_qu
:Create time: 2019/9/8 23:12
"""
import time
import traceback
# 参考https://blog.csdn.net/Mr_fengzi/article/details/93360845

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

class NumTransform(object):
    """
    这些魔术方法使类的对象可以强转为某个类型并返回值
    """
    def __init__(self,input_num):
        self._input_num = input_num

    def __int__(self):
        return int(self._input_num)

    def __float__(self):
        return float(self._input_num)

    def __abs__(self):
        return abs(self._input_num)

    def __long__(self):
        return long(self._input_num)

    def __oct__(self): # 转换为8进制
        return oct(self._input_num)

    def __hex__(self): # 转换为16进制
        return hex(self._input_num)

    def __complex__(self):# 转为复数形式
        return complex(self._input_num)


class index_and_slice(object):
    """
    索引和切片
__getitem__方法是获取索引值的

__setitem__方法可以对指定索引值进行修改

__delitem__方法可以删除制定索引值
    """
    def __init__(self, l=(10,9,8,7,6,5,4,3,2,1)):
        # 函数的默认值必须是不可变数据类型
        self.l = list(l)  # 转成可变的list集合

    def __getitem__(self, item):
        """
        # 如果是查看索引, 传递的index是索引值;
        # 如果是切片, index是slice对象;
        return  self.scores[index]
        :param item:
        :return:
        """
        return self.l[item]

    # 对指定索引index修改值;
    def __setitem__(self, index, value):
        self.l[index] = value
        print("修改后的list值为： [%s]" % ','.join(map(lambda x: str(x),self.l)))

    def __delitem__(self, index):
        del self.l[index]
        print("删除后的list值为： [%s]" % ','.join(map(lambda x: str(x),self.l)))

    def count(self, a, b):
        print(a+b)



"""
with语句 
with语句的功能：当with语句， 打开文件对象；当with语句执行结束，文件会自动关闭。
with语句的工作机制：python中的with语句使用于对资源进行访问的场合，保证不管处理过程中是否发生错误或者异常都会自动执行规定的(“清理”)操作，释放被访问的资源，比如有文件读写后自动关闭、线程中锁的自动获取和释放等。
with语句底层使用__enter__(self) 和  __exit__(self, exc_type, exc_value, traceback) 这两个魔术方法 
__enter__(self)   定义当使用 with 语句时的初始化行为    __enter__ 的返回值被 with 语句的目标或者 as 后的名字绑定  
__exit__(self, exc_type, exc_value, traceback) 定义当一个代码块被执行或者终止后上下文管理器应该做什么  一般被用来处理异常，清除工作或者做一些代码块执行完毕之后的日常工作
"""
class MyWithOpen(object):
    """
    实现 with方法
    """
    def __init__(self,file_name, mode='r'):
        self.file_name = file_name
        self.mode = mode

    def __enter__(self):
        print("文件打开")
        self.f = open(self.file_name,self.mode)
        return self.f

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.f.close()
        print("文件关闭")

def try_to_import(module_name):
    try:
        __import__(module_name)
        print("try_to_import")
    except:
        traceback.print_exc(1)

def str_contains():
    print('dawdawqjj3424'.__contains__('qjj'))
    print('dawdawqjj3424'.__contains__('123'))

def getattrbute_test():
    """
    https://blog.csdn.net/yitiaodashu/article/details/78974596
    :return:
    """
    ias = index_and_slice()
    attr = ias.__getattribute__("count")  # 获取到类中的属性、方法
    print(attr(1,1))

if __name__ == '__main__':
    func1()
    a = A()

    cwos = ClassWithoutStr()
    cws = ClassWithStr('qjj')
    print(cwos)
    print(cws)

    nt = NumTransform(-5)
    print(abs(nt),float(nt),complex(nt))

    ias = index_and_slice()
    print(ias[0])  # 得到 10   __getitem__
    print(ias[1:])  # 得到索引1之后的
    ias[2] = 11  # __setitem__
    del ias[0]

    str_contains()

    # with MyWithOpen("""C:\Users\jiajing_qu\PycharmProjects\Shmily-py\Python_Study\BaseLearning\Exception_Logging\\\\test.log""",'r') as f:
    #     print(f.read())

    try_to_import('aaa')
    try_to_import('os')

    getattrbute_test()


