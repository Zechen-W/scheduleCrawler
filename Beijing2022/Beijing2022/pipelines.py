# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import re


class Beijing2022Pipeline(object):
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        time = adapter.get('time')
        if time != '小决赛后' and not re.findall(r'\d', time):
            raise DropItem(f"Dropping item {item}")
        return item

    # def open_spider(self, spider):
    #     self.file = open('./result.txt', 'w')
    #
    # def close_spider(self, spider):
    #     self.file.close()
