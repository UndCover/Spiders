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
import mzitu.settings as settings
from mzitu.items import MzituItem,ImageItem
from pathlib import Path

class MzituPipeline(ImagesPipeline):
    headers = {'Referer': "https://www.mzitu.com/",'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
    def get_media_requests(self, item, info):
        if isinstance(item,MzituItem):
            # yield print('title'+str(self.counter1)+'===========>: '+item['title'])
            yield Request(url=item['thumb'],headers=self.headers)
        elif isinstance(item,ImageItem):
            # yield print('folder'+str(self.counter2)+'===========>: '+item['folder'])
            yield Request(url=item['src'],headers=self.headers)
        # if type(item)==MzituItem:
        #     pass
        # elif type(item)==ImageItem:
        #     pass

        # thumb_url = item['thumb']
        # # yield Request(url=thumb_url,headers=self.headers)
        # yield print("================================================")
    
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        
        if isinstance(item,MzituItem):
            newname = item['time']+item['title']+'.jpg'
            os.rename(settings.IMAGES_STORE+image_paths[0],settings.IMAGES_STORE+'full/'+newname)
            pass
        elif isinstance(item,ImageItem):
            srcArray = item['src'].split('/')
            fileName = srcArray[len(srcArray)-1]
            folderPath = settings.IMAGES_STORE+'full/'+item['folder']
            folder = Path(folderPath)
            if folder.exists():
                pass
            else:
                folder.mkdir()
            os.rename(settings.IMAGES_STORE+image_paths[0],folderPath+'/'+fileName)
            pass
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