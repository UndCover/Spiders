# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy import settings
# from scrapy.middleware._retry import RetryMiddleware
from scrapy.downloadermiddlewares.retry import RetryMiddleware
class MyRetryMiddleware(RetryMiddleware):
    def process_exception(self, request, exception, spider):
        print("UndCover =============== retry")
        if not request.meta.get('dont_retry', False):
            print("retry: "+request.url)
            return self._retry(request, exception, spider)

class MzituSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    # def __init__(self, settings):
    def __init__(self):
        # if not settings.getbool('RETRY_ENABLED'):
        #     raise NotConfigured
        # self.max_retry_times = settings.getint('RETRY_TIMES')
        # self.retry_http_codes = set(int(x) for x in settings.getlist('RETRY_HTTP_CODES'))
        # self.priority_adjust = settings.getint('RETRY_PRIORITY_ADJUST')
 
        
        self.priority_adjust = 100
        self.max_retry_times = 255
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        #request = response.request.copy()
        #original_request_url 为自定义设置的初始请求URL，在用IP代理时部分代理会修改URL

        # request = response.request.replace(url = response.meta.get('original_request_url', response.url))
        # #retry_times 为自定义重试次数
        # retry_times = request.meta.get('retry_times', 0)
        # request.dont_filter = True  #这个一定要有，否则重试的URL会被过滤
        # request.meta['retry_times'] = retry_times +1
        
        # return request

        print("process_spider_exception")
        request = response.request
        #retry_times 为自定义重试次数
        retry_times = request.meta.get('retry_times', 0)
        request.dont_filter = True  #这个一定要有，否则重试的URL会被过滤
        request.meta['retry_times'] = retry_times +1
        
        if not request.meta.get('dont_retry', False):
            yield self._retry(request,exception,spider)
            # return self._retry(request, exception, spider)
            # self._retry(request, exception, spider)

        # print('An Exception MzituSpiderMiddleware ===================================')
         # 如果发生了Exception列表中的错误，进行重试
        # return self._retry(request, exception, spider)
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
    
    def _retry(self, request, reason, spider):
        retries = request.meta.get('retry_times', 0) + 1
 
        retry_times = self.max_retry_times
 
        if 'max_retry_times' in request.meta:
            retry_times = request.meta['max_retry_times']
 
        stats = spider.crawler.stats
        if retries <= retry_times:
            print("Retrying %(request)s (failed %(retries)d times): %(reason)s",
                    request, retries, reason)
            # logger.debug("Retrying %(request)s (failed %(retries)d times): %(reason)s",
            #              {'request': request, 'retries': retries, 'reason': reason},
            #              extra={'spider': spider})
            retryreq = request.copy()
            retryreq.meta['retry_times'] = retries
            retryreq.dont_filter = True
            retryreq.priority = request.priority + self.priority_adjust
 
            # if isinstance(reason, Exception):
            #     reason = global_object_name(reason.__class__)
 
            stats.inc_value('retry/count')
            stats.inc_value('retry/reason_count/%s' % reason)
            return retryreq
        else:
            stats.inc_value('retry/max_reached')
            print("Gave up retrying %(request)s (failed %(retries)d times): %(reason)s",
                    request, retries, reason)
            # logger.debug("Gave up retrying %(request)s (failed %(retries)d times): %(reason)s",
            #              {'request': request, 'retries': retries, 'reason': reason},
            #              extra={'spider': spider})


class MzituDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        print('An Exception MzituDownloaderMiddleware ===================================')
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
