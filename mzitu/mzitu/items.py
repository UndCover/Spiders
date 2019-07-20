# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy

class InformationItem(scrapy.Item):
    # 标题
    title = scrapy.Field()
    # 链接
    link = scrapy.Field()
    # 时间
    time = scrapy.Field()
    # 缩略图
    thumb = scrapy.Field()
    # 套图数量
    number = scrapy.Field()
    # ID
    pid = scrapy.Field()
    # 文件名
    filename=scrapy.Field()
    # Tag
    tags=scrapy.Field()
    # 是否完成
    done=scrapy.Field()
    # sql 操作 insert 0 update 1 delete 2
    sql=scrapy.Field()
    pass
class PicContentItem(scrapy.Item):
    # 链接
    link = scrapy.Field()
    # 父级ID
    pid = scrapy.Field()
    pass

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