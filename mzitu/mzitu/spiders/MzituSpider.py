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
from mzitu.items import MzituItem,ImageItem

class MzituSpider(scrapy.Spider):
    # logging.basicConfig(level=logging.DEBUG)
    name = 'mzitu'
    allowed_domains = ['mzitu.com']
    start_urls = ['https://www.mzitu.com/']

    def parse2(self, response):
        print("================================================")
        for _li in response.xpath("//*[@id=\"pins\"]/li"):
            item = MzituItem()

            _link = _li.xpath("a/@href").extract()[0]
            _thumb = _li.xpath("a/img/@data-original").extract()[0]
            _title = _li.xpath("span/a/text()").extract()[0]
            _time = _li.xpath("span/text()").extract()[0]
            
            item['title'] = _title
            item['thumb'] = _thumb
            item['time'] = _time
            item['link'] = _link

            yield item
        print("================================================")

    def parse(self, response):
        print("================================================")
        for _li in response.xpath("//*[@id=\"pins\"]/li"):
            item = MzituItem()

            _link = _li.xpath("a/@href").extract()[0]
            _thumb = _li.xpath("a/img/@data-original").extract()[0]
            _title = _li.xpath("span/a/text()").extract()[0]
            _time = _li.xpath("span/text()").extract()[0]
            
            item['title'] = _title
            item['thumb'] = _thumb
            item['time'] = _time
            item['link'] = _link
            
            yield item

            yield scrapy.Request(_link,meta={'item':item},callback=self.parseContent)

        print("================================================")
    def parseContent(self, response):
        # _title = response.meta['title']
        _item = response.meta['item']
        imgPath = response.xpath("//*[@class=\"main-image\"]/p/a/img")
        _src = imgPath.xpath("@src").extract()[0]

        imageInfo = ImageItem()
        imageInfo['folder'] = _item['time']+_item['title']
        imageInfo['src'] = _src
        imageInfo['refer'] = _item['link']
        
        print('UndCover: '+_src)
        yield imageInfo

    # def parse(self, response):
    #     list = response.css(".list-left dd:not(.page)")
    #     for img in list:
    #         imgname = img.css("a::text").extract_first()
    #         imgurl = img.css("a::attr(href)").extract_first()
    #         imgurl2 = str(imgurl)
    #         print(imgurl2)
    #         next_url = response.css(".page-en:nth-last-child(2)::attr(href)").extract_first()
    #         if next_url is not None:
    #             # 下一页
    #             yield response.follow(next_url, callback=self.parse)

    #         yield scrapy.Request(imgurl2, callback=self.content)

    # def content(self, response):
    #     item = AoisolasItem()
    #     item['name'] = response.css(".content h5::text").extract_first()
    #     item['ImgUrl'] = response.css(".content-pic img::attr(src)").extract()
    #     yield item
    #     # 提取图片,存入文件夹
    #     # print(item['ImgUrl'])
    #     next_url = response.css(".page-ch:last-child::attr(href)").extract_first()

    #     if next_url is not None:
    #         # 下一页
    #         yield response.follow(next_url, callback=self.content)