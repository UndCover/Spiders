#coding=utf-8
#!/usr/bin/python
# 导入requests库
import requests
# 导入文件操作库
import os
import re
import bs4
from bs4 import BeautifulSoup
import sys
import time
import importlib
importlib.reload(sys)
# 给请求指定一个请求头来模拟chrome浏览器
global headers
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
# 爬图地址
mziTu = 'https://www.mzitu.com/'
global sParam 
sParam = {
    'multi':0,
    'index':-1,
    'path':'',
    'local':'',
    'single':1,
    'firstpage':-1,
    'endpage':-1
}

import getopt,optparse
try:
    options,args = getopt.getopt(sys.argv[1:],"hi:p:l:s:f:e:",["help","index=","path=","local=","single=","firstpage=","endpage="])
except getopt.GetoptError:
    sys.exit()

def usage():
    print(u"""
    -h / --help     : 使用帮助
    -i / --index    : 最后一页的位置
    -p / --path     : 自定义存储路径
    -d / --local    : 本地模式 需要下载index.html到路径
    -s / --single   : 是否单页模式 0为多页模式
    -f / --firstpage: 第一页的页码
    -e / --endpage  : 最后一页的页码
    """)

def parse_param():
    if(len(sys.argv)<2):
        print("无参数")
        return True
    try:
        for name,value in options:
            if not name:
                usage()
                return False
            if name in ("-h","--help"):
                usage()
                return False
            if name in ("-s","--single"):
                sParam['single'] = int(value)
            if name in ("-f","--firstpage"):
                sParam['firstpage'] = int(value)
            if name in ("-e","--endpage"):
                sParam['endpage'] = int(value)
            if name in ("-i","--index"):
                sParam['index'] = int(value)
            if name in ("-p","--path"):
                sParam['path'] = value
            if name in ("-l","--local"):
                sParam['local'] = value
        return True
    except Exception as e:
        print("参数异常")
        print(e)
        return False

# 创建文件夹
def createFile(file_path):
    if os.path.exists(file_path) is False:
        os.makedirs(file_path)
    # 切换路径至上面创建的文件夹
    os.chdir(file_path)
# 下载文件
def download(page_no, file_path, isLocal,index):
    global headers
    if isLocal:
        # 本地解析
        f = open(page_no,'rb')
        soup_sub  = BeautifulSoup(f.read(), 'html.parser')
    else:
        # global headers
        res_sub = requests.get(page_no, headers=headers)
        # 解析html
        soup_sub = BeautifulSoup(res_sub.text, 'html.parser')

    all_li = soup_sub.find('div',class_='postlist').find_all('li')

    count = 0
    for li in all_li:
        if(index > 0 and count >= index):
            return;
        count = count + 1
        print("内页第几页：" + str(count))
        
        # 防止<li>内找不到 <a> 
        try:
        	tA = li.find('a')
	        tImg = tA.find('img');
	        tAlt = tImg.get('alt')
	        tSrc = tImg.get('data-original')
	        tTime = li.find('span',class_='time')
	        tFileName = tTime.contents[0]+tAlt
        except Exception as e:
        	count = count - 1
        	continue
            
        # 替换特殊字符
        rightName = re.sub('[\/:*?"<>|]','', tFileName)
        tFullName = file_path + rightName + ".jpg"

        newPath = file_path + rightName
        try:
            headers = {'Referer': mziTu}
            img = requests.get(tSrc, headers=headers)
            # print('开始保存图片')
            f = open(tFullName, 'ab')
            f.write(img.content)
            # print(tFullName, '图片保存成功！')
            f.close()
            # 创建文件夹
            createFile(newPath)
        except Exception as e:
            print(e)

        # 提取href
        href = tA.attrs['href']
        print("套图地址：" + href)
        res_sub_1 = requests.get(href, headers=headers)
        soup_sub_1 = BeautifulSoup(res_sub_1.text, 'html.parser')
        # ------ 这里最好使用异常处理 ------
        try:
            # 获取套图的最大数量
            spans = soup_sub_1.find('div',class_='pagenavi').find_all('span')
            span_length = len(spans)
            pic_max = spans[span_length-2].text
            # pic_max = soup_sub_1.find('div',class_='pagenavi').find_all('span')[6].text
            print("套图数量：" + pic_max)
            for j in range(1, int(pic_max) + 1):
                # print("子内页第几页：" + str(j))
                # j int类型需要转字符串
                href_sub = href + "/" + str(j)
                print(href_sub)
                res_sub_2 = requests.get(href_sub, headers=headers)
                soup_sub_2 = BeautifulSoup(res_sub_2.text, "html.parser")
                img = soup_sub_2.find('div', class_='main-image').find('img')
                if isinstance(img, bs4.element.Tag):
                    # 提取src
                    url = img.attrs['src']
                    array = url.split('/')
                    file_name = array[len(array)-1]
                    # print(file_name)
                    # 防盗链加入Referer
                    headers = {'Referer': href}
                    img = requests.get(url, headers=headers)
                    # print('开始保存图片')
                    f = open(file_name, 'ab')
                    f.write(img.content)
                    # print(file_name, '图片保存成功！')
                    f.close()
        except Exception as e:
            print(e)

# 主方法	
def main():
    # 定义存储位置
    save_path = '/Users/UndCover/Desktop/mDocuments/mzitu'

    # print(current_date)
    if(parse_param()):
        current_date = time.strftime('%Y-%m-%d-',time.localtime(time.time()))
        isSingle = sParam['single'] > 0
        lastIndex = sParam['index']
        if sParam['path']!='':
            print(sParam['path'])
            save_path = sParam['path']
        # 创建文件夹
        createFile(save_path)
        localPath = sParam['local']
        isLocal = localPath != ''

        firstPage = sParam['firstpage']
        endPage = sParam['endpage']

        if isLocal:
            # 本地解析
            f = open(localPath,'rb')
            soup = BeautifulSoup(f.read(), 'html.parser')
        else:
            # res = requests.get(mziTu, headers=headers)
            res = requests.get(mziTu, headers=headers)
            # 使用自带的html.parser解析
            soup = BeautifulSoup(res.text, 'html.parser')

        try:
            # 获取首页总页数
            img_max = soup.find('div', class_='nav-links').find_all('a')[3].text
        except Exception as e:
            # 获取首页总页数
            img_max = '1'
        print("总页数:"+img_max)

        p_time = 0
        if isSingle or isLocal:
            print("单页模式")
            if isLocal :
                page = localPath
            else : 
                if firstPage > 1:
                    page = mziTu + 'page/' + str(firstPage)
                else: 
                    page = mziTu

            file = save_path + '/' + current_date + '1/'
            createFile(file)
            # 下载每页的图片
            print("套图页码：" + page)
            download(page,file,isLocal,lastIndex)
        else:
            print("多页模式")
            if endPage < 0 or endPage > int(img_max):
                endPage = int(img_max)
            for i in range(1, endPage + 1):
                if i < firstPage:
                    continue
                # 获取每页的URL地址
                if i == 1:
                    page = mziTu
                else:
                    page = mziTu + 'page/' + str(i)
                file = save_path + '/' + current_date + str(i)+'/'
                createFile(file)
                # 下载每页的图片
                print("套图页码：" + page)
                if i == endPage:
                    download(page,file,False,lastIndex)
                else:
                    download(page,file,False,-1)

if __name__ == '__main__':
    main()
