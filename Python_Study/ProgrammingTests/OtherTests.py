#全局变量 函数内改变函数外变量的方法
import re

count = 0
def xyz():
    global count
    while (count < 10):
        count = count + 1
    print(count)

xyz()
print(count)

res = 'https://www.%s.com/%s/%s/%d' % ('baidu','abc','def',8)
print(res)


s = 'e7\\xad\\x89\\xe6\\x93\\x8d\\xe4\\xbd\\x9c\\r\\n\\r\\n\\r\\nimport os\\r\\nimport re\\r\\n\\r\\n\\r\\n\\r\\nPROJECT_PATH = \'C:\\\\\\\\Users\''
re.match(r'.*import.*', s)

list0 = [1,5,7,6,8,4,2,3]
print(sorted(list0))
print(sorted(list0,reverse=True))

if __name__ == '__main__':
    pass

