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






