-- sql函数之 concat concat_ws group_concat

--CREATE TABLE `concat_test`  (
--  `id` int(11) NOT NULL,
--  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
--  `last_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
--  `first_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
--  PRIMARY KEY (`id`) USING BTREE
--) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;
--
--INSERT INTO `concat_test` VALUES (1, 'qjj', 'q', 'jj');
--INSERT INTO `concat_test` VALUES (2, 'zxw', 'z', 'xw');
--INSERT INTO `concat_test` VALUES (3, 'fzz', 'f', 'zz');
--INSERT INTO `concat_test` VALUES (4, 'gjj', 'g', 'jj');
--INSERT INTO `concat_test` VALUES (5, 'test', 't', 'est');
--INSERT INTO `concat_test` VALUES (6, 'has_null', null, null);
--insert concat_test values(7,'younull',null,null);
--INSERT INTO `concat_test` VALUES (8, 'qjj', 'qq', 'jjj');
--INSERT INTO `concat_test` VALUES (9, 'qjj', 'qqq', 'jjjj');
--
--commit;


--1.concat  返回结果为连接参数产生的字符串，如果有任何一个参数为null，则返回值为null。
select concat(id,'-',name,'-',first_name,'-',last_name) from concat_test where id <= 5;
select concat(id,'-',name,'-',first_name,'-',last_name) from concat_test where id > 5;


--2.concat_ws 上边的concat 每个字段之间加了'-'，如果n个字段就要n-1个'-'很麻烦，所以concat_ws可以一次性指定分隔符 语法：concat_ws(separator, str1, str2, ...)
select concat_ws('-',id,name,first_name,last_name) from concat_test where id <= 5;
select concat_ws(null,id,name,first_name,last_name) from concat_test where id <= 5;  -- 分隔符不能为null  分隔符为null结果为null
select concat_ws('-',id,name,first_name,last_name) from concat_test where id > 5;  --参数为null则那部分输出null，不为null的参数照常显示


--3.group_concat  将group by产生的同一个分组中的值连接起来，返回一个字符串结果。
-- 语法：group_concat( [distinct] 要连接的字段 [order by 排序字段 asc/desc ] [separator '分隔符'] )
-- 如果返回值出现BLOB/CLOB类型，强转为char类型
select name,group_concat(id) as gc from concat_test group by name;
select name,cast(group_concat(id) as char) as gc from concat_test group by name;

-- 拼接时用'-'连接
select name,cast(group_concat(id separator '-') as char) as gc from concat_test group by name;

-- 拼接时按id大小升序排序并用'-'连接
select name,cast(group_concat(id order by id asc separator '-') as char) as gc from concat_test group by name;

-- 拼接时按去重后id大小升序排序并用'-'连接
select name,cast(group_concat(distinct id order by id asc separator '-') as char) as gc from concat_test group by name;