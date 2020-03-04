#!/usr/bin/env python
# encoding: utf-8
"""
:Description:HBase自带监控工具 hbase org.apache.hadoop.hbase.tool.Canary 日志监控
HBase Canary监控报警  监控region get延迟  如果有部分region请求延迟过高，报警
:Author: jiajing_qu
:Create Time: 2020/3/4 14:50
:File: hbase_canary_monitor
:Site: shmily-qjj.top
:etc:  mkdir /data/hbase/log/hbase_canary/
"""

from numpy import mean
import commands
import re
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

CANARY_LOG_PATH = '/data/hbase/log/hbase_canary/canary.log'


def canary_log_analyse(canary_log_path):
    """
    解析hbase canary生成的log
    :return: [(),(),()]
    """
    result = {}
    try:
        with open(canary_log_path,encoding="utf-8",) as f:
            while True:
                lines = f.readlines(1000)
                if not lines:
                    break
                for one_line in lines:
                    logger.debug(one_line)
                    one_info = re.findall(r"[0-9\s:/]*INFO tool.Canary: read from region\s(.*?),(.*?),(.*?). column family (.*) in (\d*)ms",one_line)
                    logger.debug(one_info)
                    if one_info:
                        table = one_info[0][0]
                        start_key = one_info[0][1]
                        ts_region_id = one_info[0][2]
                        column_family = one_info[0][3]
                        ping = int(one_info[0][4])
                        result.setdefault(table, []).append((start_key, ts_region_id, column_family, ping))
    finally:
        f.close()
    return result


def run_hbase_canary(user, host, log_file='/data/hbase/log/hbase_canary/canary.log'):
    """
    对已经免密过的远程机器执行 hbase canary命令 获取region延迟相关信息 并收集日志到本地文件
    :param log_file: canary生成的日志文件路径
    :param user: 可以ssh过去并执行命令的用户
    :param host: 可以ssh过去并执行命令的host
    :return: True or False
    """
    stat, output = commands.getstatusoutput('''ssh -l {user} {host} "hbase org.apache.hadoop.hbase.tool.Canary > {log_file} 2>&1"'''.format(user=user, host=host, log_file=log_file))
    if stat == 0:
        logger.info("远程HBase Canary执行完毕")
        return True
    else:
        logger.error("远程HBase Canary执行失败")
        logger.error(output)
        return False


def deal_and_alarm(ratio=5.0, log_file='/data/hbase/log/hbase_canary/canary.log'):
    """
    处理log信息 对于region延迟高于平均值的 进行报警
    :param ratio:  超过均值的 ratio 倍 报警
    :return:
    """
    res = canary_log_analyse(log_file)
    table_avg_ping_dict = {x: mean([x[3] for x in res[x]]) for x in res}
    for table in res:
        avg_value = table_avg_ping_dict.get(table)
        region_info_list = res[table]
        for region_info in region_info_list:
            ping = region_info[3]
            if ping >= avg_value * ratio:
                start_key = region_info[0]
                ts_region_id = region_info[1]
                column_family = region_info[2]
                content = "HBase表:%s\nStartRow:%s\ntimestamp.regionID:%s\nColumnFamily:%s\n请求延迟%s超过平均值%s的%s倍,请检查。" % \
                          (table, start_key, ts_region_id, column_family, ping, avg_value, ratio)
                logger.warn(content)
            else:
                logger.info("One region of table:%s request_ping:%s avg_ping:%s. NO ALARM!" % (table, ping, avg_value))


if __name__ == '__main__':
    deal_and_alarm(log_file=CANARY_LOG_PATH)
