#!/usr/bin/env python
# encoding: utf-8
"""
: crontab调度 自动拉起Yarn应用
:Author: shmily
:Create Time: 2023/1/10 下午2:45
:@File: auto-restart-app.py
:@Software: PyCharm
:@Site: shmily-qjj.top
:调度 crontab

{
#     "msgtype": "markdown",
#     "markdown": {"title": "忽略该告警谢谢",
#                  "text": "# 任务xxx挂了自动重启 \n## 二级标题 \n> 引用文本  \n**加粗**  \n*斜体*  \n[url](https://www.baidu.com) "
#                          "\n![草莓](https://dss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=1906469856,4113625838&fm=26&gp=0.jpg) "
#                          "\n- 无序列表 \n1.有序列表  \n@某手机号主 @18688889999"},
#     "at": {
#         "atMobiles": [18688889999],
#         "isAtAll": False}  # 是否@所有人
# }
"""
import json
import requests
import logging
import subprocess as commands
import time
import datetime
import hmac
import hashlib
import base64
import urllib.parse
import socket
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

APP_TYPE = "Apache Flink"
YARN_RM_URL = "http://rm_host:8088"  # 主备均可
# 钉钉告警机器人
DING_URL = "https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxxxxxxx"
DING_SEC = "xxxxxxxxxxx"


class App:
    def __init__(self, name, run_script, owner):
        self.name = name
        self.run_script = run_script
        self.owner = owner
        self.hostname = socket.gethostname()

    def app_desc(self):
        return "App: %s - Owner: %s - RunScript:%s - Host: %s" % (self.name, self.owner, self.run_script, self.hostname)


# yarnApp 名称,执行脚本,负责人
APPS = [
    App("flink_iceberg_rcv5_t_20161_3", "kinit -kt /path/to/etl.keytab etl;/path/to/t_20161_3_rcv5.sh", "qjj"),
    App("flink_iceberg_rcv5_odl_pay_order", "kinit -kt /path/to/etl.keytab etl;/path/to/odl_pay_order.sh", "qjj"),
    App("flink_iceberg_rcv5_t_17_3", "kinit -kt /path/to/etl.keytab etl;/path/to/t_17_3_rcv5.sh", "qjj"),
    App("flink_iceberg_rcv5_t_20120_3", "kinit -kt /path/to/etl.keytab etl;/path/to/t_20120_3_rcv5.sh", "qjj"),
    App("flink_iceberg_rcv5_t_19_3", "kinit -kt /path/to/etl.keytab etl;/path/to/t_19_3_rcv5.sh", "qjj"),
    App("flink_iceberg_rcv5_t_30229_3", "kinit -kt /path/to/etl.keytab etl;/path/to/t_30229_3_rcv5.sh", "qjj"),
    App("flink_iceberg_rcv5_t_20153_3", "kinit -kt /path/to/etl.keytab etl;/path/to/t_20153_3_rcv5.sh", "qjj")
]


def exec_linux_cmd(cmd: str):
    # 执行Linux命令
    stat, output = commands.getstatusoutput(cmd)
    if stat == 0:
        logger.info("Command executed successfully.Command: %s" % cmd)
        return True
    else:
        logger.error("Command failed with output " + output)
        return False


def send_dingtalk(ding_url: str, secret: str, alert_str, at_mobiles=None, at_all=False):
    # 发送钉钉
    if at_mobiles is None:
        at_mobiles = []
    timestamp = str(round(time.time() * 1000))
    string_to_sign_enc = '{}\n{}'.format(timestamp, secret).encode('utf-8')
    hmac_code = hmac.new(secret.encode('utf-8'), string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }
    data = {
        "msgtype": "markdown",
        "markdown": {"title": "任务自动拉起告警",
                     "text": alert_str},
        "at": {
            "atMobiles": at_mobiles,
            "isAtAll": at_all}  # 是否@所有人
    }
    send_data = json.dumps(data).encode("utf-8")
    resp = requests.post(ding_url + '&timestamp={}&sign={}'.format(timestamp, sign), send_data, headers=header)
    if resp.status_code == 200:
        logger.info("Alert message %s sent successfully." % alert_str)
    else:
        logger.error("Alert message %s sent failed." % alert_str)


if __name__ == '__main__':
    url = "%s/ws/v1/cluster/apps?states=RUNNING" % YARN_RM_URL
    if APP_TYPE != "":
        url = url + "&&applicationTypes=" + APP_TYPE.replace(" ", "%20")
    res = requests.get(url)

    if res.status_code == 200:
        app_details = res.json().get("apps").get("app")
        if app_details is not None:
            app_list = list(map(lambda x: x.get("name"), app_details))
            for app in APPS:
                if app.name not in app_list:
                    logger.warning("[%s] is not running.Now restart." % app.app_desc())
                    if exec_linux_cmd("sh " + app.run_script):
                        send_dingtalk(
                            DING_URL,
                            DING_SEC,
                            "## 任务%s失败,已自动拉起成功,告警忽略\n " % app.name +
                            "### 负责人: %s \n " % app.owner +
                            "### 时间: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
                    else:
                        send_dingtalk(
                            DING_URL,
                            DING_SEC,
                            "# 任务%s失败,自动拉起失败,请关注\n " % app.name +
                            "### 负责人: %s \n " % app.owner +
                            "### 时间: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") +
                            "\n ### 启动脚本: %s[所在节点%s]" % (app.run_script, app.hostname))
                else:
                    logger.info("App %s is running." % app.name)
        else:
            logger.error("Err: Yarn app info is none.")
            send_dingtalk(DING_URL, DING_SEC, "# 自动拉起程序异常 \n Err:Yarn app info is none.")
    else:
        err_msg = "Cannot request yarn rest api, status code is %s, result is %s" % (res.status_code, res.text.encode("utf-8"))
        logger.error(err_msg)
        send_dingtalk(DING_URL, DING_SEC, "# 自动拉起程序异常 \n Err: " + err_msg)
