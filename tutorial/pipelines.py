# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class TutorialPipeline(object):
    def process_item(self, item, spider):
        with open("weixin.txt", 'a') as fp:
            fp.write(item['c2_title'].encode("utf8") + '\n')
            # fp.write(item['url'].encode("utf8") + '\n')
        # return item
