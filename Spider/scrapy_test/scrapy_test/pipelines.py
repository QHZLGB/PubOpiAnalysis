# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class ScrapyTestPipeline(object):
    def process_item(self, item, spider):
        # file = open('./items.jl', 'wb')
        # line = json.dumps(dict(item)) + "\n"
        # file.write(line.encode())
        return item
