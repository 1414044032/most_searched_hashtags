# -*- coding: utf-8 -*-
from urllib.parse import quote
import requests
import json
import pymongo
import MySQLdb
import time
import datetime
import re


class weibosearch():
    # 热门
    def __init__(self):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient["wangliuqi"]
        self.mycol = self.mydb["hot"]
        self.mycol1 = self.mydb["comment"]
        self.mycomments = self.mydb["allcomments"]
        self.conn = MySQLdb.connect(host="192.168.10.18", user="root", passwd="root", db="meltmedia", charset="utf8")
        self.cursor = self.conn.cursor()

    def keyword_search(self, key_word):
        # 清空数据库
        self.mycol.delete_many({})
        print("开始爬取搜索关键字")
        for i in range(1,60):
            base_url = "https://m.weibo.cn/api/container/getIndex?containerid=100103type%253D60%2526q%253D%25E8%25AE%25B8%25E6%2598%258C&title=%25E7%2583%25AD%25E9%2597%25A8-%25E8%25AE%25B8%25E6%2598%258C&cardid=weibo_page&extparam=title%253D%E7%83%AD%E9%97%A8%2526mid%253D%2526q%253D"+quote(key_word)+"&luicode=10000011&lfid=100103type%3D1%26q%3D"+quote(key_word)+"&page="+str(i)
            response = requests.get(base_url)
            # 获取到结果页面
            result = json.loads(response.text, encoding="GBK")
            # 解析页面
            if result.get("ok") == 1:
                print("存入搜索结果到数据库")
                news_list = result.get("data").get("cards")[0].get("card_group")
                self.mycol.insert_many(news_list)
            else:
                break
        print("热门关键字检索完毕")



    def mongo2mysql(self):
        hot_data = self.mycol.find({},{'_id':0,'mblog.id':1,'actionlog.fid':1, 'mblog.text':1,'mblog.created_at':1,'mblog.user.screen_name':1,'mblog.reposts_count':1,'mblog.comments_count':1,'mblog.attitudes_count':1})
        num = 0
        for data in hot_data:
            base_message_url ="https://m.weibo.cn/status/%s"
            message_url = base_message_url%str(data.get("mblog").get("id"))
            title=data.get("actionlog").get("fid")[-2:]
            if data.get("mblog").get("longText"):
                content = data.get("mblog").get("longText").get("longTextContent")
            else:
                content = data.get("mblog").get("text")
            happend_time = data.get("mblog").get("created_at")
            #happend_time_new = data.get("mblog").get("longText").get("url_objects")[0].get("object").get("timestamp")
            if len(happend_time) <= 6:
                # 获取时间
                if "小时" in happend_time:
                    values = [i for i in re.findall("\d*",happend_time) if i][0]
                    happend_time = (datetime.datetime.now()- datetime.timedelta(hours=int(values))).strftime("%Y-%m-%d %H:%M:%S")
                else:
                    happend_time = time.strftime('%Y',time.localtime(time.time())) +"-"+ happend_time
            origin = data.get("mblog").get("user").get("screen_name")
            create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            transmit_count = data.get("mblog").get("reposts_count")
            comment_count = data.get("mblog").get("comments_count")
            like_count = data.get("mblog").get("attitudes_count")
            sql = """
            insert into t_public_opinion_realtime_news (title, content, create_time, happend_time, origin,
             message_url, transmit_count, comment_count, collect_count, like_count)values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            test = bytes(content, encoding="utf-8")
            parms = (title,test,create_time,happend_time, origin, message_url, transmit_count,comment_count,0,like_count )
            n = self.cursor.execute(sql,parms)
            num= num+n
            print("第"+str(num)+"条热门已转到mysql")
            self.conn.commit()
        self.conn.close()
        print("数据插入完成")


    # find all comments
    def get_all_comments(self):
        allresult = self.mycol.find({}, {'_id':0,'mblog.id': 1})
        self.mycomments.delete_many({})
        print("开始爬取评论")
        tag = True
        status_url = "https://m.weibo.cn/comments/hotflow?id=%s&mid=%s&max_id_type=0"
        status_after_url = "https://m.weibo.cn/comments/hotflow?id=%s&mid=%s&max_id=%s&max_id_type=%s"
        max_id = 1
        max_id_type = 0
        for data in allresult:
            id = str(data.get("mblog").get("id"))
            print(id)
            # if sign
            index = 0
            # get all comment     loop  by  index
            while max_id!=0:
                # first loop
                if index ==0:
                    url = status_url%(id,id)
                    response = requests.get(url)
                    result = json.loads(response.text, encoding="utf-8")
                    # ensure only loop one
                    index =1
                # sencend - last
                else:
                    url = status_after_url%(id,id,str(max_id),str(max_id_type))
                    response = requests.get(url)
                    result = json.loads(response.text, encoding="utf-8")
                # save result
                if result.get("ok") == 1:
                    max_id = result.get("data").get("max_id")
                    max_id_type = result.get("data").get("max_id_type")
                    print(max_id)
                    comment_data = result.get("data").get("data")
                    for comment in comment_data:
                        comment["airticle"] = id
                    self.mycomments.insert_many(comment_data)
                else:
                    print(result)
            print("评论爬取完成")

if __name__ == "__main__":
    # weibosearch().keyword_search("许昌")
    weibosearch().mongo2mysql()
    # weibosearch().get_all_comments()