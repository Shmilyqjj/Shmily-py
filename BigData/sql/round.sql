-- ROUND函数：用于把数值字段舍入为指定的小数位数。
-- SELECT ROUND(column_name,decimals) FROM table_name;  注：decimals表名 返回的小数位数
-- 规则：四舍五入

DROP TABLE IF EXISTS `scores`;
CREATE TABLE `scores`  (
  `s_id` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `c_id` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `s_score` double NULL DEFAULT NULL,
  PRIMARY KEY (`s_id`, `c_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
INSERT INTO scores(s_id,c_id,s_score) VALUES(1,1,85.5);
INSERT INTO scores(s_id,c_id,s_score) VALUES(2,2,89.5);
INSERT INTO scores(s_id,c_id,s_score) VALUES(3,3,96.7);

-- 使用ROUND
select ROUND(avg(s_score),3) from scores;

select ROUND(avg(s_score),10) from scores;