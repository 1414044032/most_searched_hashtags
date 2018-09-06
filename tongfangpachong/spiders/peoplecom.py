# -*- coding: utf-8 -*-
import scrapy
import datetime
try:
    from urllib import parse
except:
    import urlparse as parse
from tongfangpachong.items import front_news

class baiduSpider(scrapy.Spider):
    name = 'people'
    start_urls = ['http://henan.people.com.cn/GB/378395/index.html',
                  'http://henan.people.com.cn/GB/363904/index.html',
                  'http://henan.people.com.cn/GB/357262/index.html',
                  'http://henan.people.com.cn/GB/356900/index.html']
    custom_settings = {
        'ITEM_PIPELINES': {
            'tongfangpachong.pipelines.MysqlTwistedPipline':100,
        }
    }
    def parse(self, response):
        news_list = response.xpath('//div[@class="fl w655"]')
        module = news_list.xpath('./div[@class="lujing"]/a[last()]/text()').extract_first("")
        news = news_list.xpath('.//div[contains(@class, "ej_list_box clear")]//li')
        for new in news:
            newsitem =front_news()
            title = new.xpath('./a/text()').extract_first("")
            url = "henan.people.com.cn"+ new.xpath('./a/@href').extract_first("")
            happend_time = new.xpath('./em/text()').extract_first("")
            create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            newsitem["news_source"] = "人民网"
            newsitem["news_module"] = module
            newsitem["title"] = title
            newsitem["url"] = url
            newsitem["happend_time"] = happend_time
            newsitem["create_time"] = create_time
            yield newsitem