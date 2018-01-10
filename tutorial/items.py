# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    c3_title = scrapy.Field()
    c3_types =scrapy.Field()
    c3_types_num = scrapy.Field()
    c3_district = scrapy.Field()
    c3_price = scrapy.Field()
    c3_trend = scrapy.Field()
    c2_title = scrapy.Field()

    pass
