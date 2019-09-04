# encoding=utf-8
"""
IO测试 文件读写
"""
def inputTest():
    str = raw_input()    # 函数从标准输入读取一个行，并返回一个字符串（去掉结尾的换行符）
    print(str)
    str = input()        # 和raw_input函数基本类似，但input 可以接收一个Python表达式作为输入，并将运算结果返回
    print(str)

def File_IO():
    file  = open("d:\\IO_TEST.txt",'a+')
    print(file.name)
    print(file.closed)
    print(file.mode)
    file.write("aaaaaaa\n")
    file.close()

    file0 = open("d:\\Program Files\\hadoop-2.6.0\\etc\\hadoop\\hdfs-site.xml",'a+')
    print(file0.read())
    print(file0.readline())
    print(file0.readlines())

    #os.rename()
    #os.remove()
    #os.mkdir()
    #os.chdir()

def main():
    print("exec main")
    # inputTest()
    File_IO()

if __name__ == "__main__":
    main()