# -*- coding: utf-8 -*-
import time
import os
import sys
import subprocess
import sched

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
schedule = sched.scheduler(time.time, time.sleep)


def start_spider():
    task = subprocess.Popen("scrapy crawlall")
    task.wait()
    print("success")
    schedule.enter(600, 0, start_spider)


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