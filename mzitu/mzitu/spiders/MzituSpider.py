# -*- coding: utf-8 -*-
import scrapy
import time
# import logging
from mzitu.items import MzituItem,ImageItem,PicContentItem,InformationItem
import re

class DatabaseSpider(scrapy.Spider):
    # logging.basicConfig(level=logging.DEBUG)
    name = 'db_spider'
    allowed_domains = ['mzitu.com']
    start_urls = ['https://www.mzitu.com/']
    urls = []
    count = 0
    total = 1

    stop = False
    endTime = '2019-02-12'
    def parse(self, response):
        self.count = self.count + 1
        for _li in response.xpath("//*[@id=\"pins\"]/li"):
            item = InformationItem()
            _link = _li.xpath("a/@href").extract()[0]
            _thumb = _li.xpath("a/img/@data-original").extract()[0]
            _title = _li.xpath("span/a/text()").extract()[0]
            _time = _li.xpath("span/text()").extract()[0]

            t_pid = _link.split('/')
            _pid = t_pid[len(t_pid)-1]

            item['title'] = _title
            item['thumb'] = _thumb
            item['time'] = _time
            item['link'] = _link
            item['pid'] = _pid
            item['number'] = 0
            item['sql']=0
            
            # if self.endTime <= _time:
            #     yield item
            # else:
            #     self.stop = True
                
            # yield的作用 http://www.runoob.com/w3cnote/python-yield-used-analysis.html 
            # 开启请求子地址，比较耗时
            yield scrapy.Request(_link,meta={'item':item}, callback=self.parse_content)
        if self.count < 2:
            a_nav = response.xpath("//div[@class=\"nav-links\"]/a/text()").extract()
            self.total = int(a_nav[len(a_nav)-2]) + 1
            self.urls = ['https://www.mzitu.com/page/%s'% p for p in range(2, self.total)]
            for url in reversed(self.urls):
                if self.stop :
                    break
                yield scrapy.Request(url, callback=self.parse)

        # todo 1. 区域控制 2. 更新数据 3. 下载
    def parse_content(self,response):
        # 拼装套图数量
        item = response.meta['item']
        a_nav = response.xpath("//div[@class=\"pagenavi\"]/a")
        _pageNum = a_nav.xpath("span/text()").extract()[len(a_nav)-2]

        item['number'] = int(_pageNum)
        arrTags = response.xpath("//div[@class=\"main-tags\"]/a/text()").extract()
        _tags = ','.join(arrTags)
        item['tags']=_tags
        yield item

        # 返回第一个item 
        # picItem = PicContentItem()
        # _pid = item['pid']
        # # _imgLink = response.xpath("//div[@class=\"main-image\"]/p/a/img/@src").extract()[0]
        # _imgLink = response.xpath("//div[@class=\"main-image\"]/p//img/@src").extract()[0]
        
        # picItem['pid']=_pid
        # picItem['link']=_imgLink
        # yield picItem
        # # 开启循环
        # t_urls = [response.url+'/%s'% p for p in range(2, int(_pageNum) + 1)]
        # for url in reversed(t_urls):
        #     yield scrapy.Request(url,meta={'pid':_pid}, callback=self.parse_next)
    def parse_next(self,response):
        picItem = PicContentItem()
        _pid = response.meta['pid']
        _imgLink = response.xpath("//div[@class=\"main-image\"]/p//img/@src").extract()[0]
            
        picItem['pid']=_pid
        picItem['link']=_imgLink
        yield picItem

class MzituSpider(scrapy.Spider):
    # logging.basicConfig(level=logging.DEBUG)
    name = 'mzitu'
    allowed_domains = ['mzitu.com']
    start_urls = ['https://www.mzitu.com/']
    headers = {'Referer': "https://www.mzitu.com/",'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}

    def parse(self, response):
        print("================================================")
        for _li in response.xpath("//*[@id=\"pins\"]/li"):
            item = MzituItem()

            _link = _li.xpath("a/@href").extract()[0]
            _thumb = _li.xpath("a/img/@data-original").extract()[0]
            _title = _li.xpath("span/a/text()").extract()[0]
            _time = _li.xpath("span/text()").extract()[0]
            
            item['title'] = re.sub(r'[？\\*|“<>:/]', '', _title)
            item['thumb'] = _thumb
            item['time'] = _time
            item['link'] = _link

            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
            print(_link)
            yield item

            yield scrapy.Request(_link,meta={'item':item},callback=self.parseContent,headers=self.headers)
            
        print("================================================")
    def parseContent(self, response):
        # _title = response.meta['title']
        _item = response.meta['item']
        imgPath = response.xpath("//*[@class=\"main-image\"]/p/a/img")
        _src = imgPath.xpath("@src").extract()[0]

        _spans = response.xpath("//*[@class=\"pagenavi\"]/*/span")
        pageNum = int(_spans[len(_spans)-2].xpath("text()").extract()[0])

        imageInfo = ImageItem()
        imageInfo['folder'] = _item['time']+_item['title']
        imageInfo['src'] = _src
        imageInfo['refer'] = _item['link']
        
        print('**********************************************\n'+_item['link']+'\n'+_src)
        yield imageInfo

        for i in range(2,pageNum+1):
            nextUrl = _item['link']+'/{page}'.format(page=i)

            yield scrapy.Request(nextUrl,meta={'item':_item},callback=self.parseContent,headers=self.headers)

    # def handleError(self, failure):
    #     self.logger.error(repr(failure))


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