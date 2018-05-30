# -*- coding: utf-8 -*-
import scrapy

class MyspiderItem(scrapy.Item):
    society = scrapy.Field()
    album = scrapy.Field()
    idx = scrapy.Field()
    title = scrapy.Field()
    arrange = scrapy.Field()
    vocal = scrapy.Field()
    lyric = scrapy.Field()
    ogmusic = scrapy.Field()
    source = scrapy.Field()
    ttype = scrapy.Field()
    length = scrapy.Field()
