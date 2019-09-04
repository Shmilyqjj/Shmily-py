#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description:[装饰器] 如果想访问属性可以通过属性的getter（访问器）和setter（修改器）方法进行对应的操作。如果要做到这点，就可以考虑使用@property包装器来包装getter和setter方法，使得对属性的访问既安全又方便
:Owner: 曲佳境
:Create time: 2019/9/4 14:38
"""

class Person(object):
    def __init__(self, name, age):
        self._name = name
        self._age = age

    @property   # getter
    def name(self):
        return self._name

    @property
    def age(self):
        return self._age

    @name.setter
    def set_name(self,name):
        self._name = name

    @age.setter
    def set_age(self,age):
        self._age = age

    def show(self):
        if self._age < 21:
            print('%s 比我小' % self._name)
        else:
            print('%s 比我大' % self._name)


if __name__ == '__main__':
    p = Person('zz',22)
    p.show()
    p.set_age = 18  # 调用setter
    p.show()
