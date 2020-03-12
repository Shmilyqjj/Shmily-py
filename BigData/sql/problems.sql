-- 一些sql题目

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


--2.