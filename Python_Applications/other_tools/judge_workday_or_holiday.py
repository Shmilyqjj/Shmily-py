# pip install chinesecalendar -i https://pypi.douban.com/simple/
import datetime
from chinese_calendar import is_workday
# date = datetime.datetime(2021, 10, 1)
date = datetime.datetime.today()
if is_workday(date):
    print("是工作日")
else:
    print("是休息日")
