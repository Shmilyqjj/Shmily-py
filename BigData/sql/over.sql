SQL的OVER()函数 简直是神器
它和聚合函数的不同之处是：对于每个组返回多行
over(开窗范围)
例子
over（order by salary range between 5 preceding and 5 following）：窗口范围为当前行数据幅度减5加5后的范围内的。
over（order by salary rows between 5 preceding and 5 following）：窗口范围为当前行前后各移动5行。

over不能单独使用
要和分析函数：
ROW_NUMBER()
DENSE_RANK()
RANK()
NTILE()
和聚合函数：
COUNT()
SUM()
AVG()
MAX
MIN()
等一起使用。

# 每个课程成绩排名
select *,ROW_NUMBER() OVER(partition by c_id order by s_score desc) r from score;

# 每个课程成绩排名 跳跃排名 1 2 2 4 5 5 7....
select *,RANK() OVER(partition by c_id order by s_score desc) r from score;

# 每个课程成绩排名 非跳跃排名 1 2 2 3 4 5 5 6 ...
select *,DENSE_RANK() OVER(partition by c_id order by s_score desc) r from score;

# 数据按顺序均匀分区
select *,NTILE(3) OVER(partition by c_id order by s_score desc) r from score;

# 求每个学科每个人的成绩以及该学科平均成绩
select *,AVG(s_score) OVER(partition by c_id) c from score;

# 求每个学科每个人的成绩以及该学科总成绩
select *,SUM(s_score) OVER(partition by c_id) c from score;

# 求每个学科每个人的成绩以及该学科最高成绩
select *,MAX(s_score) OVER(partition by c_id) c from score;

# 求每个学科每个人的成绩以及该学科最低成绩
select *,MIN(s_score) OVER(partition by c_id) c from score;

# 求每个学科每个人的成绩以及学该学科的总人数
select *,COUNT(*) OVER(partition by c_id) c from score;