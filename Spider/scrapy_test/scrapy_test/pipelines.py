# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import re
from .mysqlDB.setting import *
import pymysql
import logging
from scrapy.exceptions import DropItem


class ScrapyTestPipeline(object):
    def process_item(self, item, spider):
        # file = open('./items.jl', 'wb')
        # line = json.dumps(dict(item)) + "\n"
        # file.write(line.encode())
        if item['content'] is not None:
            content = item['content']
            pattern = re.compile(r'[\s]+', re.S)
            result = re.sub(pattern, '', content)
            item['content'] = result
            return item
        else:
            raise DropItem("Missing price in %s" % item)



class MysqlPipeline(object):

    def __init__(self):
        self.MYSQL_HOST = MYSQL_HOST
        self.MYSQL_USER = MYSQL_USER
        self.MYSQL_PORT = MYSQL_PORT
        self.MYSQL_PWD = MYSQL_PWD
        self.MYSQL_DB = MYSQL_DB
        self.conn = None
        self.cursor = None

    def open_spider(self, spider):
        conn = pymysql.connect(host=self.MYSQL_HOST, port=self.MYSQL_PORT, user=self.MYSQL_USER,
                               passwd=self.MYSQL_PWD, db=self.MYSQL_DB, charset='utf8')
        if conn:
            print('MySQL database opened successfully!')
            self.conn = conn
        else:
            print('MySQL database opened failed!')

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        if self.conn:
            self.cursor = self.conn.cursor()

            values = "'%s', '%s', '%s', '%s', '%s', '%s', str_to_date('%s','%%Y-%%m-%%d %%H:%%i:%%S'), " \
                     "str_to_date('%s','%%Y-%%m-%%d %%H:%%i:%%S')," \
                     "'%s',%d,%d,%d" % \
                     (item['title'], item['author'], item['keyword'], item['website'],
                      item['url'], item['content'], item['pub_time'], item['crawl_time'],
                      item['source'], item['repeat'], item['comment'], item['like']
                      )

            sql = "insert into new_article (title, author, keyword, website, url, content, pub_time, crawl_time," \
                  "source, repeat1, comment, like1) VALUES " \
                  "({values})".format(values=values)
            # values = (item['title'], item['author'], item['keyword'], item['website'],
            #           item['url'], item['content'], item['pub_time'], item['crawl_time'],
            #           item['source'], item['repeat'], item['comment'], item['like'],
            #           )
            # logging.info(sql)
            # logging.info(type(item['like']))
            self.cursor.execute(sql)
            self.conn.commit()
            # try:
            #     self.cursor.execute(sql, values)
            #     self.conn.commit()
            #     print("mysql insert into successful")
            # except:
            #     print("mysql insert into fail")
            #     self.conn.rollback()

        return item
