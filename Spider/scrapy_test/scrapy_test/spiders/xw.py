# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from .util import Util, transformTime
from ..items import ScrapyTestItem

class XwSpider(scrapy.Spider):
    name = 'xw'
    # allowed_domains = ['www.sougou.com']
    start_urls = ['http://www.sougou.com/']

    def __init__(self, keyword='中国男篮',crawl_time='2019-07-11 17:04:58', *args, **kwargs):
        super(XwSpider, self).__init__(*args, **kwargs)
        self.keyword = keyword
        self.crawl_time = crawl_time

    def start_requests(self):
        base_url = 'https://news.sogou.com/news?'
        para = {
            'query': self.keyword,
            '_ast': '1562899968',
            '_asf': 'news.sogou.com',
            'time':'0',
            'w': '03009900',
            'sort':'0',
            'mode': '1',
            'manual':'',
            'dp': '1',

        }
        url = base_url + parse.urlencode(para)
        yield scrapy.Request(url, callback=self.parse_content)

    def parse_content(self, response):
        next_base_url = 'https://news.sogou.com/news?'
        details = response.css('.news151102')
        # self.logger.info(hrefs)
        for detail in details:
            title = detail.css('h3 a').extract_first()#Util.filter_label(title)
            author_time = detail.css('.news-info .news-from ::text').extract_first()
            author, time = Util.filter_author_time(author_time)#transformTime.deal_time(time)

            title = Util.filter_label(title)
            #author
            keyword = self.keyword
            website = '网站'
            url = detail.css('h3 a ::attr(href)').extract_first()
            content = detail.css('.news-txt span').extract_first()
            pub_time = transformTime.deal_time(time)
            crawl_time = self.crawl_time
            source = author
            repeat = 0
            comment = 0
            like = 0
            # self.logger.info(Util.filter_label(content))
            # yield scrapy.Request(href, callback=self.parse)
            item = ScrapyTestItem()
            item['title'] = title
            item['author'] = author
            item['keyword'] = keyword
            item['website'] = website
            item['url'] = url
            item['content'] = Util.filter_label(content)
            item['pub_time'] = pub_time
            item['crawl_time'] = crawl_time
            item['source'] = source
            item['repeat'] = repeat
            item['comment'] = comment
            item['like'] = like
            yield item

        next_page = response.css('#sogou_next::attr(href)').extract_first()
        if next_page is not None:
            yield scrapy.Request(next_base_url+next_page,callback=self.parse_content)

    def parse(self, response):
        pass
