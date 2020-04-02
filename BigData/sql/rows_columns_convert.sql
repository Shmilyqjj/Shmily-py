行转列  和  列转行
行转列：本来多行显示的数据变为单行显示 - 结果行数减少
列转行：本来单行显示的数据变为多列显示 - 结果行数增加

行转列：一般用MAX CASE WHEN THEN ELSE END GROUP BY来实现
列转行：一般用UNION ALL来实现

-- --------------------------------------------------------------------------------------------
行转列
测试数据：
CREATE TABLE `sales`  (
  `year` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `season` int(255) NULL DEFAULT NULL,
  `num` int(11) NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

INSERT INTO `sales` VALUES ('2014', 1, 11);
INSERT INTO `sales` VALUES ('2014', 2, 12);
INSERT INTO `sales` VALUES ('2014', 3, 13);
INSERT INTO `sales` VALUES ('2014', 4, 14);
INSERT INTO `sales` VALUES ('2015', 1, 21);
INSERT INTO `sales` VALUES ('2015', 2, 22);
INSERT INTO `sales` VALUES ('2015', 3, 23);
INSERT INTO `sales` VALUES ('2015', 4, 24);

行转列，得到如下结果
year  第一季度  第二季度 第三季度 第四季度
2014    11       12       13      14
2015    21       22       23      24

select year,
max(case season when 1 then num end) as '第一季度',
max(case season when 2 then num end) as '第二季度',
max(case season when 3 then num end) as '第三季度',
max(case season when 4 then num end) as '第四季度'
from sales group by year;

-- --------------------------------------------------------------------------------------------
列转行
测试数据：
CREATE TABLE `sales1`  (
  `year` int(255) NULL DEFAULT NULL,
  `season_1` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `season_2` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `season_3` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `season_4` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;
INSERT INTO `sales1` VALUES (2014, '11', '12', '13', '14');
INSERT INTO `sales1` VALUES (2015, '21', '22', '23', '24');
INSERT INTO `sales1` VALUES (2016, '31', '32', '33', '34');


select year,1 as season,season_1 as num from sales1
union all select year,2 as season,season_2 as num from sales1
union all select year,3 as season,season_3 as num from sales1
union all select year,4 as season,season_4 as num from sales1




