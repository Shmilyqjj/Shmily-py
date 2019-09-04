"""
时间限制：C/C++语言 1000MS；其他语言 3000MS
内存限制：C/C++语言 65536KB；其他语言 589824KB
题目描述：
给定一个整数的数组，找出其中的pair(a,  b)，使得a+b=0，并返回这样的pair数目。（a,  b）和(b,  a)是同一组。
输入
 整数数组
输出
找到的pair数目
样例输入
-1,  2,   4,  5,  -2
样例输出
1
"""
#      -1,2,4,5,-2,0,-4,0
# 100%
s = input()
l = s.split(',')
count = 0
Flag = False
for i in range(len(l)):
    for j in range(i+1):
        if int(l[i])+int(l[j]) == 0:
            if int(l[i]) !=0 and int(l[j]) !=0:
                count = count + 1
            if int(l[i]) ==0 and int(l[j]) ==0 and Flag == False:
                count = count + 1
                Flag = True
print(count)



