# -*- coding: utf-8 -*-
import scrapy
from autopjt.items import AutopjtItem


class Myspd2Spider(scrapy.Spider):
    name = 'myspd2'
    allowed_domains = ['dangdang.com']
    start_urls = ['http://book.dangdang.com/01.36.htm']

    def parse(self, response):
        item = AutopjtItem()#其实如果下面不用item['link']存放新的url。这里是不用实例化item的。如果父页面中也有要提取的数据，
        #（该数据！= 传下去的url）那么最好就是这里在for循环中实例化item，然后将整个都传下去。
        item['link'] = response.xpath("//li/a[@class='img']/@href").extract()
        for url in item['link']:#因为Request中的第一个参数必须是字符串，也就是默认是一个url。所以，不能直接传item['link']这个列表
            yield scrapy.Request(url,meta={'url':url},callback=self.parse2)#传url给回调函数，而不是item。因为，这里基本没用item的其他属性。
            #meta是用来给该request传递数据的，将数据传递给下一个函数。这里只传递了parse中要使用的url，
            #这里的这种写法是因为刚好传下去的url正好是父页面中需要获取的数据。才可以通过传url，同时也传了需要的数据（item['link']）
            #或者这里meta可以多传一组数据，用字典表示，


    def parse2(self,response):
        item = AutopjtItem()#接受上一个函数传入的对应的参数item。
        item['name'] = response.xpath("//div[@class='name_info']/h1/text()").extract()
        item['price'] = response.xpath("//p[@id='dd-price']/text()").extract()
        #item['link'] = response.xpath()
        item['comnum'] = response.xpath("//div[@class='describe_detail']/span/text()").extract()
        item['link'] = response.meta['url']#这里接受了从parse中传下来的url，并且修改了它，

        return item



