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
默认等级是WARNING，这意味着仅仅这个等级及以上的才会反馈信息，除非logging模块被用来做其它事情。
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

参考 https://www.cnblogs.com/nancyzhu/p/8551506.html
"""

def logging_print():
    """
    将日志筛选并写入文件
    :return:
    """
    logging.basicConfig(filename="test.log", filemode="a", format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                        datefmt="%d-%M-%Y %H:%M:%S", level=logging.DEBUG)    # 会将DEBUG级别及以上的日志记录写入文件
    logging.debug('This is a debug message')
    logging.info('This is an info message')
    logging.warning('This is a warning message')
    logging.error('This is an error message')
    logging.critical('This is a critical message')

def exception_logging_print():
    """
    日志打印到控制台
    :return:
    """
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


# 既可写日志到文件又可以输出到控制台
from logging import handlers
class Logger(object):
    """
     既可写日志到文件又可以输出到控制台
    """
    # 日志级别关系映射
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }

    def __init__(self,filename,level='info',when='D',backCount=3,fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)#设置日志格式
        self.logger.setLevel(self.level_relations.get(level))#设置日志级别
        sh = logging.StreamHandler()#往屏幕上输出
        sh.setFormatter(format_str) #设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename,when=when,backupCount=backCount,encoding='utf-8')#往文件里写入#指定间隔时间自动生成文件的处理器
        #实例化TimedRotatingFileHandler
        #interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)#设置文件里写入的格式
        self.logger.addHandler(sh) #把对象加到logger里
        self.logger.addHandler(th)


if __name__ == '__main__':
    logging_print()   # 写文件
    print("#######################################")
    exception_logging_print()    # 写控制台
    print("#######################################")
    # 写文件和输出控制台
    log = Logger('test1.log',level='debug')
    log.logger.debug('debug')
    log.logger.info('info')
    log.logger.warning('警告')
    log.logger.error('报错')
    log.logger.critical('严重')
    Logger('error.log', level='error').logger.error('error')
