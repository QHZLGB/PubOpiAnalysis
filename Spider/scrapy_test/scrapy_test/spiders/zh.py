# -*- coding: utf-8 -*-
import scrapy
import re
from urllib import parse
from ..items import ScrapyTestItem
from .util import Util

class ZhSpider(scrapy.Spider):
    name = 'zh'
    # allowed_domains = ['www.zhuhu.com']
    start_urls = ['http://www.zhuhu.com/']

    def __init__(self, keyword='男篮世界杯',crawl_time='2019-07-11 17:04:58', *args, **kwargs):
        super(ZhSpider, self).__init__(*args, **kwargs)
        self.keyword = keyword
        self.crawl_time = crawl_time

    def start_requests(self):
        base_url = 'https://www.sogou.com/sogou?'
        para = {
            'query': self.keyword,
            '_ast': '1562808786',
            '_asf': 'www.sogou.com',
            'w': '01029901',
            'pid': 'sogou-wsse-ff111e4a5406ed40',
            'duppid': '1',
            'cid': '',
            's_from': 'result_up',
            'insite': 'zhihu.com',
            'sut': '5895',
            'sst0': '1562808831026',
            'lkt': '0,0,0',
            'sugsuv': '1562749145928752',
            'sugtime': '1562808831026',
        }
        url = base_url+ parse.urlencode(para)
        yield scrapy.Request(url,callback=self.parse_href)

    # def parse_next(self, response):
    #     next_page = response.css('#sogou_next::attr(href)').extract_first()

    def parse_href(self, response):
        base_url = 'https://www.sogou.com'
        next_base_url = 'https://www.sogou.com/sogou'
        # href = response.css('#sogou_vr_30010208_2::attr(href)').extract_first()
        hrefs = response.css('.vrwrap .vrTitle a::attr(href)').extract()
        for href in hrefs:
            yield scrapy.Request(base_url+href,callback=self.parse_redirect)
        # yield scrapy.Request(base_url+href, callback=self.parse_redirect)
        next_page = response.css('#sogou_next::attr(href)').extract_first()
        # self.logger.info(next_page)
        if next_page is not None:
            yield scrapy.Request(next_base_url+next_page,callback=self.parse_href)

    def parse_redirect(self, response):
        # self.logger.info(response.css('script').re_first(r'"(.*?)"'))
        redirect_url = response.css('script').re_first(r'"(.*?)"')
        # self.logger.info(redirect_url)
        #抽取文章类型的连接，可扩展到问答、专栏、广告
        p = redirect_url.split('/')[-2]
        # self.logger.info(redirect_url)
        if (p=='p'):
            yield scrapy.Request(redirect_url, callback=self.parse_article)
        # yield scrapy.Request(redirect_url, callback=self.parse_article)

    def parse_article(self, response):
        # self.logger.info(response.css('#root > div > main > div > article > header > h1::text').extract_first())
        text = response.css('#root > div > main > div > article > div.Post-RichTextContainer > div').extract_first()
        pattern = re.compile(r'(<.*?>)', re.S)

        #转发数、评论数、点赞数
        rpt = response.css('#Popover7-toggle > button::text').extract_first()
        comm = response.css('#root > div > main > div > article > div:nth-child(5) > div > div > button.'
                            'Button.BottomActions-CommentBtn.Button--plain.Button--withIcon.Button--withLabel::text')\
                            .extract_first()
        up = response.css('#root > div > main > div > article > div:nth-child(5) > div > div > span > button.'
                          'Button.VoteButton.VoteButton--up::text').extract_first()

        title = response.css('#root > div > main > div > article > header > h1::text').extract_first()
        author = response.css('#root > div > main > div > article > header > div.Post-Author >'
                              ' div > meta:nth-child(1)::attr(content)').extract_first()
        keyword = self.keyword
        website = '知乎'
        url = response.url
        content = re.sub(pattern, '', text)
        pub_time = response.css('#root > div > main > div > article > div.ContentItem-time::text').extract_first()
        crawl_time = self.crawl_time
        source = '知乎'
        # self.logger.info(type(rpt))
        # repeat = rpt
        # comment = comm
        # like = up
        repeat = Util.filter_num(rpt)
        comment = Util.filter_num(comm)
        like = Util.filter_num(up)
        item = ScrapyTestItem()
        item['title'] = title
        item['author'] = author
        item['keyword'] = keyword
        item['website'] = website
        item['url'] = url
        item['content'] = content
        item['pub_time'] = Util.filter_date(pub_time)
        item['crawl_time'] = crawl_time
        item['source'] = source
        item['repeat'] = repeat
        item['comment'] = comment
        item['like'] = like
        yield item
        # item['pub_time'] = pub_time
        # item['pub_time'] = pub_time


