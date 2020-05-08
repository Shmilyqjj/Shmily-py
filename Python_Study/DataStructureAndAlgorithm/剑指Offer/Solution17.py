#!/usr/bin/env python
# encoding: utf-8
"""
:Description:剑指Offer 17
:Author: 佳境Shmily
:Create Time: 2020/4/28 11:59
:File: Solution17
:Site: shmily-qjj.top
输入两棵二叉树A，B，判断B是不是A的子结构。（ps：我们约定空树不是任意一个树的子结构）
"""
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def match(self, aNode, bNode):
        if not bNode:
            return True
        if not aNode:
            return False
        if aNode.val != bNode.val:
            return False
        return self.match(aNode.left, bNode.left) and self.match(aNode.right, bNode.right)

    def HasSubtree(self, pRoot1, pRoot2):
        # write code here
        if not pRoot1 or not pRoot2:
            return False
        return self.match(pRoot1, pRoot2) or self.HasSubtree(pRoot1.left, pRoot2) or self.HasSubtree(pRoot1.right, pRoot2)







if __name__ == '__main__':
    s = Solution()
