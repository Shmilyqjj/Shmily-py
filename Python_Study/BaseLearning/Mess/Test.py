# -*- coding: UTF-8 -*-
import time;
import calendar;


a,b,c=1,2,"qjj"
print(a+b,c)
print(a+b) #换行输出
print(c)

s='abcdefghi'
print(s[1:4])#包含头下标的字符，但不包含尾下标的字符

t=['a','b','c','d','e']    # List列表
t1=[1,2,3,4,5]
print(t[0]+" "+t[-1])
print(t[0:4:2])
print(t[:])
print(t[0:4])
print(t[3:])
print(t+t1)
print('b' in t)
print('b' not in t)

tuple = ( 'runoob', 786 , 2.23, 'john', 70.2 )  #元组不能二次赋值，相当于只读列表

#字典(dictionary)  列表是有序的对象集合，字典是无序的对象集合。字典当中的元素是通过键来存取的，而不是通过偏移存取。 字典用"{ }"标识。字典由索引(key)和它对应的值value组成。
#K-V
dictionary = {}
dictionary[1] = 'a'
dictionary['a'] = 2
print(dictionary[dictionary[1]])

m=n=1
print(m is n)  #is 是判断两个标识符是不是引用自一个对象

def operatorTest(a,b,s):
    if(s=='/'):
        print(a/b)
    if(s=='**'):
        print(a**b)  #返回a的b次幂
    if(s=='//'):
        print(a//b)  #取整除 - 返回商的整数部分（向下取整）
    if(s=='<>'):
        print(a!=b)

operatorTest(40,20,'/')
operatorTest(2,7,'**')
operatorTest(27,7,'//') #返回商的整数部分-向下取整
operatorTest(7,7,'<>') #不同


for num in range(10,20):  # 迭代10-20之间的数字
    for i in range(2,num): # 根据因子迭代
        if num%i == 0:      # 确定第一个因子
            j=num/i            # 计算第二个因子
            print  ('%d 等于 %d * %d' % (num,i,j))
            break            # 跳出当前循环
    else:                  # 循环的 else 部分
        print (num, '是一个质数')

#bubble sort
NumberList = [1,15,7,6,12,38,65,179]
def bubbleSort(list):
    i = 0
    lenth = len(list)
    for i in range(lenth):
        for j in range(lenth-i-1):
            if(list[j] > list[j+1]):
                temp = list[j]
                list[j+1] = list[j]
                list[j+1] = temp
    return list
print(bubbleSort(NumberList))

print(time.localtime())
print(calendar.month(2019,8))








#多参数函数
def method(arg1,*args):
    for arg in args:
        print(arg1,arg)
    return;
method(1,2,'s','z','a')

p='2'
print(3+int(p))   # int()强转

L=[1,3,4,5,8,7,9,6,0,2,15,58,56,21]
L0 = []
for i in range(len(L)):
    L0.append(L[i])

print(L0)

def main():
    print("--Execute Main--")

if __name__ == "__main__":
    main()
    print('String Format:\n--------\n')
    s = "{str1} 💗 {str2}".format(str1='qjj',str2='zz')
    print(s)