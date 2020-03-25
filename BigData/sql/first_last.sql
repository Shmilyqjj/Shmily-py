FIRST() 函数返回指定的字段中第一个记录的值。
LAST() 函数返回指定的字段中最后一个记录的值。

# 查班级成绩排名第一的人
select s_id,first(s_score) r from score ORDER BY s_score desc



