import scrapy
import datetime
import time
import json
try:
    from urllib import parse
except:
    import urlparse as parse
from tongfangpachong.items import front_news
import re

class baiduSpider(scrapy.Spider):
    name = 'baidunews'
    unittime = str(int(time.time()))
    start_urls = ['http://news.baidu.com/widget?id=LocalNews&loc=4504&ajax=json&t=%s'%unittime]
    custom_settings = {
        'ITEM_PIPELINES': {
            'tongfangpachong.pipelines.MysqlTwistedPipline':100,
        }
    }


    def parse(self, response):
        news = json.loads(response.text).get("data").get("LocalNews").get("data").get("rows").get("first") +json.loads(response.text).get("data").get("LocalNews").get("data").get("rows").get("second")
        for new in news:
            newsitem = front_news()
            newsitem["title"] = new.get("title")
            newsitem["news_source"] = "百度新闻"
            newsitem["news_module"] = "许昌新闻"
            newsitem["url"] =  new.get("url")
            newsitem["happend_time"] = datetime.datetime.now().strftime("%Y-%m-%d ")+ new.get("time") + ":00"
            newsitem["create_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            yield newsitem