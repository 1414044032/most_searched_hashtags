# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrapy import Request
try:
    from urllib import parse
except:
    import urlparse as parse
from tongfangpachong.items import hot_search_newsItem
import re

class baiduSpider(scrapy.Spider):
    name = 'baidu'
    #allowed_domains = ['http://top.baidu.com']
    start_urls = ['http://top.baidu.com/category?c=513&fr=topbuzz_b1']
    custom_settings = {
        'ITEM_PIPELINES': {
            'tongfangpachong.pipelines.MysqlTwistedPipline':100,
        }
    }
    def parse(self, response):
        top_list = response.xpath('//div[@class="hblock"]/ul/li/a')
        for i in range(1,len(top_list)):
            top_name = top_list[i].xpath('./text()').extract_first("")
            top_url = re.sub('\s','',top_list[i].xpath('./@href').extract_first(""))[1:]
            print(parse.urljoin(response.url,top_url))
            yield Request(url=parse.urljoin(response.url,top_url),meta={"top_name":top_name},callback=self.parse_toplist,dont_filter=True)

    def parse_toplist(self, response):
        print("检索百度热搜")
        top_keywords_list = response.xpath('//table[@class="list-table"]/tr')
        for top_keyword in top_keywords_list:
            hot_search_news_item = hot_search_newsItem()
            if top_keyword.xpath('./td[@class="keyword"]/a[1]/text()').extract_first(""):
                # 排名
                top_keyword_rank = top_keyword.xpath('./td[@class="first"]/span/text()').extract_first("")
                # 关键词
                top_keyword_title = top_keyword.xpath('./td[@class="keyword"]/a[1]/text()').extract_first("")
                # 相关网址
                top_keyword_url = top_keyword.xpath('./td[@class="keyword"]/a[1]/@href').extract_first("")
                # 新闻
                info = top_keyword.xpath('./td[@class="tc"]/a[1]/@href').extract_first("")
                # 搜索指数
                top_keyword_pop = top_keyword.xpath('./td[@class="last"]/span/text()').extract_first("")
                # 词类型
                top_keyword_type = top_keyword.xpath('./td[@class="keyword"]/span/@class').extract_first("")
                #  趋势
                top_keyword_trend = top_keyword.xpath('./td[@class="last"]/span/@class').extract_first("")
                hot_search_news_item['origin_type'] = response.meta.get("top_name","")
                hot_search_news_item['title'] = top_keyword_title
                hot_search_news_item['desc'] = ""
                hot_search_news_item['news_origin'] = "百度热搜"
                hot_search_news_item['create_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                hot_search_news_item['message_url'] = top_keyword_url
                hot_search_news_item['ranking'] = top_keyword_rank
                hot_search_news_item['search_index'] = top_keyword_pop
                hot_search_news_item['message_type'] = top_keyword_type
                hot_search_news_item['message_trend'] = top_keyword_trend
                yield hot_search_news_item


