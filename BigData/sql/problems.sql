-- 一些sql题目

-- *********************************************************************************************************************

--1.根据不同的数据集判断出最优秀的学生
-- 输入
-- 表S，表结构：
-- st_id bigint comment "学生id"
-- ,st_name varchar(30) comment "学生姓名"
-- ,score int comment "分数"
-- ,pro_type varchar(20) comment "题目类型p1~p5"
-- ,start_time datetime comment "答题开始时间"
-- 输出
-- 最终只输出一条数据，最优秀的学生的学生id和姓名
-- create table S(
-- st_id bigint comment "学生id",
-- st_name varchar(30) comment "学生姓名",
-- score int comment "分数",
-- pro_type varchar(20) comment "题目类型p1~p5",
-- start_time datetime comment "答题开始时间"
-- );

-- insert into S(st_id,st_name,score,pro_type,start_time) values(1,'T',10,'p1','2019-08-22 10:09:13');
-- insert into S(st_id,st_name,score,pro_type,start_time) values(1,'T',8,'p2','2019-08-22 10:09:17');
-- insert into S(st_id,st_name,score,pro_type,start_time) values(1,'T',9,'p3','2019-08-22 10:09:37');
-- insert into S(st_id,st_name,score,pro_type,start_time) values(1,'T',5,'p4','2019-08-22 10:10:25');
-- insert into S(st_id,st_name,score,pro_type,start_time) values(1,'T',2,'p5','2019-08-22 10:12:30');
-- insert into S(st_id,st_name,score,pro_type,start_time) values(2,'L',9,'p1','2019-08-22 11:29:22');
-- insert into S(st_id,st_name,score,pro_type,start_time) values(2,'L',9,'p2','2019-08-22 11:29:30');
-- insert into S(st_id,st_name,score,pro_type,start_time) values(2,'L',7,'p3','2019-08-22 11:29:53');
-- insert into S(st_id,st_name,score,pro_type,start_time) values(2,'L',3,'p4','2019-08-22 11:32:20');
-- insert into S(st_id,st_name,score,pro_type,start_time) values(2,'L',0,'p5','2019-08-22 11:34:07');
-- insert into S(st_id,st_name,score,pro_type,start_time) values(3,'W',10,'p1','2019-08-22 11:34:03');
-- insert into S(st_id,st_name,score,pro_type,start_time) values(3,'W',9,'p2','2019-08-22 11:34:08');
-- insert into S(st_id,st_name,score,pro_type,start_time) values(3,'W',9,'p3','2019-08-22 11:34:26');
-- insert into S(st_id,st_name,score,pro_type,start_time) values(3,'W',4,'p4','2019-08-22 11:35:01');
-- insert into S(st_id,st_name,score,pro_type,start_time) values(3,'W',2,'p5','2019-08-22 11:36:12');
-- insert into S(st_id,st_name,score,pro_type,start_time) values(4,'X',10,'p1','2019-08-22 11:39:10');
-- insert into S(st_id,st_name,score,pro_type,start_time) values(4,'X',8,'p2','2019-08-22 11:39:17');
-- insert into S(st_id,st_name,score,pro_type,start_time) values(4,'X',8,'p3','2019-08-22 11:39:41');
-- insert into S(st_id,st_name,score,pro_type,start_time) values(4,'X',5,'p4','2019-08-22 11:41:15');
-- insert into S(st_id,st_name,score,pro_type,start_time) values(4,'X',3,'p5','2019-08-22 11:43:59');

-- 答案：
select st_id,st_name from
(
select st_id,st_name,sum(score*substr(pro_type,2,2))/(max(start_time)-min(start_time)) sums from s  group by st_id order by sums desc limit 1
) temp;

-- *********************************************************************************************************************

--2.有商品价格表goods_price,其中id是自增主键，goods_id是商品id，cate_id是商品分类，price价格
--create table goods_price(
--	id int primary key auto_increment,
--	goods_id VARCHAR(255),
--	cate_id VARCHAR(255),
--	price DOUBLE
--);
--
--INSERT INTO goods_price(id,goods_id,cate_id,price) VALUES(1,'100000001','101',59.2);
--INSERT INTO goods_price(id,goods_id,cate_id,price) VALUES(2,'100000002','101',34.55);
--INSERT INTO goods_price(id,goods_id,cate_id,price) VALUES(3,'100000003','102',128.9);
--INSERT INTO goods_price(id,goods_id,cate_id,price) VALUES(4,'100000004','102',18.5);
--INSERT INTO goods_price(id,goods_id,cate_id,price) VALUES(5,'100000005','102',169.44);
--INSERT INTO goods_price(id,goods_id,cate_id,price) VALUES(6,'100000006','103',77.7);
-- （1）计算每一个商品分类下的商品数和商品平均价格
select cate_id,count(*) as count,round(avg(price),4) from goods_price group by cate_id;


-- （2）定义每一个商品的价格除以其所属类目的均价为该商品的价格比例，将所有商品按价格比例从小到大排序，取TOP3的商品，输出商品ID，商品价格，类目平均价格以及价格比例。
select * from
(
select a.id,a.goods_id,a.price,b.avg_price as avg_price,a.price/b.avg_price as ratio from goods_price a left join
(select cate_id,round(avg(price),4) as avg_price from goods_price group by cate_id) b on a.cate_id=b.cate_id
)a order by ratio  limit 3;

-- *********************************************************************************************************************

--3.一张学生表 ID,学号,课程,成绩 数据如下，求所有数学成绩大于语文成绩的学生的学号：
--create table course(
--	id int,
--	sid int,
--	course varchar(255),
--	score int
--);
--insert into course(id,sid,course,score) values(1,1,'语文',50);
--insert into course(id,sid,course,score) values(2,1,'数学',70);
--insert into course(id,sid,course,score) values(3,2,'语文',79);
--insert into course(id,sid,course,score) values(4,2,'数学',83);
--insert into course(id,sid,course,score) values(5,3,'语文',76);
--insert into course(id,sid,course,score) values(6,3,'数学',20);
--commit;
--答案：
select t_math.sid from
(select sid,score from course where course = '数学') t_math
join
(select sid,score from course where course = '语文') t_chinese
on t_math.sid = t_chinese.sid where t_math.score > t_chinese.score;

--解法2：
select a.sid
  from (select * from course where course = '语文') a,
       (select * from course where course = '数学') b
 where a.sid = b.sid
   and a.score < b.score;

-- *********************************************************************************************************************

--4.现有一张店铺表store，包括字段（店铺名，月份，金额）求每个店铺当月销售额和累计到当月的销售总额：
--create table store(
--	name varchar(255),
--	month varchar(255),
--	money int
--);
--
--insert into store(name,month,money) values('a','2019-1','100');
--insert into store(name,month,money) values('a','2019-1','200');
--insert into store(name,month,money) values('b','2019-1','300');
--insert into store(name,month,money) values('b','2019-1','500');
--insert into store(name,month,money) values('c','2019-1','300');
--insert into store(name,month,money) values('c','2019-1','400');
--insert into store(name,month,money) values('a','2019-2','500');
--insert into store(name,month,money) values('a','2019-2','200');
--insert into store(name,month,money) values('b','2019-2','800');
--insert into store(name,month,money) values('b','2019-2','700');
--insert into store(name,month,money) values('c','2019-2','900');
--insert into store(name,month,money) values('c','2019-2','1000');
--insert into store(name,month,money) values('a','2019-3','300');
--insert into store(name,month,money) values('a','2019-3','100');
--commit;
--解法：
select a.*,b.total_money from
(
select name,sum(money) as monthly_money,month from store group by name,month
) a
join
(select name,sum(money) as total_money from store group by name) b
on a.name=b.name;

-- 解法2：
select
a.*, b.total_money
from
(select name,sum(money) as monthly_money,month from store group by name,month) a,
(select name,sum(money) as total_money from store group by name) b
where a.name = b.name;

-- *********************************************************************************************************************

--5.sql练习50题：
-- 参考：https://blog.csdn.net/fashion2014/article/details/78826299
CREATE TABLE `Student`(
	`s_id` VARCHAR(20) COMMENT '学生编号',
	`s_name` VARCHAR(20) NOT NULL DEFAULT '' COMMENT '学生姓名',
	`s_birth` VARCHAR(20) NOT NULL DEFAULT '' COMMENT '出生年月',
	`s_sex` VARCHAR(10) NOT NULL DEFAULT '' COMMENT '学生性别',
	PRIMARY KEY(`s_id`)
)comment='学生表';

CREATE TABLE `Course`(
	`c_id`  VARCHAR(20) COMMENT '课程编号',
	`c_name` VARCHAR(20) NOT NULL DEFAULT '' COMMENT '课程名称',
	`t_id` VARCHAR(20) NOT NULL COMMENT '教师编号',
	PRIMARY KEY(`c_id`)
)comment='课程表';

CREATE TABLE `Teacher`(
	`t_id` VARCHAR(20) COMMENT '教师编号',
	`t_name` VARCHAR(20) NOT NULL DEFAULT '' COMMENT '教师姓名',
	PRIMARY KEY(`t_id`)
)comment='教师表';

CREATE TABLE `Score`(
	`s_id` VARCHAR(20) COMMENT '学生编号',
	`c_id`  VARCHAR(20) COMMENT '课程编号',
	`s_score` INT(3) COMMENT '分数',
	PRIMARY KEY(`s_id`,`c_id`)
)comment='成绩表';

-- 插入学生表测试数据
insert into Student values('01' , '佳境' , '1990-01-01' , '男');
insert into Student values('02' , '王八' , '1990-12-21' , '男');
insert into Student values('03' , '博文' , '1990-05-20' , '男');
insert into Student values('04' , '德毅' , '1990-08-06' , '男');
insert into Student values('05' , '晓文' , '1991-12-01' , '女');
insert into Student values('06' , '哲哲' , '1992-03-01' , '女');
insert into Student values('07' , '李欣' , '1989-07-01' , '女');
insert into Student values('08' , '哎呦' , '1990-01-20' , '女');
-- 课程表测试数据
insert into Course values('01' , '计网' , '02');
insert into Course values('02' , '计组' , '01');
insert into Course values('03' , '编程' , '03');

-- 教师表测试数据
insert into Teacher values('01' , '高龙');
insert into Teacher values('02' , '唐光义');
insert into Teacher values('03' , '张亚楠');


-- 成绩表测试数据
insert into Score values('01' , '01' , 80);
insert into Score values('01' , '02' , 90);
insert into Score values('01' , '03' , 99);
insert into Score values('02' , '01' , 70);
insert into Score values('02' , '02' , 60);
insert into Score values('02' , '03' , 80);
insert into Score values('03' , '01' , 80);
insert into Score values('03' , '02' , 80);
insert into Score values('03' , '03' , 80);
insert into Score values('04' , '01' , 50);
insert into Score values('04' , '02' , 30);
insert into Score values('04' , '03' , 20);
insert into Score values('05' , '01' , 76);
insert into Score values('05' , '02' , 87);
insert into Score values('06' , '01' , 31);
insert into Score values('06' , '03' , 34);
insert into Score values('07' , '02' , 89);
insert into Score values('07' , '03' , 98);
insert into Score values('08' , '02' , 98);
insert into Score values('08' , '03' , 98);

COMMIT;

-- 求：查询"01"课程比"02"课程成绩高的学生的 信息及课程分数
SELECT s.s_id,s.s_name,s.s_birth,s.s_sex,a.s_score as score01,b.s_score as score02
from student s,score a,score b
where s.s_id = a.s_id
and s.s_id = b.s_id
and a.c_id='01'
and b.c_id='02'
and a.s_score > b.s_score;
-- 或者
select s.*,a.s_score as score_01,b.s_score as score_02
from student s
join score a
on s.s_id = a.s_id
left join score b
on a.s_id = b.s_id
where a.c_id = '01'
and b.c_id = '02'
and a.s_score > b.s_score;

-- 求：查询"01"课程比"02"课程成绩低的学生的信息及课程分数
select s.*,a.s_score as score_01,b.s_score as score_02
from student s
left join score a
on a.s_id = s.s_id
left join score b
on a.s_id = b.s_id
and a.c_id = '01'
and b.c_id = '02'
where a.s_score < b.s_score;

-- 求：查询平均成绩大于等于60分的同学的学生编号和学生姓名和平均成绩
select a.s_id,a.s_name,round(avg(b.s_score),2) as avg
from student a
left join score b
on a.s_id = b.s_id
group by a.s_name
having avg >= 60;


-- 求：查询平均成绩小于60分的同学的学生编号和学生姓名和平均成绩(包括有成绩的和无成绩的)
select a.s_id,a.s_name,round(avg(b.s_score),2) as avg
from student a,score b
where a.s_id = b.s_id
group by a.s_id having avg < 60;

-- 求：查询所有同学的学生编号、学生姓名、选课总数、所有课程的总成绩
select s.s_id,s.s_name,count(*) as total_course,sum(score.s_score) as total_score
from student s
join score
on s.s_id = score.s_id
group by s.s_id,s.s_name;

-- 求：查询"唐"姓老师的数量
select count(*) from teacher where t_name like '唐%';

-- 求：查询学过"唐光义"老师授课的同学的信息
select s.*
from student s,teacher t,course c,score
where score.c_id = c.c_id
and s.s_id = score.s_id
and c.t_id = t.t_id
and t.t_name = '唐光义';
-- 或：
select s.*
from student s
left join score
on s.s_id = score.s_id
left join course c
on c.c_id = score.c_id
left join teacher t
on t.t_id = c.t_id
where t.t_name = '唐光义';
-- 或：
select s.*
from student s
join score
on s.s_id = score.s_id
where score.c_id in
(
    select c_id
    from course
    where t_id
    in
    (
        select t_id
        from teacher
        where t_name = '唐光义'
    )
);

-- 求：查询没学过"唐光义"老师授课的同学的信息
select * from student where s_id not in
(
    select s_id from score where c_id in
    (
        select c_id from course c left join teacher t on c.t_id = t.t_id where t.t_name = '唐光义'
    )
);
-- 或：
select *
from student
where s_id not in
(
    select if(t.t_name = '唐光义', s_id, null) as s_id
    from score s,course c,teacher t
    where s.c_id = c.c_id
    and c.t_id = t.t_id
    having s_id is not null
);

-- 求：查询学过编号为"01"并且也学过编号为"02"的课程的同学的信息
select a.* from
student a,score b,score c
where a.s_id = b.s_id  and a.s_id = c.s_id and b.c_id='01' and c.c_id='02';


-- 求：查询学过编号为"01"但是没有学过编号为"02"的课程的同学的信息
select s.*
from student s
where s.s_id in (select s_id from score where c_id = '01')
and s.s_id not in (select s_id from score where c_id = '02');

-- 求：查询没有学全所有课程的同学的信息
select s.*
from student s
left join score
on score.s_id = s.s_id
group by s.s_id
having count(score.c_id) <
(
    select count(*) from course
);
-- 或：
select * from student
where s_id not in
(
    select s_id from score
    group by s_id
    having count(s_id) =
    (select count(1) from course)
);

-- 求：查询至少有一门课与学号为"01"的同学所学相同的同学的信息
select * from student
where s_id != '01'
and s_id in
(
    select s_id from score where score.c_id in
    (
        select c_id from score where score.s_id = '01'
    )
);


-- 求：查询和"01"号的同学学习的课程完全相同的其他同学的信息
select * from student
where s_id in
(
select s_id from
(
select s_id,cast(group_concat(c_id order by c_id asc separator '-') as char) c_id_group from score where s_id != '01' group by s_id
) a
right join
(
select cast(group_concat(c_id order by c_id asc separator '-') as char) c_id_group from score where s_id = '01'
) b on a.c_id_group = b.c_id_group
);

-- 求：查询没学过"唐光义"老师讲授的任一门课程的学生姓名
select s.s_name
from student s
where s.s_id not in
(
    select s_id
    from score s,teacher t,course c
    where c.c_id = s.c_id
    and t.t_id = c.t_id
    and t.t_name = '唐光义'
);

-- 求：查询两门及其以上不及格课程的同学的学号，姓名及其平均成绩
select s.s_name,a.avg_score
from student s
join
(
    select s_id,avg(score.s_score) as avg_score from score where s_score < 60 group by s_id having count(1) >= 2
) a
on s.s_id = a.s_id;

-- 求：检索"01"课程分数小于60，按分数降序排列的学生信息
select s.*
from score
left join student s
on score.s_id = s.s_id
where c_id = '01'
and s_score < 60
order by s_score desc;

-- 求：按平均成绩从高到低显示所有学生的所有课程的成绩以及平均成绩
select s.s_id,s.s_name,
(select score.s_score from score where score.s_id = s.s_id and score.c_id = '01') as 计网,
(select score.s_score from score where score.s_id = s.s_id and score.c_id = '02') as 计组,
(select score.s_score from score where score.s_id = s.s_id and score.c_id = '03') as 编程,
(select round(avg(score.s_score),2) from score where score.s_id = s.s_id) as 平均分
from student s
group by s.s_id order by 平均分 desc;

--另一种写法： （order by n）n表示第几个字段 [行转列]
-- 行转列是指本来多行显示的数据变为一行显示 一般用 max(case when then else end) group by来实现
SELECT a.s_id,
MAX(CASE a.c_id WHEN '01' THEN a.s_score END ) 计网,
MAX(CASE a.c_id WHEN '02' THEN a.s_score END ) 计组,
MAX(CASE a.c_id WHEN '03' THEN a.s_score END ) 编程,
avg(a.s_score),b.s_name FROM Score a JOIN Student b ON a.s_id=b.s_id GROUP BY a.s_id ORDER BY 5 DESC;



-- 18.查询各科成绩最高分、最低分和平均分：以如下形式显示：课程ID，课程name，最高分，最低分，平均分，及格率，中等率，优良率，优秀率
--及格为>=60，中等为：70-80，优良为：80-90，优秀为：>=90
select score.c_id as 课程ID,c.c_name as 课程name,max(score.s_score) as 最高分, min(score.s_score) as 最低分, avg(score.s_score) as 平均分,
round((sum(case when score.s_score >= 60 then 1 else 0 end)/sum(case when score.s_score then 1 else 0 end)),2) as 及格率,
round((sum(case when score.s_score >= 70 and score.s_score <= 80 then 1 else 0 end)/sum(case when score.s_score then 1 else 0 end)),2) as 中等率,
round((sum(case when score.s_score >= 80 and score.s_score <= 90 then 1 else 0 end)/sum(case when score.s_score then 1 else 0 end)),2) as 优良率,
round((sum(case when score.s_score >= 90 then 1 else 0 end)/sum(case when score.s_score then 1 else 0 end)),2) as 优秀率
from score
left join course c
on score.c_id = c.c_id
group by score.c_id;

-- 求：按各科成绩进行排序，并显示排名
select *,row_number() over(partition by c_id order by s_score desc) r from score;

# 如果再按成绩排名前三呢？
错误写法：select *,row_number() over(partition by c_id order by s_score desc) r from score having r <= 3;因为虽然Mysql优化了having可以使用别名，但是窗口函数的别名不能使用在having中。
正确：  # 注意这个rank的别名不能叫rank 不然会报错
select * from(
select *,row_number() over(partition by c_id order by s_score desc) r from score
)tmp where tmp.r <= 3

# 查看总排名，分数一样的并列-写出跳跃排名和不跳跃排名的情况：
跳跃：select *,rank() over(order by s_score desc) r from score;

不跳跃：select *,dense_rank() over(order by s_score desc) r from score;

# 如果要查每个班的成绩排名并且成绩相同的我想让他并列名次呢？(1 2 2 2 3 4 5...）
select *,dense_rank() over(partition by c_id order by s_score desc) r from score;

# 如果结果集有null呢？
null的rank排名是最大的，影响结果 所以(nulls last)(仅spark支持)
select *,rank() over(partition by c_id order by s_score desc nulls last) from score;


-- mysql没有rank函数(8.0以后有了) 用这个写法代替：select (@i:=@i+1) as rownum,s_id from student, (select @i:=0) as init;
select s_id,c_id,s_score,@i:=@i+1 as 排名
from score,(select @i:=0) as init
order by s_score desc;

-- 求：查询学生的总成绩并进行排名
select s_id,total_score,@i:=@i+1 as 排名
from
(
    select s_id,sum(s_score) as total_score
    from score
    group by s_id
) a,
(select @i:=0) as init
order by total_score desc;


-- 求：查询不同老师所教不同课程平均分从高到低显示
-- 注意 order by可以直接加函数 方便直接按平均分排序
select c.t_id,t.t_name,s.c_id,avg(s.s_score) as avg
from course c,score s,teacher t
where c.c_id = s.c_id and t.t_id = c.t_id
group by c.c_id
order by avg desc;


-- 求：查询所有课程的成绩第2名到第3名的学生信息及该课程成绩
select d.*,c.排名,c.s_score,c.c_id from (
select a.s_id,a.s_score,a.c_id,@i:=@i+1 as 排名 from score a,(select @i:=0)s where a.c_id='01'
ORDER BY a.s_score DESC
)c
left join student d on c.s_id=d.s_id
where 排名 BETWEEN 2 AND 3
UNION
select d.*,c.排名,c.s_score,c.c_id from (
select a.s_id,a.s_score,a.c_id,@j:=@j+1 as 排名 from score a,(select @j:=0)s where a.c_id='02'
ORDER BY a.s_score DESC
)c
left join student d on c.s_id=d.s_id
where 排名 BETWEEN 2 AND 3
UNION
select d.*,c.排名,c.s_score,c.c_id from (
select a.s_id,a.s_score,a.c_id,@k:=@k+1 as 排名 from score a,(select @k:=0)s where a.c_id='03'
ORDER BY a.s_score DESC
)c
left join student d on c.s_id=d.s_id
where 排名 BETWEEN 2 AND 3;


-- 求：统计各科成绩各分数段人数：课程编号,课程名称,[100-85],[85-70],[70-60],[0-60]及所占百分比
select distinct f.c_name,a.c_id,b.`85-100`,b.百分比,c.`70-85`,c.百分比,d.`60-70`,d.百分比,e.`0-60`,e.百分比 from score a
				left join (select c_id,SUM(case when s_score >85 and s_score <=100 then 1 else 0 end) as `85-100`,
											ROUND(100*(SUM(case when s_score >85 and s_score <=100 then 1 else 0 end)/count(*)),2) as 百分比
								from score GROUP BY c_id)b on a.c_id=b.c_id
				left join (select c_id,SUM(case when s_score >70 and s_score <=85 then 1 else 0 end) as `70-85`,
											ROUND(100*(SUM(case when s_score >70 and s_score <=85 then 1 else 0 end)/count(*)),2) as 百分比
								from score GROUP BY c_id)c on a.c_id=c.c_id
				left join (select c_id,SUM(case when s_score >60 and s_score <=70 then 1 else 0 end) as `60-70`,
											ROUND(100*(SUM(case when s_score >60 and s_score <=70 then 1 else 0 end)/count(*)),2) as 百分比
								from score GROUP BY c_id)d on a.c_id=d.c_id
				left join (select c_id,SUM(case when s_score >=0 and s_score <=60 then 1 else 0 end) as `0-60`,
											ROUND(100*(SUM(case when s_score >=0 and s_score <=60 then 1 else 0 end)/count(*)),2) as 百分比
								from score GROUP BY c_id)e on a.c_id=e.c_id
				left join course f on a.c_id = f.c_id


-- 求：查询学生平均成绩及其名次
select a.s_id,
@i:=@i+1 as '不保留空缺排名',
@k:=(case when @avg_score=a.avg_s then @k else @i end) as '保留空缺排名',
@avg_score:=avg_s as '平均分'
from (select s_id,ROUND(AVG(s_score),2) as avg_s from score GROUP BY s_id ORDER BY avg_s DESC)a,(select @avg_score:=0,@i:=0,@k:=0)b;

-- 求：查询各科成绩前三名的记录
select * from(
select *,row_number() over(partition by c_id order by s_score desc) r from score
) a where a.r <= 3


-- 求：查询每门课程被选修的学生数
select c_id,count(s_id) from score a GROUP BY c_id

-- 求：查询出只有两门课程的全部学生的学号和姓名
select s.s_id,s.s_name
from student s
left join score sc
on s.s_id = sc.s_id
group by s.s_id
having count(sc.c_id) = 2;
或者：
select s_id,s_name from student
where s_id in(
select s_id from score GROUP BY s_id HAVING COUNT(c_id)=2
);

-- 求：查询男生、女生人数
select s_sex,COUNT(s_sex) as 人数  from student GROUP BY s_sex

-- 求：查询名字中含有"文"字的学生信息
select * from student where s_name like '%文%';

-- 求：查询1990年出生的学生名单
select s_name from student where s_birth like '1990%'

-- 求：查询每门课程的平均成绩，结果按平均成绩降序排列，平均成绩相同时，按课程编号升序排列
# order by可以指定多个字段不同顺序
select c_id,round(avg(s_score), 2) as avg
from score
group by c_id
order by avg desc,c_id asc

-- 求：查询平均成绩大于等于70的所有学生的学号、姓名和平均成绩
select score.s_id,s.s_name,round(avg(score.s_score),2) as avg
from student s,score
where s.s_id = score.s_id
group by s.s_id
having avg >= 70


-- 求：查询课程名称为"计网"，且分数低于60的学生姓名和分数
select s.s_name,score.s_score
from student s,score,course c
where s.s_id = score.s_id and score.c_id = c.c_id
and score.s_score < 60 and c.c_name = '计网';
或者
select s.s_name,score.s_score
from student s
left join score
on s.s_id = score.s_id
where score.s_score < 60 and score.c_id =
(select c_id from course where c_name = '计网')


-- 求：查询所有学生的课程及各科分数和总分情况；
select s.s_name,c.c_name,score.s_score,avg_table.avg,avg_table.sum
from student s,course c,score,
(select s_id,avg(s_score) as avg,sum(s_score) as sum from score group by s_id) avg_table
where s.s_id = score.s_id and c.c_id = score.c_id and s.s_id = avg_table.s_id
或：
行转列 写法：
select a.s_id,a.s_name,
SUM(case c.c_name when '计网' then b.s_score else 0 end) as '计网',
SUM(case c.c_name when '计组' then b.s_score else 0 end) as '计组',
SUM(case c.c_name when '编程' then b.s_score else 0 end) as '编程',
SUM(b.s_score) as  '总分'
from student a left join score b on a.s_id = b.s_id
left join course c on b.c_id = c.c_id
GROUP BY a.s_id


-- 求：查询任何一门课程成绩都在70分以上的姓名、课程名称和分数

select s.s_name s_name,c.c_name c_name,score.s_score s_score
from student s
left join score on s.s_id = score.s_id
left join course c on c.c_id = score.c_id
where s.s_id in
(
    select s_id from score
    where s_score > 70
    group by s_id
    having count(*) = (select count(*) from course)
)


-- 求：查询不及格的课程
select a.s_id,a.c_id,b.c_name,a.s_score from score a left join course b on a.c_id = b.c_id where a.s_score<60

-- 求：查询课程编号为01且课程成绩在80分以上的学生的学号和姓名
select a.s_id,b.s_name from score a LEFT JOIN student b on a.s_id = b.s_id where a.c_id = '01'	and a.s_score>80

-- 求：求每门课程的学生人数
select count(*) from score GROUP BY c_id;

-- 求：查询选修"唐光义"老师所授课程的学生中，成绩最高的学生信息及其成绩
select s.*,max(score.s_score)
from student s,score,course c,teacher t
where s.s_id = score.s_id and c.c_id = score.c_id and t.t_id = c.t_id
and t.t_name = '唐光义'


-- 求：查询不同课程成绩相同的学生的学生编号、课程编号、学生成绩
select DISTINCT b.s_id,b.c_id,b.s_score from score a,score b where a.c_id != b.c_id and a.s_score = b.s_score


-- 求：查询每门功成绩最好的前两名
select s_id,s_name,c_id,s_score from
(select s.s_id,s.s_name,score.c_id,score.s_score,row_number() over(partition by score.c_id order by score.s_score desc) r
from student s,score
where s.s_id = score.s_id) a
where a.r <= 2


-- 求：统计每门课程的学生选修人数（超过5人的课程才统计）。要求输出课程号和选修人数，查询结果按人数降序排列，若人数相同，按课程号升序排列
select c_id,count(*) as total from score GROUP BY c_id HAVING total>5 ORDER BY total,c_id ASC

-- 求：检索至少选修两门课程的学生学号
select s_id,count(*) as sel from score GROUP BY s_id HAVING sel>=2

-- 求：查询选修了全部课程的学生信息
select s.*,count(score.c_id) c from
student s
left join score
on s.s_id = score.s_id
group by s.s_id
having c = (select count(1) from course)
或
select * from student
where s_id in(
    select s_id from score
    GROUP BY s_id
    HAVING count(*)=(select count(*) from course)
)

-- 求：查询各学生的年龄
	-- 按照出生日期来算，当前月日 < 出生年月的月日则，年龄减一
SELECT s_birth,(DATE_FORMAT(NOW(),'%Y')-DATE_FORMAT(s_birth,'%Y')-(case when DATE_FORMAT(NOW(),'%m%d') > DATE_FORMAT(s_birth,'%m%d') then 0 else 1 end)) as age from student;


-- 求：查询本周过生日的学生
select s_name from student where weekofyear(s_birth) = weekofyear(now())

-- 求：查询下周过生日的学生
select s_name from student where weekofyear(s_birth) = weekofyear(now()) + 1

-- 求：查询本月过生日的学生
select s_name from student where month(s_birth) = month(now())

-- 求：查询下月过生日的学生
select * from student where month(s_birth) = month(now()) + 1

-- *********************************************************************************************************************

--6.一张微博表，获取互相关注的人的id：
--CREATE TABLE `weibo`  (
--  `memberid` int(255) NULL DEFAULT NULL,
--  `followerid` int(11) NULL DEFAULT NULL
--) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;
--INSERT INTO `weibo` VALUES (1, 3);
--INSERT INTO `weibo` VALUES (1, 4);
--INSERT INTO `weibo` VALUES (4, 1);
--INSERT INTO `weibo` VALUES (4, 5);
--INSERT INTO `weibo` VALUES (3, 5);

--答案：
select w1.memberid,w1.followerid from weibo w1 join weibo w2 on w1.memberid=w2.followerid and w1.followerid=w2.memberid;
--或者：
select t1.memberid,t1.followerid from weibo t1,weibo t2 where t1.memberid=t2.followerid and t1.followerid = t2.memberid;

-- *********************************************************************************************************************
--7.[Hive] sum() over()  distribute by和sort by
--现有这么一批数据，现要求出：每个用户截止到每月为止的最大单月访问次数和累计到该月的总访问次数
--三个字段的意思：
--用户名，月份，访问次数
csv_file:
user_name,month,times
A,2020-01,5
A,2020-01,15
B,2020-01,5
A,2020-01,8
B,2020-01,25
A,2020-01,5
A,2020-02,4
A,2020-02,6
B,2020-02,10
B,2020-02,5
A,2020-03,16
A,2020-03,22
B,2020-03,23
B,2020-03,10
B,2020-03,11
--
df = spark.read.csv('D:/spark/00.csv', header=True, encoding='utf8',inferSchema=True)
df.registerTempTable('hive_table')
spark.sql("""

""").show(1000,False)
--最后结果展示:
--用户	月份		最大访问次数	总访问次数		当月访问次数
--A	2020-01		        33		  33		        33
--A	2020-02		        33		  43		        10
--A	2020-03		        38		  81		        38
--B	2020-01		        30		  30		        30
--B	2020-02		        30		  45                15
--B	2020-03		        44		  89		        44

-- 答案：
select
user_name,
month,
times,
max(times) over(distribute by user_name sort by month) maxtimes,
sum(times) over(distribute by user_name sort by month) sumtimes
from
(select
user_name,
month,
sum(times) times
from hive_table
group by user_name,month) tmp

--8.[hive] 求：所有A课程成绩 大于 B课程成绩的学生的学号
csv_file:
id,stu_id,course,score
1,1,'A',43
2,1,'B',55
3,2,'A',77
4,2,'B',88
5,3,'A',98
6,3,'B',65

df = spark.read.csv('D:/spark/01.csv', header=True, encoding='utf8',inferSchema=True)
df.registerTempTable('hive_table')
spark.sql("""

""").show(10000,False)


--答案：
-- 普通做法
select a.stu_id from
(select stu_id,score from hive_table where course="'A'") a,
(select stu_id,score from hive_table where course="'B'") b
where a.stu_id=b.stu_id and a.score > b.score

-- 行转列
select stu_id from
(select stu_id,
sum(case course when "'A'" then score else 0 end) as A,
sum(case course when "'B'" then score else 0 end) as B,
from hive_table
group by stu_id
) tmp where tmp.A > tmp.B

-- 9.2010012325表示在2010年01月23日的气温为25度。现在要求使用hive，计算每一年出现过的最大气温的日期+温度
csv_File:
2014010114
2014010216
2014010317
2014010410
2014010506
2012010609
2012010732
2012010812
2012010919
2012011023
2001010116
2001010212
2001010310
2001010411
2001010529
2013010619
2013010722
2013010812
2013010929
2013011023
2008010105
2008010216
2008010337
2008010414
2008010516
2007010619
2007010712
2007010812
2007010999
2007011023
2010010114
2010010216
2010010317
2010010410
2010010506
2015010649
2015010722
2015010812
2015010999
2015011023

from pyspark.sql.types import StructType, StructField, StringType
df = spark.read.csv('D:/spark/000.csv', header=False, encoding='utf8',schema=StructType([StructField('info', StringType(), True)]))
df.registerTempTable('hive_table')
# 注意HQL里没有mid  用substr切分字符串  substr(col,start,n几个字符)
# 注意 时间转换 使用concat+substr或 from_unixtime(unix_timestamp(FIRST(a.d),'yyyymmdd'),'yyyy-mm-dd')
# 注意聚合函数 未聚合的字段想查找到，需要加FIRST()
spark.sql("""

""").show(1000,False)
-- 答案1：
select FIRST(a.d) as day,MAX(a.t) max_t from
(select CONCAT(substr(info,1,4),'-',substr(info,5,2),'-',substr(info,7,2)) as d,
substr(info,9,2) as t,
substr(info,1,4) as y
from hive_table
) a group by a.y

--答案2：
select from_unixtime(unix_timestamp(FIRST(a.d),'yyyymmdd'),'yyyy-mm-dd') as day,MAX(a.t) AS max_t from
(select substr(info,1,8) as d,
substr(info,9,2) as t,
substr(info,1,4) as y
from hive_table) a
group by a.y;

-- 10.查每个用户最近一笔交易记录的金额
CREATE TABLE `TRecent` (
  `name` varchar(20) default NULL,
  `money` float(9,2) default NULL,
  `add_date` datetime default NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

insert into TRecent VALUES('a',100.3,'2008-01-24 22:16:31');
insert into TRecent VALUES('a',103.5,'2008-04-04 10:06:15');
insert into TRecent VALUES('b',1000,'2004-06-02 01:06:24');
insert into TRecent VALUES('b',200.7,'2008-11-04 09:16:39');
insert into TRecent VALUES('c',8000,'2006-04-25 08:00:32');

-- 答案：
select a.name,a.money from student.trecent a,
(select name,max(add_date) as d from student.trecent group by name) b
where a.name=b.name and a.add_date=b.d;

select a.name,a.money from student.trecent a inner join
(select name,max(add_date) as d from student.trecent group by name) b
on a.name=b.name and a.add_date=b.d;

-- 11.现有一份以下格式的数据,表示有id为1,2,3的学生选修了课程a,b,c,d,e,f中其中几门：
csv_file:
id course
1,a
1,b
1,c
1,e
2,a
2,c
2,d
2,f
3,a
3,b
3,c
3,e

df = spark.read.csv('D:/spark/0000.csv', header=True, encoding='utf8',inferSchema=True)
df.registerTempTable('hive_table')
spark.sql("""
select id,course from hive_table distribute by id
""").show(10000,False)

-- 1.编写Hive的HQL语句来实现以下结果：(表中的1表示选修，表中的0表示未选修)
1       1       1       1       0       1       0
2       1       0       1       1       0       1
3       1       1       1       0       1       0

-- 答案1
select id,
case when course='a' then 1 else 0 end as a,
case when course='b' then 1 else 0 end as b,
case when course='c' then 1 else 0 end as c,
case when course='d' then 1 else 0 end as d,
case when course='e' then 1 else 0 end as e
from hive_table;


--答案2：
select id,
IF(course='a',1,0) as a,
IF(course='b',1,0) as b,
IF(course='c',1,0) as c,
IF(course='d',1,0) as d,
IF(course='e',1,0) as e,
IF(course='f',1,0) as f
from hive_table;

-- 2.列转行，得出每个人修的所有课，字段名为courses，课名之间用“,”隔开

select id,concat_ws(',',collect_list(course)) from hive_table group by id;
select id,course from hive4 partition by id

-- 3.如果以上面题2结果为hive_table1，求出行转列结果
https://blog.csdn.net/qq_41851454/article/details/79856627
https://www.cnblogs.com/blogyuhan/p/9274784.html