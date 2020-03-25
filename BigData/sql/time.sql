计算时间必备的相关函数


select year(now());  # 第几年
select dayofyear(now()) # 一年中第几天


select week(now());  # 今年的第几周
select weekday(now());  # 函数返回一个日期的工作日索引值  (星期一为0，星期二为1，星期日为6)
select weekofyear(now())  # weekofyear函数是计算出当前日期所在周数
select yearweek(now(),1)  # 返回年和第几周  格式：202013
select dayofweek(now())  # 周日为每周的第一天，获取结果为这周的第几天


select month(now())  # 今年的第几个月
select monthname(now())  # 返回英文  如3月 返回 March
select dayofmonth(now())  # 这个月的第几天

select day(now())  # 这个月的第几天
select dayname(now())  # Wednesday
select current_date(),now()  # current_date时间精确到day
select sysdate() # 获取当前系统时间
select utc_timestamp()  # 获取utc时间 当前的减8小时

select hour(now())
select minute(now())
select second(now())
select microsecond(now())


select date_add(now(), interval -2 day)   # 2天前
select date_add(now(), interval -1 week)  # 一周前
select date_add(now(), interval 10 year)  # 十年后
 # DATE_ADD函数向日期添加指定的时间间隔,语法DATE_ADD(date,INTERVAL expr type)
--参数类型：
--MICROSECOND
--SECOND
--MINUTE
--HOUR
--DAY
--WEEK
--MONTH
--QUARTER
--YEAR
--SECOND_MICROSECOND
--MINUTE_MICROSECOND
--MINUTE_SECOND
--HOUR_MICROSECOND
--HOUR_SECOND
--HOUR_MINUTE
--DAY_MICROSECOND
--DAY_SECOND
--DAY_MINUTE
--DAY_HOUR
--YEAR_MONTH


select date_sub(now(),interval -1 year)  # -(-1年) 负负得正
# DATE_SUB() 函数从日期减去指定的时间间隔。参数与date_add相同

