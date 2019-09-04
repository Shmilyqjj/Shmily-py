#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description:  list实现栈和队列
:Owner: jiajing_qu
"""

#栈（一种线性表） 先进后出，删除与加入均在栈顶操作 FILO
#插入元素 0 1 2 3 4 5
queue = [1,2,3,4,5,]
print(queue)
queue.insert(0,0) #入栈/插入 在index=0的位置插入0
queue.insert(0,-1)#在index=0的位置插入1
queue.insert(0,-2)
print(queue)
while queue:
    o = queue.pop()
    print(o)


print('-----------------------')

#队列 先进先出 FIFO 队列在队头做删除操作,在队尾做插入操作
#插入元素 0 1 2 3 4 5
stack = [0,1,2,3,4,5]
stack.append(6) #加入
print(stack)
while stack:  #依次出队/删除
    o = stack.pop()
    print(o)