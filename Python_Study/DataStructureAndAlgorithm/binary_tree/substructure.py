#!/usr/bin/env python
# encoding: utf-8
"""
:Description:判断二叉树A是否为B的子结构（substructure） 约定：空树不是任何一个树的子结构
:Author: 佳境Shmily
:Create Time: 2020/4/23 11:54
:File: substructure
:Site: shmily-qjj.top
二叉树的子树和子结构
子树的意思是只要包含了一个结点，就得包含这个结点下的所有节点.
子结构的意思是包含了一个结点，可以只取左子树或者右子树，或者都不取。
简单而言，与子树不同的是，子结构可以是A树的任意一部分。
"""
from Python_Study.DataStructureAndAlgorithm.binary_tree.binary_tree import BinaryTree

# 两个函数 一个判断是否子结构 一个用于遍历B的子节点作为根节点

def match(root1, root2):
    """
    判断是否子结构
    :param root1:
    :param root2:
    :return:
    """
    if not root1:  # B非空但A先为空 => A先到达叶子节点
        return True
    if not root2:  # A树还有子节点而B树已经到了叶子节点，一定不是子结构
        return False
    if root1.value != root2.value:  # 值不想等一定不是子结构
        return False
    else:
        return match(root1.left, root2.left) and match(root1.right, root2.right)  # 当前节点值相等，递归匹配下一节点值

def is_substructure(a_tree, b_tree):
    """
    主方法 遍历B，判断A是否是B的子树的子结构
    :param a_tree:
    :param b_tree:
    :return:
    """
    if not a_tree or not b_tree:  # 空树不是任何一个树的子结构  当然一个树也不能是空树的子结构  返回False
        return False
    if a_tree.value == b_tree.value:  # 匹配到节点值相等，就开始判断是否是子结构
        return match(a_tree, b_tree)
    else:  # 节点值不想等，递归判断子树节点值
        return is_substructure(a_tree, b_tree.left) or match(a_tree, b_tree.right)

# def has_subtree(root1,root2):
#     if not root1:
#         return True
#     if not root2:
#         return False
#     if root1.value != root2.value:
#         return False
#     else:
#         return has_subtree(root1.left, root2.left) and has_subtree(root1.right, root2.right)
# def is_substructure(a_tree, b_tree):
#     if not a_tree or not a_tree:
#         return False
#     return has_subtree(a_tree, b_tree) or has_subtree(a_tree, b_tree.left) or has_subtree(a_tree, b_tree.right)



if __name__ == '__main__':
    A = BinaryTree()
    A.add(2)
    A.add(3)
    A.add(4)
    A.add(5)
    A.add(6)
    A.add(7)
    A.add(8)


    B = BinaryTree()
    B.add(1)
    B.add(2)
    B.add(3)
    B.add(4)
    B.add(5)
    B.add(6)
    B.add(7)
    B.add(8)
    # B.draw_tree()

    print(is_substructure(A.root, B.root))  # True
    A.add(4)
    A.draw_tree()
    print(is_substructure(A.root, B.root))  # False