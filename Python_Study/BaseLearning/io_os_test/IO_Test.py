# encoding=utf-8
"""
IO测试 文件读写
"""
import os


def inputTest():
    str = raw_input()    # 函数从标准输入读取一个行，并返回一个字符串（去掉结尾的换行符）
    print(str)
    str = input()        # 和raw_input函数基本类似，但input 可以接收一个Python表达式作为输入，并将运算结果返回
    print(str)

def File_IO():
    """
    文件读写
    :return:
    """
    file  = open("d:\\IO_TEST.txt",'a+')
    print(file.name)
    print(file.closed)
    print(file.mode)
    file.write("aaaaaaa\n")
    file.close()

    file0 = open("d:\\Program Files\\hadoop-2.6.0\\etc\\hadoop\\hdfs-site.xml",'a+')
    print(file0.read()) # 读取整个文件，将文件内容放到一个字符串变量中。 如果文件非常大，尤其是大于内存时，无法使用read()方法。
    print(file0.readline()) # 每次只读取一行 与while True和else break连用
    print(file0.readlines()) # 一次性读取整个文件；自动将文件内容分析成一个行的列表list格式

    #os.rename()
    #os.remove()
    #os.mkdir()
    #os.chdir()

def main():
    print("exec main")
    # inputTest()
    File_IO()


def read_dir(path):
    """
    遍历文件夹下所有文件
    :param path:
    :return:
    """
    for root, dirs, filenames in os.walk(path):
        path = [os.path.join(root, name) for name in filenames] # 所有文件全路径

if __name__ == "__main__":
    main()