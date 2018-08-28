# -*- coding: utf-8 -*-
import time
import os
import sys
from scrapy.cmdline import execute
import subprocess

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
i = 1
while True:
    # execute(['scrapy', 'crawlall'])
    subprocess.Popen("scrapy crawlall")
    print("第"+str(i)+"次执行爬虫")
    time.sleep(120)
    i +=1