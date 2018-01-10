# _*_coding:utf-8 _*_
import requests
from scrapy.http import HtmlResponse

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

url="https://mp.weixin.qq.com/s?timestamp=1515226337&src=3&ver=1&signature=UwejyZLADBsL1wS7sEpBWgiEA9c-ubXCDoHsd8-7625LiTyGwmPK0NwuCRqWd25TxDn3fHMu5qjVmVAi9PodUH8q7rsiMGZdNsNUnKuNsz1gweB7Wm9WoXjwLNHLFUouSDtb4ar9usTBrhThXxb7OckV4ZA3U4I4TeINmnp*UqU="
# aa =requests.get(url)
url="https://mp.weixin.qq.com/s?timestamp=1515479263&src=3&ver=1&signature=WdySDZn33Ws7Hz5AahNIJKIeeUyH4yYlaEpP5JIYyYlBWBrQsiDOIC73SUjMbr19V*StqhDX9xC5urxwH6amr*Ybcs26lVqwxOzYmDW1HpWpxd6o1abXY-SWXcvqEG7TUxebI*znOGJSWj67r6A5PyY1AOA0HfnSGJfQL9OIvYo="


def request_static():
    url = "https://mp.weixin.qq.com/s?timestamp=1515479263&src=3&ver=1&signature=WdySDZn33Ws7Hz5AahNIJKIeeUyH4yYlaEpP5JIYyYlBWBrQsiDOIC73SUjMbr19V*StqhDX9xC5urxwH6amr*Ybcs26lVqwxOzYmDW1HpWpxd6o1abXY-SWXcvqEG7TUxebI*znOGJSWj67r6A5PyY1AOA0HfnSGJfQL9OIvYo="
    url="https://mp.weixin.qq.com/s?timestamp=1515574251&src=3&ver=1&signature=xsZdozV1JPS2K8SuXJ8TKRjG3vSQNif7rgij0pzt7-vYrECexzvsL4oV68xD4eqBHkrMG0FowOEOJJU0fqYwwYxtgTTs4zL-HQ0LoQit6iD1Y5JWvOxXBsYrYh1YYNFREOwkJQ-vAVwtdnOiR4k8DUVGIaAbhPgm**9Re0KeV-8="
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; windows NT)'
    headers = {'User-Agent': user_agent}
    r= requests.post(url, headers=headers)
    body=r.content
    with open('static.html','wb') as fd:
        fd.write(body)


    return HtmlResponse(url=url, body=body, encoding='utf-8')


def parse_item(response=request_static()):
    # item = ArticleItem()
    print "####parse_item url:" + response.url

    article_title = get_text(response.xpath('//h2[@id="activity-name"]/text()').extract())
    print 444444,article_title

    article_time = get_text(response.xpath('//em[@id="post-date"]/text()').extract())
    print "article_time:" + article_time

    article_content_body = response.xpath('//div[@id="js_content"]/blockquote/span').extract()
    # print 'article_content_body:'+article_content_body
    article_content = get_text(article_content_body)
    print 445345345,article_content

    article_content_body = response.xpath('//div[@id="js_content"]/blockquote')
    for body_table in article_content_body:
        table_title = body_table.xpath('./span/strong/span/strong/span/text()|./span/strong/span/text()|./span/strong/span/span/strong/span/text()').extract()
        table_title = get_text(table_title)
        print 'table_title:'+table_title

    article_content_body = response.xpath('//div[@id="js_content"]/table').extract()
    # print 'article_content_body:'+article_content_body
    table_content_body = get_text(article_content_body)
    print 'table_content_body:', table_content_body
    table_content_body = response.xpath('//div[@id="js_content"]/table')

    for body_table in table_content_body:
        # table_detail = body_table.xpath('./tbody/tr/td[not(@rowspan)]/span/text()').extract()
        table_detail = body_table.xpath('./tbody/tr/td[not(@rowspan)]/span')
        table_detail = body_table.xpath('./tbody/tr')
        # print 'type', type(table_detail)
        # print 'length:', len(table_detail)
        for kk in table_detail:
            # info = kk.xpath('string(.)').extract()
            # print 'length:', len(kk.xpath('./td'))
            # print 'type', type(kk.xpath('./td'))

            if len(kk.xpath('./td')) <= 3:
                table_detail_1 = kk.xpath('./td[not(@rowspan)]/span/text()').extract()
                for v in table_detail_1:
                    # print 'table_detail_1:'+v
                    pass
            elif len(kk.xpath('./td')) > 3:
                table_detail_1 = kk.xpath('./td[not(@rowspan)]/span/text()').extract()
                for v in table_detail_1[-3:]:
                    # print 'table_detail_11111:' + v
                    pass




            # num =count( kk.xpath('./td'))

            # print 'length:', len(num)
            # print 'type',type(info)
            # print 'length:',len(info)
            # for i in info[-3:]:
            #     print i
        # table_detail = get_text(table_detail)
        # print 'table_detail:' + table_detail



    for body_table in table_content_body:
        table_detail = body_table.xpath('./tbody/tr/td/@rowspan').extract()
        table_detail_dis = body_table.xpath('./tbody/tr/td[@rowspan]/span/text()').extract()
        if '2' in table_detail:
            table_detail_dis.insert(table_detail.index('2')+1,'空')

        m=0
        for i in table_detail:
            print 'district_num:',table_detail[m]

            if table_detail_dis[m] == "    （棚前）" or table_detail_dis[m] == "    （棚后）" or table_detail_dis[m] == "    ":
            # if table_detail_dis[m] == "    （棚前）" or table_detail_dis[m] == "    （棚后）" :

                table_detail_dis.pop(m)
                # print 444444,table_detail_dis[m]
            # if int(table_detail[m]) == 2:
            #     print 'district_num: 空'
            #     m+=1
            #     continue

            table_detail_dis[m] = table_detail_dis[m] if table_detail_dis[m].strip() else u'空1111'
            print 'district_name:',table_detail_dis[m]
            m += 1
        # table_detail = get_text(table_detail)
        # print 'table_detail:' + table_detail







    # tables_detail = response.xpath('//*[@id="js_content"]')
    # print tables_detail
    # for table in tables_detail:
    #     table_title = ""
    #     # table_tltle = response.xpath('./blockquote/span/text()').extract()
    #     table_tltle = response.xpath('./section').extract()
    #     print 88888888888888, table_tltle


def get_text(texts):
    text = ""
    if len(texts) > 0:
        for tmp in texts:
            text = text + tmp
    return text.strip()

parse_item()