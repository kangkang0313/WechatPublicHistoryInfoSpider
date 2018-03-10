# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WechathistoryspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class HistoryItem(scrapy.Item):
    title = scrapy.Field()
    date = scrapy.Field()
    public_name = scrapy.Field()
    content_url = scrapy.Field()
    like_num = scrapy.Field()
    read_num = scrapy.Field()
