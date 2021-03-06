# encoding=utf-8

# https://spark.apache.org/docs/2.2.0/monitoring.html#rest-api
# /applications/[app-id]/jobs?status=[running|succeeded|failed|unknown] list only jobs in the specific state.

# 所有job：https://yarn-ip/application_1565234959424_0037/api/v1/applications/application_1565234959424_0037/jobs
import requests
import time
from requests.auth import HTTPBasicAuth

count = 0 # 全局变量 记录同job running的批次数

def getJSON(url):       # 得到JSON
    res = requests.get(url,auth=HTTPBasicAuth('admin','admin'))   # 解决401权限问题
    if res.status_code == 200:
        return res.json()

def getTime(JSON):      # 得到运行时间
    dict = JSON[0]  # 最新完成的job
    jobID = dict['jobId']
    subTime = dict['submissionTime']    # 2019-08-17T15:22:55.065GMT
    comTime = dict['completionTime']    # 2019-08-17T15:22:55.093GMT
    GMT_FORMAT = '%Y-%m-%dT%H:%M:%S.%fGMT'
    st = time.strptime(subTime, GMT_FORMAT)
    ct = time.strptime(comTime, GMT_FORMAT)
    return jobID,time.mktime(ct) - time.mktime(st)    # return tuple类型


def main(applicationID,batchTime):
    baseUrl = 'https://yarn-ip/'+applicationID+'/api/v1/applications/'+applicationID+'/jobs'
     #同Job记录Running状态次数
    while True:
        if(getJSON(baseUrl+'?status=failed') != []):
            print('failed Job')  #报警-failed
        elif(getJSON(baseUrl+'?status=unknown') != []):
            print("unknown Job") #报警-unknown
        elif(getJSON(baseUrl+'?status=succeeded') != []):
            result = getTime(getJSON(baseUrl+'?status=succeeded'))
            print(result)
            if(result[1]>batchTime):
                print(result[0],result[1]-batchTime)   # 运行时长大于batchTime 预警 输出jobId和超时时间
        # elif(getJSON(baseUrl+'?status=running') != []):
        #     currentJobId = getJSON(baseUrl + '?status=running')[0]['jobId']  #当前正running的JobId
        #     global count
        #     if(getJSON(baseUrl + '?status=running')[0]['jobId'] == currentJobId):
        #         count = count + 1  #本batch时间内在运行 count自增1
        #         if(count > 3):     #超过三次batch，同一个job还在running -> 警报超时
        #             print("running timeout")
        # time.sleep(1)


if __name__ == '__main__':
    main('application_1565234959424_0037',1)