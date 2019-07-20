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
from mzitu.items import MzituItem,ImageItem,PicContentItem,InformationItem
from pathlib import Path
import sqlite3
import re
from mzitu import utils
import time

class TestPipeline(object):
    def process_item(self, item, spider):
        # self.count = self.count + 1
        return item

    def open_spider(self,spider):
        self.count = 0
        self.startTime = time.localtime(time.time())
        print("=======TestPipeline open_spider======")

    def close_spider(self,spider):
        self.endTime = time.localtime(time.time())
        print("=======TestPipeline close_spider======")
        print("count      : "+str(self.count))
        print("start time : "+time.strftime("%Y-%m-%d %H:%M:%S", self.startTime))
        print("end   time : "+time.strftime("%Y-%m-%d %H:%M:%S", self.endTime))

class DbPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, InformationItem):
            if item['sql'] == 0:
                self.insert_main(item)
            elif item['sql'] == 1:
                self.update_main(item)
        elif isinstance(item, PicContentItem):
            self.insert_content(item)
        return item
    def open_spider(self,spider):
        self.count = 0
        self.connector = sqlite3.connect(utils.DB_FILE)
        self.create_table()

    def close_spider(self,spider):  
        self.connector.commit()
        self.connector.close()

    def create_table(self):
        conn = self.connector
        try:
            conn.execute(utils.DB_CREATE_TABLE_MAIN)
            conn.execute(utils.DB_CREATE_TABLE_CONTENT)
        except Exception as e:
            print(e)
        conn.commit()
        
    def insert_main(self,item):
        # tmp_id = item['link'].split('/')
        # tb_id = tmp_id[len(tmp_id)-1]

        tb_id = item['pid']
        tb_title = item['title']
        tb_fileName = re.sub('[\/:*?"<>|]','', tb_title)
        tb_link = item['link']
        tb_postDate = item['time']
        tb_thumb = item['thumb']
        tb_picCount = item['number']
        tb_tags = item['tags']
        tb_done = 0

        self.count = self.count + 1
        insert_sql = "INSERT INTO Information (ID,Title,FileName,Link,PostDate,Thumb,PicCount,Tags,Done) VALUES ('%s','%s','%s','%s','%s','%s',%s,'%s',%s)" %(tb_id,tb_title,tb_fileName,tb_link,tb_postDate,tb_thumb,tb_picCount,tb_tags,tb_done)
        conn = self.connector
        try:
            conn.execute(insert_sql)
        except Exception as e:
            print(e)
        if self.count // 10000 > 0:
            conn.commit()
            self.count = 0

    def update_main(self,item):
        tb_id = item['pid']
        tb_picCount = item['number']
        tb_done = item['done']

        insert_sql = "update Information set PicCount = %s ,Done = %s where id = '%s'" %(tb_picCount,tb_done,tb_id)
        conn = self.connector
        try:
            conn.execute(insert_sql)
        except Exception as e:
            print(e)
        if self.count // 10000 > 0:
            conn.commit()
            self.count = 0

    def insert_content(self,item):
        # https://i.meizitu.net/2019/02/01e01.jpg
        t_name = item['link'].split('/')
        t_id = t_name[len(t_name)-1].split('.')
        tb_id = item['pid']+'_'+t_id[0]
        tb_pid = item['pid']
        tb_link = item['link']
        tb_done = 0
        
        self.count = self.count + 1
        insert_sql = "INSERT INTO PicContent (ID,Pid,Link,Done) VALUES ('%s','%s','%s','%s')" %(tb_id,tb_pid,tb_link,tb_done)
        conn = self.connector
        try:
            conn.execute(insert_sql)
        except Exception as e:
            print(e)
        if self.count // 10000 > 0:
            conn.commit()
            self.count = 0

class MzituPipeline(ImagesPipeline):
    headers = {'Referer': "https://www.mzitu.com/",'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
    def get_media_requests(self, item, info):
        if isinstance(item,MzituItem):
            # yield print('title'+str(self.counter1)+'===========>: '+item['title'])
            yield Request(url=item['thumb'],headers=self.headers)
        elif isinstance(item,ImageItem):
            # yield print('~~~~~~~~~~~~~~~~~~~~~'+item['src'])
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

class TestImagePipeline(ImagesPipeline):
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