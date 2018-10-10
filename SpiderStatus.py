# -*- coding: utf-8 -*-
import MySQLdb
import datetime
import os
import re
import configparser


class SpiderStatus:

    def __init__(self):
        self.conn = MySQLdb.connect(host=getsetting(), user="root", passwd="root", db="meltmedia", charset="utf8")
        self.cursor = self.conn.cursor()

    def getspider(self,name):
        sql = "select * from t_public_spider_list where name =%s and status = 1"
        result = self.cursor.execute(sql,[name,])
        self.closeconn()
        return result

    def setspidertime(self, name,interval):
        last_spider_time =  datetime.datetime.now()
        after_spider_time = (last_spider_time + datetime.timedelta(minutes=interval)).strftime("%Y-%m-%d %H:%M:%S")
        last_spider_time = last_spider_time.strftime("%Y-%m-%d %H:%M:%S")
        sql = "update t_public_spider_list set last_spider_time =%s,after_spider_time=%s,spider_count=spider_count+1 where name =%s "
        self.cursor.execute(sql,[last_spider_time,after_spider_time,name])
        self.conn.commit()
        self.closeconn()

    def setstatus(self, name, execute_status):
        sql = "update t_public_spider_list set execute_status =%s where name =%s "
        self.cursor.execute(sql,[execute_status,name])
        self.conn.commit()
        self.closeconn()

    def closeconn(self):
        self.cursor.close()
        self.conn.close()

def getsetting():
    dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(dir ,"scrapy.cfg")
    config = configparser.ConfigParser()
    config.read(filename)
    setfile = "\\".join(config.get("settings","default").split("."))+".py"
    setfile = os.path.join(dir,setfile)
    with open(setfile,"r") as f:
        setting = f.read()
    result = re.findall(r"MYSQL_HOST=\"(.*)\"",setting)
    if len(result)== 1:
        return result[0]
    else:
        return "192.168.10.18"

if __name__ == "__main__":
    pass