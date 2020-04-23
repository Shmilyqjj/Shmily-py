#!/usr/bin/env python
# encoding: utf-8
"""
:Description: 判断二叉树A是否为B的子树
:Author: 佳境Shmily
:Create Time: 2020/4/20 17:34
:File: subtree
:Site: shmily-qjj.top
二叉树的子树和子结构
子树的意思是只要包含了一个结点，就得包含这个结点下的所有节点.
子结构的意思是包含了一个结点，可以只取左子树或者右子树，或者都不取。
简单而言，与子树不同的是，子结构可以是A树的任意一部分。
"""
from Python_Study.DataStructureAndAlgorithm.binary_tree.binary_tree import BinaryTree

# 分为两个函数，一个用于遍历节点当做子树的根节点，另一个用于判断是否是子树
def match(root1, root2):
    """
    递归判断root1和root2为根节点的子树
    :param root1:
    :param root2:
    :return:
    """
    if not root1:  # 递归完成时A树先为空则返回TRUE
        return True
    if not root2:   # 递归完成时B树的子树先为空，而A不为空，A比B还大，那A一定不是B的子树
        return False
    if root1.value != root2.value:
        return False
    return match(root1.left, root2.left) and match(root1.right, root2.right)  # 子树：只要包含了一个结点，就得包含这个结点下的所有节点.


def is_subtree(a_tree, b_tree):
    """
    A是否为B的子树
    :param a_tree:
    :param b_tree:
    :return:
    """
    if not a_tree or not b_tree:  # 匹配过程中其中一个子树为空树 则False
        return False
    if match(a_tree, b_tree):  # 匹配以当前的节点为根节点时 是否为子树
        return True
    else:  # 如果当前节点为根节点时不是子树 判断A树是否为B树的左or右子树
        return is_subtree(a_tree, b_tree.left) or is_subtree(a_tree, b_tree.right)


if __name__ == '__main__':
    bt = BinaryTree()
    bt.add(1)
    bt.add(2)
    bt.add(3)
    bt.add(4)
    bt.add(5)
    bt.add(6)
    bt.add(7)

    bt1 = BinaryTree()
    bt1.add(1)
    bt1.add(2)
    bt1.add(3)
    bt1.add(4)
    bt1.add(5)
    bt1.add(6)
    bt1.add(7)
    bt1.add(8)
    # bt.draw_tree()
    # bt1.draw_tree()
    print(is_subtree(bt1.root, bt.root))
    print(is_subtree(bt.root, bt1.root))
