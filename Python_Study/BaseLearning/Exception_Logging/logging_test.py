#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: logging模块学习
:Owner: jiajing_qu
:Create time: 2019/9/25 16:10
"""
import logging
import time
"""
1、日志级别
Python 标准库 logging 用作记录日志，默认分为六种日志级别（括号为级别对应的数值），NOTSET（0）、DEBUG（10）、INFO（20）、WARNING（30）、ERROR（40）、CRITICAL（50）。我们自定义日志级别时注意不要和默认的日志级别数值相同，logging 执行时输出大于等于设置的日志级别的日志信息，如设置日志级别是 INFO，则 INFO、WARNING、ERROR、CRITICAL 级别的日志都会输出。
2、logging 流程
官方的 logging 模块工作流程图如下：
从下图中我们可以看出看到这几种 Python 类型，Logger、LogRecord、Filter、Handler、Formatter。
类型说明：
Logger：日志，暴露函数给应用程序，基于日志记录器和过滤器级别决定哪些日志有效。
LogRecord ：日志记录器，将日志传到相应的处理器处理。
Handler ：处理器, 将(日志记录器产生的)日志记录发送至合适的目的地。
Filter ：过滤器, 提供了更好的粒度控制,它可以决定输出哪些日志记录。
Formatter：格式化器, 指明了最终输出中日志记录的布局。

参数:
filename 日志输出到文件的文件名
filemode 文件模式，r[+]、w[+]、a[+]
format 日志输出的格式
datefat 日志附带日期时间的格式
style 格式占位符，默认为 "%" 和 “{}”
level 设置日志输出级别
stream 定义输出流，用来初始化 StreamHandler 对象，不能 filename 参数一起使用，否则会ValueError 异常
handles 定义处理器，用来创建 Handler 对象，不能和 filename 、stream 参数一起使用，否则也会抛出 ValueError 异常
"""

def logging_print():
    logging.basicConfig(filename="test.log", filemode="a", format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                        datefmt="%d-%M-%Y %H:%M:%S", level=logging.DEBUG)
    logging.basicConfig()
    logging.debug('This is a debug message')
    logging.info('This is an info message')
    logging.warning('This is a warning message')
    logging.error('This is an error message')
    logging.critical('This is a critical message')

def exception_logging_print():
    f = lambda x, y: x / y
    try:
        f(6,0)
    except Exception as e:
        logging.exception("Exception occurred")
        print('-----------------------------------------')
        time.sleep(2)
        logging.error("Exception occurred", exc_info=True)
        print('-----------------------------------------')
        time.sleep(2)
        logging.log(level=logging.DEBUG, msg="Exception occurred", exc_info=True)





if __name__ == '__main__':
    # logging_print()
    exception_logging_print()
