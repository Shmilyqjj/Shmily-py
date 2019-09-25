#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
:Description: 学习Phoenix
:Owner: jiajing_qu
:Create time: 2019/9/25 11:12
"""
"""
安装部署phoenix:
1.官网http://phoenix.apache.org/index.html下载对应HBase版本的phoenix
2.上传到集群 tar -zxvf apache-phoenix-4.14.3-HBase-1.3-bin.tar.gz -C /opt/module  mv重命名为phoenix (仅在主机器HMaster所在机器上操作)
3.将phoenix/phoenix-4.14.3-HBase-1.3-server.jar分发到各个集群的HBASE_HOME/lib  scp -r  ....
4.至此，完成了phoenix的安装部署

连接phoenix:
1.先启动hdfs和yarn
2.三台机器启动zookeeper  ->  /opt/module/zookeeper-3.4.13/bin/zkServer.sh start
3.主机启动hmaster -> /opt/module/hbase/bin/hbase-daemon.sh start master   
4.从机启动HregionServer -> /opt/module/hbase/bin/hbase-daemon.sh start regionserver
5.主机运行 bin/sqlline.py localhost       出现： Building list of tables and columns for tab-completion (set fastconnect to true to skip)... 即为成功

phoenix常用命令行操作：
help        查看帮助
!tables     查看所有映射表
!quit       退出
!sql        回车后输入sql语句回车

eg:
!sql
create table phoenix_table (mykey integer not null primary key, mycolumn varchar);
!sql
upsert into phoenix_table values (1,'qjj');
!sql
select * from phoenix_table
此时用HBase Shell查询
hbase shell -> list 会发现上面phoenix_table，已经转为了大写的表名 -> scan 'PHOENIX_TABLE' -> 
结果：
ROW                              COLUMN+CELL                                                                                
 \x80\x00\x00\x01                column=0:\x00\x00\x00\x00, timestamp=1569431662453, value=x                                
 \x80\x00\x00\x01                column=0:\x80\x0B, timestamp=1569431662453, value=qjj                                      
1 row(s) in 0.0230 seconds
---------------------------------------------------------------------------------------
!sql
drop table phoenix_table;
这时HBase中表也删除了
"""




import phoenixdb
import phoenixdb.cursor
ZK_URL = '10.2.5.201'
HBASE_HOST = '10.2.5.37'
HBASE_DB = 'user'

def easy_conn():
    """
    基础操作phoenix
    :return:
    """
    database_url = 'http://%s:8765/' % ZK_URL
    conn = phoenixdb.connect(database_url, autocommit=True)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE users")
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username VARCHAR)")
    cursor.execute("UPSERT INTO users VALUES (?, ?)", (1, 'qjj'))
    cursor.execute("SELECT * FROM users")
    print(cursor.fetchall()) # 只能用在select之后,fetch之后清空cursor的内容,再fetch结果为空
    # -----------------------------------------------
    cursor = conn.cursor(cursor_factory=phoenixdb.cursor.DictCursor)  # DictCursor :A cursor which returns results as a dictionary
    cursor.execute("SELECT * FROM users WHERE id=1")
    print(cursor.fetchone()['USERNAME'])


class phoenix_client:
    def __init__(self):
        self.url = ''.format(HBASE_HOST)
        self.Hbase_db = HBASE_DB


    def create_mapping(self,hbase_host,hbase_db):
        """"""
        pass#给已有的hbase表创建phoenix映射


    def pull_data(self,query_str):
        """
        拉取/查询数据
        :param query_str: 查询语句
        :return:
        """
        try:
            self.conn = phoenixdb.connect('http://%s:8765/' % ZK_URL, autocommit=True)
            self.cursor = self.conn.cursor()
            self.cursor.execute(query_str)
            all_datas = self.cursor.fetchall() # 取全部记录
            one_data = self.cursor.fetchone() # 取一条记录
            many_data = self.cursor.fetchmany(size=5) # 取五条记录
            print(all_datas)
            print(one_data)
            print(many_data)
        except Exception as e:
            print(e)
        finally:
            self.cursor.close()
            self.conn.close()


    def push_data(self,table_name,row,cf,value):
        """
        插入数据
        :param table_name: HBase映射Phoenix表名
        :param row: 列名
        :param cf:  列族
        :param value: 值
        :return:
        """
        try:
            self.conn = phoenixdb.connect('http://%s:8765/' % ZK_URL, autocommit=True)
            self.cursor = self.conn.cursor()

        except Exception as e:
            print(e)

        finally:
            self.cursor.close()
            self.conn.close()


    def exec_query(self,query_str,values = None):
        """
        执行无返回值的语句 比如upsert
        :param query_str: 查询语句 eg: UPSERT INTO users VALUES (?, ?)
        :param values: list[tuple(),tuple(),tuple()....]多个值tuple
        :return:
        """
        try:
            self.conn = phoenixdb.connect('http://%s:8765/' % ZK_URL, autocommit=True)
            self.cursor = self.conn.cursor()
            if not values:
                self.cursor.execute(query_str)
            else:
                self.cursor.executemany(query_str,values)
        except Exception as e:
            print(e)
        finally:
            self.cursor.close()
            self.conn.close()


    def get_table_infos(self): # 得到所有表信息
        try:
            self.conn = phoenixdb.connect('http://%s:8765/' % ZK_URL, autocommit=True)
            self.cursor = self.conn.cursor()
            row_name_list = [x.name for x in self.cursor.description]
            info_list = self.cursor.description
            print(row_name_list)
            print(info_list)
        except Exception as e:
            print(e)
        finally:
            self.cursor.close()
            self.conn.close()



