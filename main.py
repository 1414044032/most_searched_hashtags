#coding:utf-8
import os
import sys
from scrapy.cmdline import execute
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#execute(['scrapy','crawl','jobbole'])
# execute(['scrapy','crawl','baidu'])
# execute(['scrapy','crawl','localnew'])
#execute(['scrapy','crawl','areabaidu'])
execute(['scrapy','crawl','baidunews'])
# execute(['scrapy','crawlall'])