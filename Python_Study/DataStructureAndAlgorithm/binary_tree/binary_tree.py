#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description:  二叉树 二叉排序树
:Owner: jiajing_qu
"""

class Node:
    def __init__(self,value=None,left=None,right=None):
        self.value = value
        self.left = left  #左子树
        self.right = right#右子树
    def insert_node(self,root,value):  # 二叉排序树的插入  左小右大
        if root == None:
            root = Node(value)
        else:
            if value < root.value:
                root.left = self.insert_node(root.left,value)
            if value > root.value:
                root.right = self.insert_node(root.right,value)
        return root

    def delete_node(self):
        pass



def pre_order(root): #前序 - 根 左 右
    if root == None:
        return
    print(root.value)
    pre_order(root.left)
    pre_order(root.right)

def mid_order(root):#中序 - 左 根 右
    if root == None:
        return
    mid_order(root.left)
    print(root.value)
    mid_order(root.right)

def aft_order(root):#后序 - 左 右 根
    if root == None:
        return
    aft_order(root.left)
    aft_order(root.right)
    print(root.value)

def BFS(root):#层次遍历(宽度优先遍历) 利用队列，依次将根，左子树，右子树存入队列，按照队列的先进先出规则来实现层次遍历。
    if root == None:
        return
    queue = [] # 创建一个队列
    queue.append(root) # 将根存入队列
    while queue:
        current_node = queue.pop(0)  # 拿出首节点
        print(current_node.value)
        if current_node.left:
            queue.append(current_node.left)
        if current_node.right:
            queue.append(current_node.right)

def DFS(root):#深度优先遍历 利用栈，先将根入栈，再将根出栈，并将根的右子树，左子树存入栈，按照栈的先进后出规则来实现深度优先遍历。
    if root == None:
        return
    stack = []
    stack.append(root) #先将根入栈
    while stack:
        current_node = stack.pop()
        print(current_node.value)
        if current_node.right:
            stack.append(current_node.right)
        if current_node.left:
            stack.append(current_node.left)

def add_values_for_sorted_tree(root,value):
    Node.insert_node(root,root,value)

def find_max(root): #仅限二叉排序树调用
    pass

if __name__ == '__main__':
    root = Node('D',Node('B',Node('A'),Node('C')),Node('E',right=Node('G',Node('F'))))
    # pre_order(root)
    # BFS(root)
    DFS(root)
    n = Node(3)
    add_values_for_sorted_tree(n,5)
    add_values_for_sorted_tree(n,7)
    add_values_for_sorted_tree(n,8)
    add_values_for_sorted_tree(n,6)
    add_values_for_sorted_tree(n,2)
    add_values_for_sorted_tree(n,9)
    mid_order(n)
    print('--------------')
    find_max(n)


