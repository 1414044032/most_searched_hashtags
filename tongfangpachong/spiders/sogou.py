# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from tongfangpachong.items import hot_search_newsItem
import datetime
try:
    from urllib import parse
except:
    import urlparse as parse

class SogouSpider(scrapy.Spider):
    name = 'sogou'
    # allowed_domains = ['http://top.sogou.com']
    start_urls = ['http://top.sogou.com/hot/shishi_1.html',
                  'http://top.sogou.com/hot/shishi_2.html',
                  'http://top.sogou.com/hot/shishi_3.html',
                  'http://top.sogou.com/hot/sevendsnews_1.html',
                  'http://top.sogou.com/hot/sevendsnews_2.html',
                  'http://top.sogou.com/hot/sevendsnews_3.html']
    # custom_settings = {
    #     'ITEM_PIPELINES': {
    #         'tongfangpachong.pipelines.MysqlTwistedPipline': 100,
    #     }
    # }
    def start_requests(self):
        print("检索搜狗热搜")
        create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for i in self.start_urls:
            yield Request(url=i,meta={"create_time":create_time})

    def parse(self, response):
        news_list = response.xpath('//ul[@class="pub-list"]/li')
        origin_type = response.xpath('//div[@class="snb"]/a[@class="cur"]/text()').extract_first("")
        for news in news_list:
            hot_search_news_item = hot_search_newsItem()
            ranking = news.xpath('./span[@class="s1"]//i/text()').extract_first("")
            title = news.xpath('./span[@class="s2"]/p/a/text()').extract_first("")
            message_url = news.xpath('./span[@class="s2"]/p[1]/a/@href').extract_first("")
            news_desc = news.xpath('./span[@class="s2"]/p[2]/text()').extract_first("")
            search_index = news.xpath('./span[@class="s3"]/text()').extract_first("")
            message_trend = news.xpath('./span[@class="s3"]/i/@class').extract_first("")

            hot_search_news_item['title'] = title
            hot_search_news_item['desc'] = news_desc
            hot_search_news_item['news_origin'] = "搜狗热搜"
            hot_search_news_item['create_time'] = response.meta.get("create_time")
            hot_search_news_item['message_url'] = message_url
            hot_search_news_item['ranking'] = ranking
            hot_search_news_item['origin_type'] = origin_type
            hot_search_news_item['search_index'] = search_index
            hot_search_news_item['message_type'] = ""
            hot_search_news_item['message_trend'] = message_trend

            yield hot_search_news_item

