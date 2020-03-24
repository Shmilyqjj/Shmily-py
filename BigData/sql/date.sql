# Mysql DATE(date)  date 参数是合法的日期表达式。
# 如果date是date类型则无变化  如果是varchar等类型，转为date类型


select submitTime from student.orderform;

select DATE(submitTime) from student.orderform;



select TDate from student.teacher;

select DATE(TDate) from student.teacher;

