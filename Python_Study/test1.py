#函数
a=100
b=-100
print(abs(a),' ',abs(b))#abs函数是取绝对值函数
print(max(1,5,7,-3,6,8,6))#max函数取最大值

a = abs # 变量 a 指向 abs 函数
print(a(-1) )# 所以也可以通过 a 调用 abs 函数
print(hex(35))#整数转十六进制的函数

#定义一个函数
def my_abs(x):
  if x>=0:
    return x
  else:#注意缩进 否则报错expected an indented block
    return -x

print(my_abs(-5),my_abs(6))

def nulf():
    pass#定义一个空函数用pass语句  实际上 pass 可以用来作为占位符，比如现在还没想好怎么写函数的代码，就可以先放一个 pass ，让代码能运行起来。
#pass占位符

#导入包
import math
def move(x,y,step,angle=0):
    nx = x+step*math.cos(angle)
    ny = y-step*math.sin(angle)
    return nx,ny

m = move
r = m(100,100,60,math.pi/6)#但其实这只是一种假象，Python 函数返回的仍然是单一值
print(r)#返回值是一个tuple

print(math.sqrt(2))#根号
print(math.pow(2,2))#2的2次方

def my_pow(x,n=2):#n=2是指在没有传入n值时，默认参数n是2  注意：必选参数在前，默认参数在后，有多个默认参数时变化大的在前变化小的在后
    s=1
    for i in range(n):
      s*=x
    return s

print(my_pow(5,2))
print(my_pow(5))

#多个默认参数时：
def enroll(name, gender, age=6, city='Beijing'):
    print('name:', name)
    print('gender:', gender)
    print('age:', age)
    print('city:', city)

print(enroll('Luna','F'),enroll('QJJ','M',7),enroll('zcy','F',city='Chaoyang'))
    #默认参数必须指向不变对象

def calc(numbers):
    sum=0
    for n in numbers:
        sum = sum + n*n
    return sum		

print(calc([1,2,3]))

def calcv(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n*n
    return sum

print(calcv(1,2,3))

def person(name,age,**kw):
    if 'city' in kw:
	    pass
    if 'job' in kw:
        pass
    print('name:',name,'age:',age,'other:',kw)#关键字参数，传入0个或任意个含参数名的参数在函数内部自动组装为tuple
	

print(person('Michael',30),'|||||',person('Bob',35,city='Beijing'),'|||||',person('Adam', 45, gender='M', job='Engineer'))
#  *arg是可变参数，args接受的是一个tuple   **kw 是关键字参数，kw 接收的是一个 dict
#可变参数既可以直接传入： func(1, 2, 3) ，又可以先组装 list 或 tuple，再通过 *args 传入： func(*(1, 2, 3)) ；


#递归函数：在函数内部，可以调用其他函数。如果一个函数在内部调用自身本身，这个函数就是递归函数。
#递归  -  阶乘
def fact(n):
    if n==1:
        return 1
    return n*fact(n-1)
print(fact(3))

#解决递归调用栈溢出的方法是通过 尾递归优化
#改成尾递归方式，需要多一点代码，主要是要把每一步的乘积传入到递归函数中
def fact(n):
    return fact_iter(n,1)

def fact_iter(num,product):       
    if num==1:
        return product
    return fact_iter(num-1,num*product)
print(fact(5))
#任何递归函数都存在栈溢出的问题。


#练习
#汉诺塔的移动可以用递归函数非常简单地实现。
#请编写 move(n, a, b, c) 函数，它接收参数 n ，表示 3 个柱子 A、B、C
#中第 1 个柱子 A 的盘子数量，然后打印出把所有盘子从 A 借助 B 移动到 C 的方法
def move(n, a, b, c):
    if n == 1:
        print('move', a, '-->', c)
    else:
        move(n-1, a, c, b)
        move(1, a, b, c)
        move(n-1, b, a, c)

print(move(3, 'A', 'B', 'C'))


#slice  切片
L = ['bob','jack','rose','aas','maya','luna']
print(L[0:3]) #切片  0开始时0可省略
print(L[1:5])
#倒着取  右比左大
print(L[-2:])
print(L[-2:-1])
print(L[-5:-2])

L=list(range(100))
print(L[:10:2])#0-9每两个取一个
print(L[::5])#每5个取一个

#tuple也是一种list只是不可变  list是[] tuple元组是()  tuple也可以用切片

T=(1,2,5,8,6,7,9,10)
print(T[1:6:2])

#字符串也可以切片
print('abcdefghijk'[1:6])




#迭代：如果给定一个 list 或 tuple，我们可以通过 for 循环来遍历这个list或tuple，这种遍历我们称为迭代（Iteration）。

#dict的迭代：默认迭代K   d.values() 可迭代value   dict是｛｝
d = {'a':1,'b':2,'c':3}
for key in d:
    print(key)
for value in d.values():
    print(value)

for i,value in enumerate(['a','b','c']):  #Python 内置的 enumerate 函数可以把一个 list 变成索引-元素对
    print(i,value)
for k,v in d.items():#.items()可以同时迭代key和value
    print(k,v)

#列表生成式 range
print(list(range(5)),range(2,15))

#特殊的列表生成式
a = list(x*x for x in range(10))
print(a)
a = list(x*x for x in range(10) if x%2==0)#加判断语句
print(a)
a = list(m+n for m in 'ABC' for n in 'XYZ')#两层循环
print(a)

L=['Hello', 'World', 'IBM', 'Apple']
a = list(s.lower() for s in L) #全部变小写
print(a)

x='abc'
print(isinstance(x,str))#判断是不是字符串

L = ['Hello', 'World', 18, 'Apple', None]
for x in L:
    if isinstance(x,str)==1:
        print(x)

#生成器 generator
g1 = (x*x for x in range(10))#生成器 []和()区别是 前者是一个 list，而后者是一个generator。
print(next(g1))
print(next(g1))
print('---------------------------------')



#生成器打印斐波拉契数列-容易
def fib(max):
    n,a,b=0,0,1
    while n<max:
        yield b#要把 fib 函数变成generator，只需要把 print(b) 改为 yield b 就可以了
        a,b=b,a+b
        n=n+1
    return 'fib done'
print(fib(7))

#杨辉三角的每行
def trangles():
    N = [1]
    while True:
        yield N
        N.append(0)
        N = [N[i-1] + N[i] for i in range(len(N))]
#输出杨辉三角
n = 0
for t in trangles():
    print(t)
    n = n+1
    if n ==10:
        break

#isinstance 判断一个对象是否是Iterable对象（可迭代对象）
from collections import Iterable#先引入Iterable
print(isinstance([],Iterable))  #list
print(isinstance({},Iterable))  #tuple 一旦初始化就不能更改
print(isinstance('abc',Iterable))
print(isinstance(100,Iterable))
#集合数据类型如 list 、 dict 、 str 等是 Iterable 但不是 Iterator

#接收另一个函数为参数的称为高阶函数
def addd(x,y,f):
    return f(x)+f(y)

print(addd(5,-6,abs))

# map() 函数接收两个参数，一个是函数，一个是 Iterable ，
#map 将传入的函数依次作用到序列的每个元素，并把结果作为新的
#Iterator 返回。
#map 例1：
r = map(abs,[1,-2,3,-4,5,-6,-7,8,-9,10])#list的每个元素经过abs作用后返回一个新的list
print(r)   #这个只会输出地址，下面的输出list的值
print(list(r))

#map 例2：
r = map(str,[1,2,3,5,4,-6,8,-7,9,0])#数字转字符串
print(list(r))

#reduce
#再看 reduce 的用法。 reduce 把一个函数作用在一个序列 [x1, x2, x3, ...]
#上，这个函数必须接收两个参数， reduce 把结果继续和序列的下一个元
#素做累积计算，其效果就是：
#reduce(f, [x1, x2, x3, x4]) = f(f(f(x1, x2), x3), x4)

#reduce 例1
def add(x,y):
    return x+y

from functools import reduce #python3需要引用functools
a = reduce(add,[1,2,3,-4,5,6,7,-8])
print(a)

#reduce 例2
def fn(x,y):
    return 10*x + y

a = reduce(fn,[1,3,5,7,9])
print(a)

#test
def normalize(name):
    pass
# 测试:
L1 = ['adam', 'LISA', 'barT']
L2 = list(map(normalize, L1))
print(L2)

#filter - 用于过滤序列  接收一个函数和一个序列，把函数一次作用于每个元素，根据返回值True/False选择是否丢弃该元素
def is_odd(n):
    return n%2 == 1
#filter Test1 选出奇数
f = filter(is_odd,[1,2,3,4,5,6,7,8,9,10,11,12,13])
print(list(f))

#filter Tes2-删除空字符串
def not_empty(s):
    return s and s.strip()

f = filter(not_empty,['a','b','c',' ','None','d','','e',''])
print(list(f))

#sorted 对list进行排序
print(sorted([1,5,8,-8,10,-21,-6,-7,0,2]))
print(sorted([1,5,8,-8,10,-21,-6,-7,0,2],key = abs))  #按绝对值大小排序
print(sorted(['bob', 'about', 'Zoo', 'Credit']))  #按照ASCII的值 首字母的Ascii
print(sorted(['bob', 'about', 'Zoo', 'Credit'],key = str.lower)) #忽略大小写




