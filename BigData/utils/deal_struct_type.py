#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: 处理复杂结构体中的type的代码  hive 结构体类型语句处理逻辑 自动对_id这样的结构体中字段加反引号
:Owner: jiajing_qu
:Create time: 2019/12/12 10:28
"""

"""
一些场景会用到字段类型 如下面的修改注释
ALTER TABLE table_name CHANGE COLUMN muid muid_new STRING COMMENT '这里是列注释!'; 

如拼接spark ddl语句
cols.append(" `%s` %s  comment  '%s' " % (column_name, type, comment))
cols_str = ",\n  ".join(cols)
ddl = '''
CREATE  TABLE `%s`(
  %s 
)
%s
STORED AS %s;
'''% ( table_name, cols_str, part_cols_str,table_storage)

但是hive_cursor执行时如果struct类型内部字段出现'_'开头的情况就会创建失败而报错，为了兼容，如下代码对type类型做了自动处理。
"""

types = 'array<struct<_id:struct<_oid:string>,_code:int,name:string>>'
# types1 = 'bigint'
# types = types1
replace_para = []
for i in types.split('<'):
    # print(i)
    if i.startswith('_'):
        replace_para.append(i.split(':')[0])
    if len(i.split(',')) != 1:
        for j in i.split(','):
            if j.startswith('_'):
                replace_para.append(j.split(':')[0])
replace_para = set(replace_para)
# print(replace_para)
for i in replace_para:
    types = types.replace(i, "`" + i + "`")
print(types)