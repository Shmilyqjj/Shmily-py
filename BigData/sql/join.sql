-- join的学习

create table a(
id int,
name varchar(255)
);
create table b(
id int,
address varchar(255)
);
INSERT INTO `a`(`id`, `name`) VALUES (1, 'Google');
INSERT INTO `a`(`id`, `name`) VALUES (2, 'Taobao');
INSERT INTO `a`(`id`, `name`) VALUES (3, 'Weibo');
INSERT INTO `a`(`id`, `name`) VALUES (4, 'Facebook');
INSERT INTO `b`(`id`, `address`) VALUES (1, '美国');
INSERT INTO `b`(`id`, `address`) VALUES (3, '中国');
INSERT INTO `b`(`id`, `address`) VALUES (5, '中国');
INSERT INTO `b`(`id`, `address`) VALUES (6, '美国');




# inner join只取交集 左表右表都有的
select * from a inner join b on a.id = b.id;

# left join取全部左表的和右表满足on条件的，如果左表的行在右表中没有匹配，那么这一行右表中对应数据用NULL代替。
select a.id,a.name,b.address
from a
LEFT JOIN b
ON a.id = b.id;

select a.id,a.name,b.address
from a
LEFT JOIN b
ON a.id = b.id where address is not Null;

# right join取全部右表的和左表满足on条件的，如果右表的行在左表中没有匹配，那么这一行左表中对应数据用NULL代替。
select a.id,a.name,b.address from a right join b on a.id = b.id;
select a.id,a.name,b.address from a right join b on a.id = b.id where a.name is not NULL;


# FULL JOIN 会从左表 和右表 那里返回所有的行。如果其中一个表的数据行在另一个表中没有匹配的行，那么对面的数据用NULL代替
# mysql不支持full join 但是可以相当于 left join union right join
select a.id,a.name,b.address from a right join b on a.id = b.id
union
select a.id,a.name,b.address from a left join b on a.id = b.id;

# 取左表独有数据
select a.id,a.name,b.address from a left join b on a.id = b.id where b.id is NULL;
select a.id,a.name,b.address from a left join b on a.id = b.id where b.address is NULL;

# 取右表独有数据
select a.id as aid,b.id as bid,a.name,b.address from a right join b on a.id = b.id where a.id is NULL;

# 并集去交集
select a.id as aid,b.id as bid,a.name,b.address from a left join b on a.id = b.id where b.id is NULL
union
select a.id as aid,b.id as bid,a.name,b.address from a right join b on a.id = b.id where a.id is NULL;


