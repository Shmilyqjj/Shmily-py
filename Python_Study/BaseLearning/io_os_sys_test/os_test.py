"""
:Author: jiajing_qu
:Create Time: 2020/2/12 19:57
:@File: os_test.py
:@Software: PyCharm
:@Site: shmily-qjj.top
"""
import os
print(os.getcwd())
print(os.getcwdu())
print(os.chdir("C:\Users\Home-PC\PycharmProjects\Shmily-py\Python_Study\BaseLearning\io_os_sys_test"))  #  改变工作路径

# os.path.getatime(file) 输出文件访问时间
# os.path.getctime(file) 输出文件的创建时间
# os.path.getmtime(file) 输出文件最近修改时间