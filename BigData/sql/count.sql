-- count(*) count(0) count(1) 没有区别，都会统计包含null的值的项
-- 但 count(field) 则会在查询字段时忽略字段值为null的项。
-- 统计表长时，用count(*) 就可以了，但要统计字段时，需要注意这个问题。

select count(1) from course;
select count(0) from course;
select count(*) from course;
select count(sid) from course;