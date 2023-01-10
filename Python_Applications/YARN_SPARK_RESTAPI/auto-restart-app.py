#!/usr/bin/env python
# encoding: utf-8
"""
: 自动拉起Yarn应用
:Author: shmily
:Create Time: 2023/1/10 下午2:45
:@File: auto-restart-app.py
:@Software: PyCharm
:@Site: shmily-qjj.top
"""
import requests
import logging
import subprocess as commands
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

APP_TYPE = "Apache Flink"
YARN_RM_URL = "http://rm_host:8088"  # 主备均可
KINIT_CMD = "kinit -kt /path/to/etl.keytab etl"

# yarnApp名: 启动脚本
APP_SCRIPT_MAP = {
    "flink_iceberg_rcv5_t_20161_3": "/path/to/t_20161_3_rcv5.sh",
    "flink_iceberg_rcv5_odl_pay_order": "/path/to/odl_pay_order.sh",
    "flink_iceberg_rcv5_t_17_3": "/path/to/t_17_3_rcv5.sh",
    "flink_iceberg_rcv5_t_20120_3": "/path/to/t_20120_3_rcv5.sh",
    "flink_iceberg_rcv5_t_19_3": "/path/to/t_19_3_rcv5.sh",
    "flink_iceberg_rcv5_t_30229_3": "/path/to/t_30229_3_rcv5.sh",
    "flink_iceberg_rcv5_t_20153_3": "/path/to/t_20153_3_rcv5.sh"
}


def exec_linux_cmd(cmd: str):
    # 执行Linux命令
    stat, output = commands.getstatusoutput(cmd)
    if stat == 0:
        logger.info("Command executed successfully.Command: %s" % cmd)
    else:
        logger.error("Command failed with output " + output)


if __name__ == '__main__':
    url = "%s/ws/v1/cluster/apps?states=RUNNING" % YARN_RM_URL
    if APP_TYPE != "":
        url = url + "&&applicationTypes=" + APP_TYPE.replace(" ", "%20")
    res = requests.get(url)

    if res.status_code == 200:
        l = res.json().get("apps").get("app")
        if l is not None:
            l = list(map(lambda x: x.get("name"), l))
            for app in APP_SCRIPT_MAP.keys():
                if app not in l:
                    logger.warning("App %s is not running.Now restart." % app)
                    app_start_script = APP_SCRIPT_MAP.get(app)
                    if KINIT_CMD != "": exec_linux_cmd(KINIT_CMD)
                    exec_linux_cmd("sh " + app_start_script)
                else:
                    logger.info("App %s is running." % app)
        else:
            logger.error("Err: app info is none.")
    else:
        logger.error("Cannot request yarn rest api, status code is %s, result is %s" %(res.status_code, res.text))
