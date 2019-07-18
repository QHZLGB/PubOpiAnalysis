from scrapy.crawler import CrawlerProcess
from scrapy_test.spiders import zh, xw, wb, wx
from scrapy.utils.project import get_project_settings
from scrapy_test.mysqlDB.scheme import get_keywords
from scrapy_test.spiders.util import Util
from multiprocessing import Process
import schedule
import time
import logging


#单个进程运行所有spider，包括所有的主题
# def launch():
#     # setting = get_project_settings()
#     # logging.info(setting)
#     # 同一个进程中无法重启twisted框架中的reactor堆,采用多个进程
#     sql = 'select keyword from scheme'
#     process = CrawlerProcess(get_project_settings())
#     for keyword in get_keywords(sql):
#         # keyword = "中美贸易战"
#         # process.crawl(zh, keyword="河北地质大学",crawl_time = "2019-07-11 17:04:58")
#         process.crawl(zh.ZhSpider, keyword=keyword[0], crawl_time=Util.now())
#         process.crawl(xw.XwSpider, keyword=keyword[0], crawl_time=Util.now())
#         process.crawl(wb.WbSpider, keyword=keyword[0], crawl_time=Util.now())
#         process.crawl(wx.WxSpider, keyword=keyword[0], crawl_time=Util.now())
#     process.start()

# 同一个进程中无法重启twisted框架中的reactor堆,采用多个进程


def launch(keyword, crawl_time):
    process = CrawlerProcess(get_project_settings())
    process.crawl(zh.ZhSpider, keyword=keyword, crawl_time=crawl_time)
    process.crawl(xw.XwSpider, keyword=keyword, crawl_time=crawl_time)
    process.crawl(wb.WbSpider, keyword=keyword, crawl_time=crawl_time)
    process.crawl(wx.WxSpider, keyword=keyword, crawl_time=crawl_time)
    process.start()


def job():
    sql = 'select keyword from scheme'
    pool = []
    for keyword in get_keywords(sql):
        pool.append(Process(target=launch, args=(keyword[0], Util.now())))
    for p in pool:
        p.start()
    for p in pool:
        p.join()


if __name__ == '__main__':
    schedule.every().minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
