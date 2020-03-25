ROW_NUMBER()  RANK()  DENSE_RANK()  NTILE()
这三个函数的区别主要在分数一致的情况下
row_number()不重复排名
rank()重复且跳跃数字排名 eg: 1 2 3 3 3 6 7 8 9  跳跃排名最终总数不变
dense_rank()重复且不跳跃数字排名。  eg:1 2 3 3 3 4 5 6  不跳跃 总数改变
NTILE() 将有序分区中的行分发到指定数目的组中，各个组有编号，编号从1开始，就像我们说的’分区’一样 ，分为几个区，NTILE的值为分区号.(它把有序的数据集合平均分配到指定的数量（num）个桶中, 将桶号分配给每一行。如果不能平均分配，则优先分配较小编号的桶，并且各个桶中能放的行数最多相差1。)

测试数据：
0.csv
id,name,class,score
1,张飞,1,100
2,刘备,1,99
3,李逵,1,95
4,小动,1,97
5,小智,1,80
6,吕布,2,67
7,赵云,2,90
8,典韦,2,89
9,关羽,2,70
10,马超,2,98
11,张媛,1,100
12,元歌,2,100
12,后裔,3,90
12,大乔,3,90
12,小乔,3,90


use pyspark-sql 2.4

df = spark.read.csv('D:/spark/0.csv', header=True, encoding='utf8',inferSchema=True)
df.registerTempTable('tb')
spark.sql("""
select *,NTILE(3) over(order by score desc) area_number from tb
""").show(1000,False)


# 得到按成绩从高到底降序排序并且 加排名r  分数一样的名词不一样
select id,name,class,score,row_number() over(order by score desc) r from tb

# 每个班级内排名
select id,name,class,score,row_number() over(partition by class order by score desc) r from tb

# 每个班级内排名前三
select * from(
select id,name,class,score,row_number() over(partition by class order by score desc) r from tb
) t where t.r <= 3

# 注意select语句中的别名 不能用作where和having的条件


跳跃排名：
select *,rank() over(order by score desc) from tb

不跳跃排名
select *,dense_rank() over(order by score desc) from tb

# NTILE()分区
select *,NTILE(3) over(order by score desc) area_number from tb  # 将所有数据分三个区


题：
--列出每个班分数排名前三的学生
    select * from (select id, name, class, score ,
                row_number() over (partition by class order by score desc) as r1,
                rank() over (partition by class order by score desc) as r2 ,
                dense_rank() over (partition by class order by score desc) as r3 from te.sc) B where r1<=3 ;

Tips：
使用rank over()的时候，空值是最大的，如果排序字段为null, 可能造成null字段排在最前面，影响排序结果。
可以这样： rank over(partition by course order by score desc nulls last)