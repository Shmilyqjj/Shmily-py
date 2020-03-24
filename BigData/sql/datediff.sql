# Mysql的datediff函数使用
# datediff 函数返回两个日期之间的天数  datediff(x,y) 天数为：x-y  注意顺序

select DATEDIFF('2019-10-9','2019-10-8');   # 返回1

select datediff(submitTime,now()) from student.orderform;

select * from student.orderform where datediff(now(), submitTime) = 2488;

select * from student.orderform having datediff(now(), submitTime) = 2488;

select *,datediff(now(),TDate) from student.teacher;


