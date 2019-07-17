import scrapy
from mzitu.items import TestItem

#run "scrapy crawl TestSpider"
class TestSpider(scrapy.Spider):
    name = 'TestSpider'
    allowed_domains = ['lab.scrapyd.cn']
    start_urls = ['http://lab.scrapyd.cn/archives/55.html']

    def parse(self, response):
        item = TestItem()  # 实例化item
        imgurls = response.css(".post img::attr(src)").extract() # 注意这里是一个集合也就是多张图片
        item['imgUrl'] = imgurls
        yield item
        pass