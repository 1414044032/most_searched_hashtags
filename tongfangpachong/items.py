# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose,TakeFirst,Join


class baiduToplistItemloader(ItemLoader):
    default_output_processor = TakeFirst()


# 区域风向标
class areabaiduItem(scrapy.Item):
    area = scrapy.Field()
    keyword = scrapy.Field()
    searches = scrapy.Field()
    changeRate = scrapy.Field()
    isNew = scrapy.Field()
    trend = scrapy.Field()
    percentage = scrapy.Field()

    def get_insert_sql(self):

        insert_sql = """
                        insert into areabaidu(area, keyword, searches, changeRate, isNew, trend, percentage)
                        VALUES (%s,%s,%s,%s,%s,%s,%s)
                         """
        parms=(
        self["area"],self["keyword"], self["searches"], self["changeRate"], self["isNew"], self["trend"],
        self["percentage"])
        return insert_sql,parms


# 本地新闻
class localnewItem(scrapy.Item):
    url =scrapy.Field()
    title =scrapy.Field()

    def get_insert_sql(self):

        insert_sql = """
                        insert into localnew(url,title)
                        VALUES (%s,%s)
                         """
        parms=(self["url"],self["title"])
        return insert_sql,parms


# 测试环境表
class hot_search_newsItem(scrapy.Item):
    title = scrapy.Field()
    desc = scrapy.Field()
    search_index = scrapy.Field()
    create_time = scrapy.Field()
    news_origin = scrapy.Field()
    origin_type = scrapy.Field()
    message_type = scrapy.Field()
    message_trend = scrapy.Field()
    message_url = scrapy.Field()
    ranking = scrapy.Field()
    def get_insert_sql(self):
        insert_sql = """
                        insert into t_public_opinion_hot_search_news(title,news_desc, search_index,create_time,news_origin,origin_type, message_type, message_url,message_trend, ranking)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                         """
        parms=(self["title"], self["desc"], self["search_index"], self["create_time"], self["news_origin"],
               self["origin_type"],self["message_type"], self["message_url"], self["message_trend"], self["ranking"])
        return insert_sql,parms

class front_news(scrapy.Item):
    news_source = scrapy.Field()
    news_module = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    happend_time = scrapy.Field()
    create_time = scrapy.Field()
    def get_insert_sql(self):
        insert_sql = """
                        insert into t_public_opinion_front_news(news_source,news_module,title,url,happend_time,create_time)
                        VALUES (%s,%s,%s,%s,%s,%s)
                         """
        parms=(self["news_source"],self["news_module"],self["title"],self["url"],self["happend_time"],self["create_time"])
        return insert_sql,parms