from scrapy import signals
from scrapy.exceptions import NotConfigured


class SpiderOpenCloseLogging(object):

    def __init__(self):
        self.items_scraped = 0
        self.items_dropped = 0

    @classmethod
    def from_crawler(cls, crawler):
        # 读取settings配置信息，检查是否启动扩展，没有启用则抛出异常，扩展被禁用
        if not crawler.settings.getbool('MY_EXTENSION'):
            raise NotConfigured

        # 实例化扩展对象
        ext = cls()

        # 注册信号处理函数
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)

        return ext

    # 自定义的3个信号处理函数
    def spider_opened(self, spider):
        spider.log(">>> opened spider %s" % spider.name)

    def spider_closed(self, spider, reason):
        spider.log(">>> closed spider %s" % spider.name)
        spider.log(">>>scraped %d items" % self.items_scraped)
        spider.log(">>>dropped %d items" % self.items_dropped)
        # 获取状态收集器信息
        print(spider.crawler.stats.get_stats())
