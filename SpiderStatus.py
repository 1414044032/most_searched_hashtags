# -*- coding: utf-8 -*-
import MySQLdb
import datetime
import os
import re
import configparser
import traceback

class SpiderStatus:

    def __init__(self):
        # [host, dbname, port, user, password]
        # 配置list
        set_list = getsetting()
        self.conn = MySQLdb.connect(host=set_list[0], user=set_list[3], passwd=set_list[4], db=set_list[1],
                                    port=set_list[2], charset="utf8")
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
    #     MYSQL_HOST="192.168.10.18"
    # MYSQL_DBNAME="meltmedia"
    # MYSQL_USER="root"
    # MYSQL_port=3306
    # MYSQL_PASSWORD="root"
    try:
        host = re.findall(r"MYSQL_HOST=\"(.*)\"",setting)[0]
        dbname = re.findall(r"MYSQL_DBNAME=\"(.*)\"",setting)[0]
        port = int(re.findall(r"MYSQL_PORT=(.*)",setting)[0])
        user = re.findall(r"MYSQL_USER=\"(.*)\"",setting)[0]
        password = re.findall(r"MYSQL_PASSWORD=\"(.*)\"",setting)[0]
        return [host, dbname, port, user, password]
    except Exception as e:
        traceback.print_exception()
        print(e)
        print("检查配置文件mysql配置")


if __name__ == "__main__":
    pass