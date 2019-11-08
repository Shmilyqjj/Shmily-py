# encoding=utf-8
#https://yarn-ip/application_1565234959424_0037/api/v1/applications/application_1565234959424_0037/jobs
import  requests
import time
from requests.auth import HTTPBasicAuth



def getJSON(applicationID): #根据applicationID获得JSON
    # res = requests.get('https://yarn-ip/'+applicationID+'/api/v1/applications/'+applicationID+'/jobs?status=running',auth=HTTPBasicAuth('admin', 'admin'))
    res = requests.get('https://yarn-ip' + applicationID + '/api/v1/applications/' + applicationID + '/jobs',auth=HTTPBasicAuth('admin', 'admin'))
    if res.status_code == 200:
        return res.json()

def getRunningTime(JSON):         #最新Job的运行时间
    newJobId = JSON[0]['jobId']   #获取最新JobId
    submissionTime = JSON[0]['submissionTime']
    startTime = time.mktime(time.strptime(submissionTime,'%Y-%m-%dT%H:%M:%S.%fGMT'))+ 8*60*60
    nowTime = long(time.time())
    runTime = nowTime - startTime
    return newJobId,runTime

def getApplicationID():
    running_list = YarnSpider.get_running_apps()


def main():
    out = getRunningTime(getJSON('application_1565234959424_0037'))
    print(out)
if __name__ == '__main__':
    main()