# Spiders

这里会不定期更新一些定向爬虫

### mzitu.com

####功能
* 定向爬取网站下所有套图，下载thumb图，并以目录整理

####不足

* 目前没有做套图完整性检查
* 没有异常重联机制
* 现在为按页爬去，爬去完一页继续爬取另外一页，所以会存在网站post新图的时候，丢失一部分图片的情况
* 命令只有结束的index，没有做开始的index

暂时就这些，由于打算启用Scrapy框架来重新做这个爬虫，所以目前这个简易爬虫就暂时不维护了