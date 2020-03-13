-- mysql通过查看执行计划 来判断效率
-- 语句： explain select * from table;
-- explain + xxx;

-- 辟谣count(1)和count(*)效率：
explain select count(1) from information_schema.COLUMNS;
结果：
+----+-------------+---------+------+---------------+------+---------+------+------+--------------------------------------+
| id | select_type | table   | type | possible_keys | key  | key_len | ref  | rows | Extra                                |
+----+-------------+---------+------+---------------+------+---------+------+------+--------------------------------------+
|  1 | SIMPLE      | COLUMNS | ALL  | NULL          | NULL | NULL    | NULL | NULL | Open_frm_only; Scanned all databases |
+----+-------------+---------+------+---------------+------+---------+------+------+--------------------------------------+
1 row in set (0.02 sec)


explain select count(*) from information_schema.COLUMNS;
结果：
+----+-------------+---------+------+---------------+------+---------+------+------+--------------------------------------+
| id | select_type | table   | type | possible_keys | key  | key_len | ref  | rows | Extra                                |
+----+-------------+---------+------+---------------+------+---------+------+------+--------------------------------------+
|  1 | SIMPLE      | COLUMNS | ALL  | NULL          | NULL | NULL    | NULL | NULL | Open_frm_only; Scanned all databases |
+----+-------------+---------+------+---------------+------+---------+------+------+--------------------------------------+
1 row in set (0.00 sec)

-- 所以 count(1)和count(*)效率 一样 没区别
