# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
import os
import requests
from scrapy.exceptions import DropItem

class MzituPipeline(ImagesPipeline):
    fPath = '/Users/UndCover/Desktop/Spider/Spiders/mzitu/test/'
    headers = {'Referer': "https://www.mzitu.com/",'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
    def get_media_requests(self, item, info):
        # 循环每一张图片地址下载，若传过来的不是集合则无需循环直接yield
        thumb_url = item['thumb']
        yield Request(url=thumb_url,headers=self.headers)
    
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        newname = item['time']+item['title']+'.jpg'
        os.rename(self.fPath+image_paths[0],self.fPath+'full/'+newname)
        # os.rename("/neteaseauto/" + image_paths[0], "/neteaseauto/" + newname)
        return item

class TestPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        # 循环每一张图片地址下载，若传过来的不是集合则无需循环直接yield
        for image_url in item['imgUrl']:
            yield Request(image_url)

class MzituPipeline1(object):
    # def process_item(self, item, spider):
    #     return item

    def process_item(self, item, spider):
        self.download_thumb(item,spider)
        # self.write_name(item,spider)
        return item

    def download_thumb(self,item,spider):
        headers = {'Referer': "https://www.mzitu.com/",'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
        # headers = {'Referer': "https://www.mzitu.com/"}
        img = requests.get(item["thumb"], headers=headers)
        f = open(item["title"]+".jpg", 'ab')
        f.write(img.content)
        # print(tFullName, '图片保存成功！')
        f.close()

    def write_name(self,item, spider):
        with open("my_meiju.txt",'a') as fp:
            fp.write(item['title']+"\n")