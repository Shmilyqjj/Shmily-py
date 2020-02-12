# coding=utf-8
"""
:Description: sys模块学习
:Author: jiajing_qu
:Create Time: 2020/2/12 20:06
:File: sys_test_1.py
:Site: shmily-qjj.top
"""
import sys

"""
sys.modules是一个全局字典，该字典是python启动后就加载在内存中。
每当程序员导入新的模块，sys.modules都将记录这些模块。
字典sys.modules对于加载模块起到了缓冲的作用。
当某个模块第一次导入，字典sys.modules将自动记录该模块。
当第二次再导入该模块时，python会直接到字典中查找，从而加快了程序运行的速度。
字典sys.modules具有字典所拥有的一切方法，可以通过这些方法了解当前的环境加载了哪些模块
"""
modules_dict = sys.modules
print(modules_dict)
print("已经加载的module数：%s" % len(modules_dict))
print(sys.modules["os"])
print(sys.modules["os"].path)