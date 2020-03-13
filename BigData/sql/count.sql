-- count(*) count(0) count(1) 没有区别，都会统计包含null的值的项
-- 但 count(field) 则会在查询字段时忽略字段值为null的项。
-- 统计表长时，用count(*) 就可以了，但要统计字段时，需要注意这个问题。

select count(1) from course;
select count(0) from course;
select count(*) from course;
select count(sid) from course;

-- count(*)的执行效率比count(col)高，因此可以用count(*)的时候就不要去用count(col)
-- count(col)的执行效率比count(distinct col)高，不过这个结论的意义不大，这两种方法也是看需要去用
-- 如果是对特定的列做count的话建立这个列的非聚集索引能对count有很大的帮助
-- 如果经常count(*)的话则可以找一个最小的col建立非聚集索引以避免全表扫描而影响整体性能
-- 在不加WHERE限制条件的情况下，COUNT(*)与COUNT(COL)基本可以认为是等价的，但是在有WHERE限制条件的情况下，COUNT(*)会比COUNT(COL)快非常多
-- count(0)=count(1)=count(*) 逻辑计划里都是 count(*)