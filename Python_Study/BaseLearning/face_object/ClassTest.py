# encoding=utf-8

class Employee:
    '这里是项目介绍'
    empCount = 0
    def __init__(self,name,salary):   # self 代表类的实例 self定义类方法必须有，但是调用时不必传参
        self.name = name
        self.salary = salary
        Employee.empCount += 1

    def displayCount(self):
        print("Count: %d" % Employee.empCount)

    def displayEmployee(self):
        print("Name:",self.name,",Salary:",self.salary)

emp1 = Employee('zz',22)
emp2 = Employee('q',21)
emp1.displayEmployee()
emp2.displayCount()

print(Employee.__doc__,Employee.__name__,Employee.__module__,Employee.__bases__,Employee.__dict__)

class Parent:
    parentAttr = 100
    def __init__(self):
        print("parent constructor")
    def parentMethod(self):
        print("parent method")
    def setAttr(self,attr):
        Parent.parentAttr = attr
    def getAttr(self):
        print("parent attr")

class child(Parent):
    def __init__(self):
        print("child constructor")
    def childMethod(self):
        print("child method")

c = child()
c.childMethod()
c.parentMethod()
c.setAttr(98)
c.getAttr()

#py支持多继承  class A(B,C):

#方法重写
class Parent0:  # 定义父类
    def myMethod(self):
        print '调用父类方法'


class Child0(Parent0):  # 定义子类
    def myMethod(self):
        print '调用子类方法'
c = Child0()  # 子类实例
c.myMethod()  # 子类调用重写方法

#方法重载 （运算符重载）
class Vector:
    __x = 0 #双下划线开头是私有变量
    _y = 1  #单下划线开头是protected变量
    def __init__(self,a,b):
        self.a = a
        self.b = b
    def __str__(self):   #__str__( self ) 用于将值转化为适于人阅读的形式
        return 'Vector(%d,%d)' % (self.a,self.b)
    def __add__(self, other):  #累加
        return Vector(self.a+other.a,self.b+other.b)

V1 = Vector(2,10)
V2 = Vector(5,-4)
print(V1+V2)

