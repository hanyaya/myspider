# -*- coding: utf-8 -*-
import scrapy
from autopjt.items import AutopjtItem
import random
#实现动态修改（添加）start_urls.这时，不需要指定start_urls.只需要重写start_requests函数，如下：


class Myspd2Spider(scrapy.Spider):
    name = 'myspd3'
    allowed_domains = ['dangdang.com']
    #redis_key = 'dang_spider:start_urls'
    #start_urls = ['http://book.dangdang.com/01.36.htm']

    def parse(self, response):
        item = AutopjtItem()
        #next_url = response.xpath("//li/a[@class='img']/@href").extract()
        item['link'] = response.xpath("//li/a[@class='img']/@href").extract()
        for url in item['link']:#因为Request中的第一个参数必须是字符串，也就是默认是一个url。所以，不能直接传item['link']这个列表
            yield scrapy.Request(url,meta={'url':url},callback=self.parse2)#传url给回调函数，而不是item。因为，这里基本没用item的其他属性。
            #meta是用来给该request传递数据的，将数据传递给下一个函数


    def parse2(self,response):
        item = AutopjtItem()#接受上一个函数传入的对应的参数item。
        item['name'] = response.xpath("//div[@class='name_info']/h1/text()").extract()
        item['price'] = response.xpath("//p[@id='dd-price']/text()").extract()
        #item['link'] = response.xpath()
        item['comnum'] = response.xpath("//div[@class='describe_detail']/span/text()").extract()
        item['link'] = response.meta['url']#这里接受了从parse中传下来的url，并且修改了它，

        return item

    def start_requests(self):
        pages=[]
        for i in range(1,10):
            x = random.randint(1,20)
            url="http://book.dangdang.com/01."+str(x)+".htm"
            page=scrapy.Request(url)
            pages.append(page)
        return pages






