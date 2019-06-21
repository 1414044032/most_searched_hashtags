# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi

class TongfangpachongPipeline(object):
    def process_item(self, item, spider):
        return item

# 清表
class MysqlPipline(object):
    def __init__(self, host, user, password, dbname, port):
        self.conn=MySQLdb.connect(host, user, password, dbname, port=port, charset="utf8",use_unicode=True)
        self.cursor=self.conn.cursor()
        number = self.cursor.execute("select id from t_public_opinion_hot_search_news")
        print(number)
        if number >2000:
            print("数据库数据超过了2000条，清空数据")
            self.cursor.execute("truncate table t_public_opinion_hot_search_news")
            self.cursor.execute("truncate table t_public_opinion_front_news")
        #self.cursor.execute("truncate table areabaidu")
    @classmethod
    def from_settings(cls, setting):
        host=setting["MYSQL_HOST"]
        user=setting["MYSQL_USER"]
        password=setting["MYSQL_PASSWORD"]
        dbname=setting["MYSQL_DBNAME"]
        port=setting["MYSQL_PORT"]
        return cls(host, user, password, dbname, port)
    def process_item(self, item, spider):
        return item

# 插入
class MysqlTwistedPipline(object):
    def __init__(self,dbpool):
        self.dbpool=dbpool
    @classmethod
    def from_settings(cls,setting):
        dbparms=dict(
                host=setting["MYSQL_HOST"],
                db=setting["MYSQL_DBNAME"],
                user=setting["MYSQL_USER"],
                passwd=setting["MYSQL_PASSWORD"],
                charset='utf8',
                port=setting["MYSQL_PORT"],
                cursorclass=MySQLdb.cursors.DictCursor,
                use_unicode=True,
        )
        dbpool=adbapi.ConnectionPool("MySQLdb",**dbparms)
        return cls(dbpool)
    #mysql异步插入执行
    def process_item(self, item, spider):
        query=self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error,item,spider)

    def handle_error(self,failure,item,spider):
        #处理异步插入的异常
        print (failure)
    def do_insert(self,cursor,item):
        insert_sql,parms=item.get_insert_sql()
        cursor.execute(insert_sql, parms)