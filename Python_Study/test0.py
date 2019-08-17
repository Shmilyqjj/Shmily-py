#Test--＃是注释

print('I','am','a','hero.')
print('100 + 200 =',100+200)

# print absolute value of an integer:
a = int(input('input a num\n'))#input是str型，需要强制类型转换
if a >= 0:
    print(a)
	#缩进是必须的，默认4个空格的缩进
else:
    print(-a)
	
print('I\'m \"OK\"!')#加斜杠 转义字符
print(r'////n/n/t/t/')#r转义字符
print('''wo
shi
ni
ba
ba''')#多行输出
print(True,False,3>2,3>5,5>3 and 3>5,True and False)#and（与运算） 和 布尔
print(True or False)#or（或运算）
print(not 3>5)#not（非运算）
print(None)#空值

a=1 #整数变量a
t_007 = 't007'
Answer0 = True#变量
a = 'abc' #变量a变为字符串
b = a;#让b指向a的数据
a = 3
print(b)#输出b为 abc 不是 3

print('n=123/n','f=456.789/n')
print('\'Hello,\\,Adam\\\'\'')
print('s3 =',r'Hello,'"Bart"'')
#中文编码GBK gb2312 --Unicode 把所有语言都统一到一套编码里    UTF-8 编码就能比Unicode节省空间
print(ord('a'))
print(chr(97))
print(ord('中'))
print(chr(20013))
print(len('ansjs'),len('中文'))
print('中文测试')

name = 'qjj'
print('Hello,%s,you have $%d.'%(name,100))#输出变量值
print('you also have $%d'%2550)#单个变量括号可以省略
print('%2d-%02d'%(3,1))#指定是否补0，和位数
print('PI的值约为%.2f'%3.1415926)#指定小数位数
print('a = %s,b = %s,c = %s,d = %s'%('qjj',20,172.5,'zxw'))#%s是万能的
print('a = %%d,a = %%%d'%5.2)#当%是一个普通符号

#list和tuple
classmates = ['Michael', 'Bob', 'Tracy']#list是一种 有序有序有序的 集合，可以随时添加和删除其中的元素。
print('classmates name = %s'%classmates,len(classmates))#输出list以及list元素的个数
print(classmates[0],classmates[2],classmates[1])#取list中每个元素。索引不要越界，记得最后一个元素的索引是 len(classmates) - 1 。
print(classmates[-1],classmates[-2],classmates[-3])#倒着取元素 倒数第一个 倒数第二个 倒数第三个
classmates.append('Adam')#添加元素到末尾
print('添加元素到末尾',classmates)
classmates.insert(1,'Jack')#元素插入到指定位置-如1是插入到第二个位置
print('插入元素到第二个位置',classmates)
classmates.pop()#删除末尾元素
print('删除末尾元素',classmates)
classmates[1] = 'Sarah'#替换元素
L = ['Apple',123,True,12.856,['asp','java','python'],'end']#list元素类型可以不同，也可以是另外一个list
print('L = %s len = %d'%(L,len(L)),L[4][1])#取出list中list的元素
#另一种有序列表叫元组：tuple    tuple 一旦初始化就不能修改
classmates = ('Michael', 'Bob', 'Tracy')  #没有能改变内部元素值的方法 取内部元素方法与list一致
tNull= ()#这个是tuple
t1=(1)#这个不是tuple，而是数字1
t1t=(1,)#这个是tuple
tC= ('a', 'b', ['A', 'B'])#tuple里插入list，list可变

#条件判断
age=10
if age>=18:
    print('Adult')
elif age >=6:
    print('Teenager')
else:
    print('Kid')
if age:#只要 age 是非零数值、非空字符串、非空 list 等，就判断为 True 否则为False
    print(age)
	
i = input('birth: ')
birth = int(i)
if birth>2000:
    print('00后')
else:
    print('非00后')

#循环----------for...in...循环
names = ['qjj','zxw','aaa','cmy']
for name in names:#依次把 list 或 tuple 中的每个元素迭代出来 for x in list/tuple
    print(name)#注意缩进
sum = 0
for x in [1,2,3,4,5,6,7,8]:
    sum += x
    print(sum)
sum = 0
for x in range(9):#表示0-8
    sum = sum+x
print(sum)

n=99
sum=0
while n>=0:
    sum = sum+n
    n=n-2
print(sum)
print('---------------------------------------------')

#dict  dict的key必须是不可变对象
d = {'Michael':95,'Bob':75,'Tracy':85}#建一个dict
print(d['Michael'])
d['Michael'] = 60 #修改值
if('aaa' in d):#判断是否存在
     print(b['aaa'])
else:
    print('不存在') 
#set和dict类似也是一组key的集合但不存储value，没有重复的key
#set和dict都不是有序的 set自动过滤掉重复元素
s = set([1,2,3,4,4,5,4,5])
s.add(6)#向set中添加元素
print(s)
s.remove(2)#向set中删除元素
print(s)
s1 = set([1,2,3])
s2 = set([2,3,4])
print(s1&s2)#交集
print(s1|s2)#并集


