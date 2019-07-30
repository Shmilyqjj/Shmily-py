import random
import time

#Spark项目数据生成 - 爱奇艺影视网站服务器log生成器 - 直接生成非脏数据

#生成时间
time_str=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

#reference 访问来源：
http_references=["https://www.baidu.com/s?wd={query}",
            "https://www.google.com?key={query}",
            "https://www.sougou.com/web?k={query}",
            "https://www.cn.bing.com/search?q={query}",
            "https://www.search.yahoo.com/search?p={query}"]
search_keyword=["大数据",
                "Java",
                "去上海实习",
                "去北京秋招",
                "去天津",
                "算法与数据结构",
                "《轮到你了》日剧资源",
                "bilibili官网",
                "游侠网",
                "GitHub",
                "网恋奔现",
                "Ubuntu系统"
                ]
def sample_reference():
    if random.uniform(0,1)>0.2:
        return "-"
    refer_str=random.sample(http_references,1)
    query_str=random.sample(search_keyword,1)
    return refer_str[0].format(query=query_str[0])


#status code状态码
status_code=[404,302,301,200,200]
def sample_status():
    return random.sample(status_code,1)[0]

#url地址
url_pahts = [
    "www/2",
    "www/1",
    "www/6",
    "www/3",
    "www/4",
    "pianhua/130",
    "tuokouxiu/821",
    "zangshujv/87"
]
def sample_url():
    return random.sample(url_pahts,1)[0]

#生成ip地址
ip_slices=[132,156,124,10,29,167,143,187,30,100]
def sample_ip():
    slice = random.sample(ip_slices,4)
    return ".".join( [str(item) for item in slice] )

#生成日志
def generate_log(count=10):
    while count >=1:
        query_log = "{ip}\t{localtime}\t\"GET {url} HTTP/1.0\"\t{reference}\t{status}".format(ip = sample_ip(),localtime=time_str,url=sample_url(),status=sample_status(),reference=sample_reference())

        #将日志写入文件
        f=open("D:\\GenerateLogs","a")  #a参数代表打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。
        f.write(query_log+"\n")
        print(query_log)
        count = count - 1;


if __name__ == '__main__':
    generate_log(1000000);