# -*- coding: utf-8 -*-
import scrapy
from tongfangpachong.items import hot_search_newsItem
import datetime

class WeoboSpider(scrapy.Spider):
    print("检索微博热搜")
    name = 'weibo'
    # allowed_domains = ['http://s.weibo.com']
    start_urls = ['http://s.weibo.com/top/summary?cate=homepage']
    # custom_settings = {
    #     'ITEM_PIPELINES': {
    #         'tongfangpachong.pipelines.MysqlTwistedPipline': 100,
    #     }
    # }
    def parse(self, response):

        top_list = response.xpath('//tr[@action-type="hover"]')
        for top in top_list:
            hot_search_news_item = hot_search_newsItem()
            top_name = "新浪热搜"
            top_keyword_rank = top.xpath('.//span[@class="search_icon_rankntop"]/em/text() | .//span[@class="search_icon_rankn"]/em/text()').extract_first("")
            top_keyword = top.xpath('.//p[@class="star_name"]/a/text()').extract_first("")
            top_keyword_url = top.xpath('.//p[@class="star_name"]/a/@href').extract_first("")
            top_keyword_type = top.xpath('.//p[@class="star_name"]/i/text()').extract_first("")
            if top_keyword_type == "荐":
                top_keyword_url = top.xpath('.//p[@class="star_name"]/a/@href_to').extract_first("")
            top_keyword_pop = top.xpath('.//p[@class="star_num"]/span/text()').extract_first("")
            hot_search_news_item['title'] = top_keyword
            hot_search_news_item['desc'] = ""
            hot_search_news_item['search_index'] = top_keyword_pop
            hot_search_news_item['create_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            hot_search_news_item['news_origin'] = top_name
            hot_search_news_item['origin_type'] = "热搜榜"
            hot_search_news_item['message_type'] = top_keyword_type
            hot_search_news_item['message_trend'] = ""
            hot_search_news_item['message_url'] = "http://s.weibo.com"+top_keyword_url
            hot_search_news_item['ranking'] = top_keyword_rank


            yield hot_search_news_item




