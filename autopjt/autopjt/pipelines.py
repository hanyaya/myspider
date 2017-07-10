# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
class AutopjtPipeline(object):
    def __init__(self):
        self.file = codecs.open('mydata.json','wb',encoding='utf8')

    def process_item(self, item, spider):
        i = json.dumps(dict(item),ensure_ascii=False)
        line = str(i) + '\n'
        self.file.write(line)
        return item
    def cloes_spider(self,spider):
        self.file.close()