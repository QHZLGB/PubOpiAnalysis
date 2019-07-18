# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from .util import Util, transformTime
from ..items import ScrapyTestItem


class WxSpider(scrapy.Spider):
    name = 'wx'
    # allowed_domains = ['www.sougou.com']
    start_urls = ['http://www.sougou.com/']

    def __init__(self, keyword='河北 财政 河北财政厅',crawl_time='2019-07-11 17:04:58', *args, **kwargs):
        super(WxSpider, self).__init__(*args, **kwargs)
        self.keyword = keyword
        self.crawl_time = crawl_time

    def start_requests(self):
        base_url = 'https://weixin.sogou.com/weixin?'
        para = {
            'p': '01030402',
            'query': self.keyword,
            'type': '2',
            'ie': 'utf8',
        }
        url = base_url + parse.urlencode(para)
        yield scrapy.Request(url, callback=self.parse_href)

    def parse_href(self, response):
        # self.logger.info(response.css('.news-list li '))
        hrefs = response.css('.news-list li ')
        next_base_url = 'https://weixin.sogou.com/weixin'
        for href in hrefs:
            # self.logger.info(href.css('.txt-box h3 a').extract_first())
            url = href.css('.txt-box h3 a::attr(data-share)').extract_first()
            title = Util.filter_label(href.css('.txt-box h3 a').extract_first())
            author = href.css('.txt-box .s-p a ::text').extract_first()
            time = transformTime.deal_time(href.css('.txt-box .s-p span script').re_first(r'[\d]+'))
            # self.logger.info(time)
            meta = {
                'url': url,
                'title': title,
                'author': author,
                'time': time,
            }
            yield scrapy.Request(url, meta=meta, callback=self.parse_content,)
        next_page = response.css('#sogou_next::attr(href)').extract_first()
        yield scrapy.Request(next_base_url+next_page, callback=self.parse_href)

    def parse_content(self, response):
        content = Util.filter_label(response.css('.rich_media_content').extract_first())

        item = ScrapyTestItem()
        item['title'] = response.meta['title']
        item['author'] = response.meta['author']
        item['keyword'] = self.keyword
        item['website'] = '微信'
        item['url'] = response.meta['url']
        item['content'] = content
        item['pub_time'] = response.meta['time']
        item['crawl_time'] = self.crawl_time
        item['source'] = response.meta['author']
        item['repeat'] = 0
        item['comment'] = 0
        item['like'] = 0
        yield item
        # self.logger.info(response.meta['time'])

    def parse(self, response):
        pass
