-- sql if判断
-- IF(expr1,expr2,expr3)
-- If expr1 is TRUE (expr1 <> 0 and expr1 <> NULL) then IF() returns expr2; otherwise it returns expr3. IF() returns a numeric or string value, depending on the context in which it is used.


select if(1>2,2,3);
select if(1<2,'yes','no');

-- STRCMP(str1,str2)  比较两个字符串，如果这两个字符串相等返回0，如果第一个参数是根据当前的排序顺序比第二较小则返回-1，否则返回1。
select STRCMP('test','test1');

select if(STRCMP('test','test1'),'no','yes');
select if(0,'no','yes');
select if(null,'no','yes');