#  encoding = utf-8
# 第一行输入点集的个数 N， 接下来 N 行，每行两个数字代表点的 X 轴和 Y 轴。
# 对于 50%的数据,  1 <= N <= 10000;
# 对于 100%的数据, 1 <= N <= 500000;
#
# 输出描述:
# 输出“最大的” 点集合， 按照 X 轴从小到大的方式输出，每行两个数字分别代表点的 X 轴和 Y轴。
#
# 输入例子1:
# 5
# 1 2
# 5 3
# 4 6
# 7 5
# 9 0
#
# 输出例子1:
# 4 6
# 7 5
# 9 0

#30%:
n = int(input())
points = {}
while n:
    x,y = input().split(' ')
    n = n - 1
    points[int(x)] = int(y)

pow_list = []
x_list = list(points.keys())
y_list = list(points.values())
for i in range(len(x_list)):
    pow_list.append(pow(x_list[i],2)+pow(y_list[i],2))

x_list = sorted(x_list,reverse=True)
y = 0
for i in range(len(x_list)):
    if points[x_list[i]] >= y:
        y = points[x_list[i]]
        print(x_list[i], points[x_list[i]])


#10%:
# n = int(input())
# points = {}
# while n:
#     x,y = input().split(' ')
#     n = n - 1
#     points[int(x)] = int(y)
#
# key_list = sorted(list(points.keys()))
# print(key_list[n-1],points[key_list[n-1]])


