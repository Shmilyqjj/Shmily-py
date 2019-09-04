# Spark REST API监控Spark Applications运行时间
import requests
import time
def getJson(url):
    res =  requests.get(url)
    if res.status_code == 200:
        return res.json()   #等价于json.loads(res.text)

def main():
    jo = getJson("http://hadoop101:4000/api/v1/applications/")  #得到json对象的list集合
    print(type(jo))
    print(jo)
    list = jo[0]['attempts']
    print(type(list))
    st = list[0]['startTime']
    et = list[0]['endTime']
    # print(st,et)
    GMT_FORMAT = '%Y-%m-%dT%H:%M:%S.%fGMT'
    st0 = time.strptime(st, GMT_FORMAT)
    et0 = time.strptime(et,GMT_FORMAT)
    RT = time.mktime(et0)-time.mktime(st0)
    print(RT)






if __name__ == "__main__":
    main()