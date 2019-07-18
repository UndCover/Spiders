# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy

class MzituItem(scrapy.Item):
    # 标题
    title = scrapy.Field()
    # 链接
    link = scrapy.Field()
    # 时间
    time = scrapy.Field()
    # 缩略图
    thumb = scrapy.Field()
    # # 浏览数量
    # view = scrapy.Field()

# PageInfoModel
class ImageItem(scrapy.Item):
    folder = scrapy.Field()
    src = scrapy.Field()
    refer = scrapy.Field()
    
    

class TestItem(scrapy.Item):
    imgUrl = scrapy.Field()
    pass