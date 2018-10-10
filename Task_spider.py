# -*- coding: utf-8 -*-
import time
import os
import sys
import subprocess
import sched
from SpiderStatus import SpiderStatus
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
schedule = sched.scheduler(time.time, time.sleep)


def start_spider():
    name = "hotsearch"
    interval = 60
    status = SpiderStatus().getspider(name)
    if status:
        SpiderStatus().setstatus(name,1)
        task = subprocess.Popen("scrapy crawlall")
        task.wait()
        print("Once complete success")
        SpiderStatus().setstatus(name, 2)
        SpiderStatus().setspidertime(name,int(interval/60))
        schedule.enter(interval, 0, start_spider)
    else:
        SpiderStatus().setstatus(name, 0)
        schedule.enter(60, 0, start_spider)

if __name__ =="__main__":
    schedule.enter(0,0,start_spider)
    schedule.run()


# i = 1
# while True:
#     # execute(['scrapy', 'crawlall'])
#     subprocess.Popen("scrapy crawlall")
#     print("第"+str(i)+"次执行爬虫")
#     time.sleep(300)
#     i +=1