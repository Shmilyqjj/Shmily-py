# encoding=utf-8

# https://spark.apache.org/docs/2.2.0/monitoring.html#rest-api
# /applications/[app-id]/jobs?status=[running|succeeded|failed|unknown] list only jobs in the specific state.

# 所有job：https://yarn.intsig.net/proxy/application_1565234959424_0037/api/v1/applications/application_1565234959424_0037/jobs
import requests
import time
from requests.auth import HTTPBasicAuth

def getJSON(url,*newJobId):       # 得到JSON
    res = requests.get(url+bytes(newJobId),auth=HTTPBasicAuth('YarnAuth','AG9RiOZjXYrd'))   # 解决401权限问题
    if res.status_code == 200:
        return res.json()
    if res.text == 'unknown job: '+bytes(newJobId):
        time.sleep(1)

def getTime(JSON):      # 得到运行时间
    dict = JSON # 最新完成的job
    jobID = dict['jobId']
    subTime = dict['submissionTime']    # 2019-08-17T15:22:55.065GMT
    comTime = dict['completionTime']    # 2019-08-17T15:22:55.093GMT
    GMT_FORMAT = '%Y-%m-%dT%H:%M:%S.%fGMT'
    st = time.strptime(subTime, GMT_FORMAT)
    ct = time.strptime(comTime, GMT_FORMAT)
    return jobID,time.mktime(ct) - time.mktime(st)    # return tuple类型


def main(applicationID,newJobId):
    while True:
        Url = 'https://yarn.intsig.net/proxy/'+applicationID+'/api/v1/applications/'+applicationID+'/jobs'
        dict = getJSON(Url,newJobId)
        result = getTime(dict)
        newJobId = newJobId + 1
        print(result)


if __name__ == '__main__':
    main('application_1565234959424_0037',3164009)


