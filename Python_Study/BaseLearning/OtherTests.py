#全局变量 函数内改变函数外变量的方法
count = 0
def xyz():
    global count
    while (count < 10):
        count = count + 1
    print(count)

xyz()
print(count)