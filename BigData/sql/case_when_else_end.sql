-- select case 值 WHEN 表达式1 THEN 结果1 WHEN 表达式2 THEN 结果2 ELSE 结果3 END;
-- select case when 表达式1 THEN 值或字段名 WHEN 表达式2 THEN 结果2；
-- select case when 表达式1 THEN 值或字段名 WHEN 表达式2 THEN 结果2 as alias；
SELECT CASE 2 WHEN 1 THEN 'one' WHEN 2 THEN 'two' ELSE 'more' END;

SELECT CASE WHEN 1>0 THEN 'true' ELSE 'false' END;

SELECT CASE 'qjj' WHEN 'qq' THEN false WHEN 'qjj' THEN true ELSE 'more' END;

select name,
case when money>800 then money else 0 end as m
from store having m != 0;
