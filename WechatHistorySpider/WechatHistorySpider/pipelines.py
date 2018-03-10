# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymysql import cursors
from twisted.enterprise import adbapi


class WechathistoryspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MyYiBuSQL(object):
    @classmethod
    def from_settings(cls, settings):
        db_params = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            port=settings['MYSQL_PORT'],
            user=settings['MYSQL_USER'],
            charset=settings['MYSQL_CHARSET'],
            password=settings['MYSQL_PASSWORD'],
            use_unicode=True,
            cursorclass=cursors.DictCursor
        )
        db_pool = adbapi.ConnectionPool('pymysql', **db_params)
        return cls(db_pool)

    def __init__(self, db_pool):
        self.db_pool = db_pool

    def process_item(self, item, spider):
        querry = self.db_pool.runInteraction(self.do_insert, item)
        querry.addErrback(self.handle_error, item, spider)
        return item

    def handle_error(self, failure, item, spider):
        return failure

    def do_insert(self, cursor, item):
        my_sql = 'insert into history(title,date,public_name,content_url,like_num,read_num)VALUES (%s,%s,%s,%s,%s,%s)'
        cursor.execute(my_sql, (item['title'], item['date'], item['public_name'], item['content_url'], item['like_num'], item['read_num']))

