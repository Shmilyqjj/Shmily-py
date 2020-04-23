#!/usr/bin/env python
# encoding: utf-8
"""
:Description: 复习二叉树
:Author: 佳境Shmily
:Create Time: 2020/3/31 22:42
:File: binary_tree_test
:Site: shmily-qjj.top

先说树的概念：
没有结点的树称为空(null或empty)树。
一棵非空的树包括一个根结点，还(很可能)有多个附加结点，所有结点构成一个多级分层结构。
节点的度：节点A的子女数目为该节点的度（几个分叉就是几度）
树的度：树中节点的最大的度。
叶子：度为0的节点
分支结点：度不为零的结点。
层次：根结点的层次为1，其余结点的层次等于该结点的双亲结点的层次加1。
树的高度：树中结点的最大层次。
无序树：如果树中结点的各子树之间的次序是不重要的，可以交换位置。
有序树：如果树中结点的各子树之间的次序是重要的, 不可以交换位置。
森林：0个或多个不相交的树组成。对森林加上一个根，森林即成为树；删去根，树即成为森林。

一个有用的小公式：树中结点数 = 总分叉数 +1。(这里的分叉数就是所有结点的度之和)
题1：设树T的度为4，其中度为1，2，3，4的节点个数分别为4，2，1，1，则T中的叶子数为？
根据节点数=总分叉数+1得到总节点数：1*4+2*2+3*1+4*1+1=16
又根据题目可以知道顶点数目还可以列出一个式子：4+2+1+1+x便可以得到等式：4+2+1+1+x=16；x=8为叶子数。


*性质：
二叉树：
    1.第n层最多有2^(n-1)个元素
    2.深度h树节点最多2^h-1个  （深度：只有一个节点深度是1，根节点只有左子树，深度是左子树深度+1；根节点只有右子树深度是右子树深度+1；根节点既有左子树又有右子树，深度是左右子树深度较大值+1）
满二叉树：
    1.所有叶子节点都在同一层次，且非叶子节点度都为2
    2.深度h的满二叉树节点必为2^h-1个
完全二叉树：
    1.深度为h，除了第h层其余层节点数都达到最大个数，第h层的所有节点连续集中在左边
    2.是一种效率很高的数据结构
二叉查找树：
    1.左子树值小于根节点值，右子树的值大于根节点值
    2.任意节点左右子树也分别是二叉查找树
    3.某些情况会退化成线性链表
红黑树：
    1.节点只有红色和黑色，根节点是黑色
    2.每个叶子节点都是黑色空节点(NIL)
    3.每个红色节点的两个子节点都是黑色（任何位置没有两个相邻红色节点）
    4.从任一节点到其每个叶子的所有路径都包含相同数目的黑色节点。
    5.适用于搜索，插入，删除操作多的场景
    6.查询性能略低于AVL树（最多比AVL多一层，也就是最多比AVL树多比较一次）
    7.插入，删除性能高，AVL树每次插入删除会进行大量的平衡度计算，而红黑树为了维持红黑性质所做的红黑变换和旋转的开销，相较于AVL树为了维持平衡的开销要小得多
二叉平衡树（AVL）： 与红黑树相比更严格平衡
    1.左右子树高度差不超过1
    2.插入和删除过程一旦破坏平衡就要通过旋转来重新平衡
    3.拥有二叉查找树的所有特点
    4.适用场景：插入删除少，查询多。
*存储结构
顺序存储和链式存储
*遍历方式
前序遍历：根节点->左子树->右子树
中序遍历：左子树->根节点->右子树
后序遍历：左子树->右子树->根节点
层次遍历：即每一层从左向右输出
*遍历实现方式
递归实现
非递归实现
"""
import turtle


class Node(object):
    def __init__(self, value=None, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def get_value(self):
        return self.value

    def __str__(self):
        """
        可以直接print node  得到值
        :return:
        """
        return str(self.value)

    def to_dict(self):
        return {
            "value": self.value,
            "left": self.left,
            "right": self.right
        }


class BinaryTree:
    def __init__(self):
        self.root = None
        self.size = 0

    def is_empty(self):
        if self.size == 0 or not self.root:
            return True

    def add(self, value):
        """
        add value to the binary search tree
        :param value:
        :return:
        """
        def insert(node, val):
            if node.value > val:
                if not node.left:
                    node.left = Node(val)
                else:
                    insert(node.left, val)
            else:
                if not node.right:
                    node.right = Node(val)
                else:
                    insert(node.right, val)
        if not self.root:
            self.root = Node(value)
        else:
            insert(self.root, value)

    def pre_traverse(self, root_node):
        """
        pre_order   root->left->right  [one way of deep_order]
        :param root_node:  node
        :return:
        """
        if not root_node:
            return
        print(root_node)
        self.pre_traverse(root_node.left)
        self.pre_traverse(root_node.right)

    def pre_traverse_without_recursion(self, root_node):
        """
        pre_order_without_recursion   root->left->right  [one way of deep_order]
        :param root_node:  node
        :return:
        """
        stack = []
        current_node = root_node
        while current_node or stack:
            if current_node:
                print(current_node)
                stack.append(current_node)
                current_node = current_node.left
            else:
                node = stack.pop()
                current_node = node.right

    def mid_traverse(self, root_node):
        """
        mid_order left->root->right  [one way of deep_order]
        :param root_node:  node
        :return:
        """
        if not root_node:
            return
        self.mid_traverse(root_node.left)
        print(root_node)
        self.mid_traverse(root_node.right)

    def mid_traverse_without_recursion(self, root_node):
        """
        mid_order_without_recursion  left->root->right  [one way of deep_order]
        :param root_node:  node
        :return:
        """
        stack = []
        current_node = root_node
        while current_node or stack:
            if current_node:
                stack.append(current_node)
                current_node = current_node.left
            else:
                node = stack.pop()
                print(node)
                current_node = node.right

    def after_traverse(self, root_node):
        """
        after_order  left->right->mid  [one way of deep_order]
        :param root_node:
        :return:
        """
        if not root_node:
            return
        self.after_traverse(root_node.left)
        self.after_traverse(root_node.right)
        print(root_node)

    def level_traverse(self, root_node):
        """
        层次遍历
        :param root_node: root_node
        :return:
        """
        if not root_node:
            return
        queue = []
        queue.append(root_node)
        while queue:
            current_node = queue.pop()
            print(current_node)
            if current_node.left:
                queue.insert(0, current_node.left)
            if current_node.right:
                queue.insert(0, current_node.right)

    def draw_tree(self, node=None) -> None:
        """
        This function can use turtle to draw a binary tree
        """
        def height(head):
            return 1 + max(height(head.left), height(head.right)) if head else -1
        def jump_to(x, y):
            t.penup()
            t.goto(x, y)
            t.pendown()
        def draw(node, x, y, dx):
            if node:
                t.goto(x, y)
                jump_to(x, y - 20)
                t.write(node.value, align="center")
                draw(node.left, x - dx, y - 60, dx / 2)
                jump_to(x, y - 20)
                draw(node.right, x + dx, y - 60, dx / 2)
        node = node if node else self.root
        t = turtle.Turtle()
        t.speed(0)
        turtle.delay(0)
        h = height(node)
        jump_to(0, 30 * h)
        draw(node, 0, 30 * h, 10 * h)
        t.hideturtle()
        turtle.mainloop()


if __name__ == '__main__':
    bt = BinaryTree()
    # bt.add(1)
    # bt.add(2)
    # bt.add(5)
    # bt.add(7)
    # bt.add(3)
    # bt.add(8)
    # bt.add(10)
    # bt.add(4)
    # bt.add(6)
    # bt.add(9)

    bt.add(3)
    bt.add(2)
    bt.add(4)
    bt.add(1)
    bt.add(6)
    bt.add(5)
    bt.add(7)
    bt.add(8)
    bt.add(8)
    bt.draw_tree()
    # bt.pre_traverse(bt.root)
    # bt.pre_traverse_without_recursion(bt.root)
    # bt.mid_traverse(bt.root)
    # bt.mid_traverse_without_recursion(bt.root)
    # bt.after_traverse(bt.root)
    bt.level_traverse(bt.root)