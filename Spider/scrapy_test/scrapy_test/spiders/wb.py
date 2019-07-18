# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
import json
from ..items import ScrapyTestItem
from .util import Util, transformTime


class WbSpider(scrapy.Spider):
    name = 'wb'
    # allowed_domains = ['www.weibo.com']
    start_urls = ['http://www.weibo.com/']

    def __init__(self, keyword='河北 财政 河北财政厅',crawl_time='2019-07-11 17:04:58', *args, **kwargs):
        super(WbSpider, self).__init__(*args, **kwargs)
        self.keyword = keyword
        self.crawl_time = crawl_time
        self.pageNum = 2


    def start_requests(self):
        base_url = 'https://m.weibo.cn/api/container/getIndex?'
        para = {
            'containerid': '100103type=61&q='+self.keyword+'&t=0',
            'page_type': 'searchall',
        }
        url = base_url + parse.urlencode(para)
        yield scrapy.Request(url,callback=self.parse_json)

    def parse(self, response):
        self.logger.info(response.text)

    def parse_json(self, response):
        detail_base_url = 'https://m.weibo.cn/'
        # self.logger.info(response.text)
        result = json.loads(response.text)
        ok = result.get('ok')
        # self.logger.info(type(ok))
        if ok:
            res = result.get('data').get('cards')[0].get('card_group')
            for re in res:
                mblog = re.get('mblog')
                is_long = mblog.get('isLongText')
                # self.logger.info(type(is_long))
                if is_long:
                    content = mblog.get('longText').get('longTextContent')
                else:
                    content = mblog.get('text')
                mblog_id = mblog.get('id')
                url = detail_base_url+'detail/'+mblog_id
                time = transformTime.deal_time(mblog.get('created_at'))
                user = mblog.get('user')
                author = user.get('screen_name')
                like = mblog.get('attitudes_count')
                comment = mblog.get('comments_count')
                repeat = mblog.get('reposts_count')

                item = ScrapyTestItem()
                item['title'] = author
                item['author'] = author
                item['keyword'] = self.keyword
                item['website'] = '微博'
                item['url'] = url
                item['content'] = Util.filter_label(content)
                item['pub_time'] = time
                item['crawl_time'] = self.crawl_time
                item['source'] = '微博'
                item['repeat'] = repeat
                item['comment'] = comment
                item['like'] = like
                yield item
            next_base_url = 'https://m.weibo.cn/api/container/getIndex?'
            para = {
                'containerid': '100103type=61&q='+self.keyword+'&t=0',
                'page_type': 'searchall',
                'page': self.pageNum,
            }
            url = next_base_url + parse.urlencode(para)
            yield scrapy.Request(url,callback=self.parse_json)
            self.pageNum += 1

