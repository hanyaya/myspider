# -*- coding: utf-8 -*-
import scrapy
from autopjt.items import AutopjtItem

class AutospdSpider(scrapy.Spider):
    name = 'autospd'
    allowed_domains = ['dangdang.com']
    start_urls = ['http://book.dangdang.com/01.36.htm']


    def parse(self,response):
        new_url = response.xpath("//li/a[@class='img']/@href").extract()
        for i in range(0,len(new_url)):#上面分析得出的每一个url都需要单独爬取一次，也就是爬取的最小单元，所以要给每一次爬取都初始化一次item来存放数据。
            item = AutopjtItem()
            item['link'] = new_url[i]#给item['link']赋值，赋给要进入下一层的url。
            yield scrapy.Request(item['link'],meta={'item':item},callback=self.parse2)


    def parse2(self,response):
        item = response.meta['item']#接受上一个函数传入的对应的参数item。
        item['name'] = response.xpath("//div[@class='name_info']/h1/text()").extract()
        item['price'] = response.xpath("//p[@id='dd-price']/text()").extract()
        #item['link'] = response.xpath()
        item['comnum'] = response.xpath("//div[@class='describe_detail']/span/text()").extract()


        return item
        #这里返回的item包含了item里面的四项，link属性在parse中就已经找到了，并且通过Request传给了parse2，传了下来