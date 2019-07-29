import requests,re
if __name__ == '__main__':
    url = 'https://read.qidian.com/chapter/qrqmtYSE7XFmzDX0o03xsg2/LOibR1_EzCTgn4SMoDUcDQ2'
    html = requests.get(url).text
    reg = r'''<h3 class="j_chapterName">(.*)</h3>
                <div class="text-info cf">
                <div class="info fl">.*</div>
            <div class="read-content j_readContent">(.*)</div>

            <div class="admire-wrap">.*<a id="j_chapterNext" href="(.*)" data-eid="qd_R109" >下一章</a>.*'''
    result = re.findall(reg, html, re.S)
    print(html)
    print(result)