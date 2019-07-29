import requests
import re
#获得页面html文本
def get_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text

#获得一个list，从html中得到小说标题小说文本以及下一章的链接 - 分析html代码
def get_data(html):
    reg = r'''<h3 class="j_chapterName">(.*)</h3>
            <div class="text-info cf">.*</div>
        <div class="read-content j_readContent">(.*)</div>
         
        <div class="admire-wrap">.*<a id="j_chapterNext" href="(.*)" data-eid="qd_R109" >下一章</a>.*'''
    result = re.findall(reg,html,re.S)  #re.S是可以带着换行符匹配
    return result

def filter_Data(str):
    return re.sub(r'''<p>''',"\n",str)
    #过滤得到的文本，将<p>换成换行符

#主函数
def main(url):
    #起点网小说第一章的链接
    html = get_page(url)
    result = get_data(html)
    with open("三体全集.txt","a") as f:
        f.write(result[0][0])
        f.write(filter_Data(result[0][1]))
    #递归调用，获得后面的章节
    main("https:"+result[0][2])

if __name__ == '__main__':
    url = 'https://read.qidian.com/chapter/qrqmtYSE7XFmzDX0o03xsg2/LOibR1_EzCTgn4SMoDUcDQ2'
    main(url)
