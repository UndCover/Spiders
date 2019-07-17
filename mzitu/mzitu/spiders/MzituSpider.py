# import scrapy
# from mzitu.items import MzituItem

# class MzituSpider(scrapy.Spider):
#     name = 'MzituSpider'
#     allowed_domains = ['www.mzitu.com']
#     start_urls = ['https://www.mzitu.com/page/2/']
#     def parse(self, response):
#         pass


# -*- coding: utf-8 -*-
import scrapy
import time
# import logging
from mzitu.items import MzituItem


class MzituSpider(scrapy.Spider):
    # logging.basicConfig(level=logging.DEBUG)
    name = 'mzitu'
    allowed_domains = ['mzitu.com']
    start_urls = ['https://www.mzitu.com/']

    def parse(self, response):
        print("================================================")
        for _li in response.xpath("//*[@id=\"pins\"]/li"):
            item = MzituItem()
            # _img = _li.xpath("a/img")

            _link = _li.xpath("a/@href").extract()[0]
            _thumb = _li.xpath("a/img/@data-original").extract()[0]
            _title = _li.xpath("span/a/text()").extract()[0]
            _time = _li.xpath("span/text()").extract()[0]
            # _view = _li.xpath("span[3]/text()").extract()

            # _link = _li.xpath("a[1]/@href").extract()
            # _thumb = _li.xpath("a[1]/img/@data-original").extract()
            # _title = _li.xpath("span[1]/a[1]/text()").extract()
            # _time = _li.xpath("span[2]/text()").extract()

            item['title'] = _title
            item['thumb'] = _thumb
            item['time'] = _time
            item['link'] = _link
            #
            # print(_title)
            # print(_time)
            # print(_thumb)
            # print(_link)
            # print("---------")
            # # yield的作用 http://www.runoob.com/w3cnote/python-yield-used-analysis.html
            yield item
        print("================================================")

    def parseContent(self, response):
        pass