# _*_coding:utf-8 _*_
#
#借鉴https://github.com/beng0305/WechatSpider,
#动态请求和静态请求相结合，动态和请求自己定义的函数，前2层使用动态请求，第3层使用静态请求（前2层是js生成的网页）
#因为表格的数据不整齐，大量使用了if判断
#
import scrapy
from selenium import webdriver
from datetime import datetime
from scrapy.http import HtmlResponse
import requests
import time
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')
import csv
import codecs
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cdate = (datetime.now()).strftime("%Y%m%d_%H%M")


class QuotesSpider(scrapy.Spider):
    '''
    微信公众号第一层请求
    '''
    name = "quotes"
    start_urls = [
        'http://weixin.sogou.com/weixin?type=1&s_from=input&query=家禽信息PIB'
    ]

    def parse(self, response):
        print "url:" + response.url
        print "response:" + response.__str__()
        account = response.xpath('//a[@uigs="account_name_0"]/@href').extract()[0]
        #打印第一层网页
        # with open('c1_basic.html','wb') as fd:
        #     fd.write(response.body)
        if account is not None:
            body1=self.request_phantomjs(account)
            #打印第二层网页
            # with open('c2_basic.html', 'wb') as fd:
            #     fd.write(body1.body)
            self.parse_list(body1)


    def parse_list(self,response):
        '''
        第二层数据处理
        :param response:
        :return:
        '''
        article_srcs = response.xpath("//div[@class='profile_info']/strong[@class='profile_nickname']/text()").extract()
        article_src = article_srcs[0].strip()
        print "article_src:" + article_src

        date = datetime.now().timetuple()
        dateStr = str(date.tm_year) + u'年' + str(date.tm_mon) + u'月' + str(date.tm_mday) + u'日'
        #获取当天的文章
        # re_path = u'//div[@id="history"]/div[@class="weui_msg_card"]/div[contains(./text(), "{0}")]/../div[@class="weui_msg_card_bd"]/div[@class="weui_media_box appmsg"]'.format(
        #     dateStr)
        #获取近10天的文章
        re_path = u'//div[@id="history"]/div[@class="weui_msg_card"]/div[@class="weui_msg_card_bd"]/div[@class="weui_media_box appmsg"]'
        today_cards = response.xpath(re_path)
        if len(today_cards) <= 0:
            print "《" + article_src + "》今日没有发布内容！"
            return
        i=0
        for card in today_cards:
            article_summary = ""
            article_summarys = card.xpath('./div[@class="weui_media_bd"]/h4/text()').extract()
            for tmp in article_summarys:
                article_summary = article_summary + tmp
            article_summary = article_summary.strip()
            if '行情早报与趋势分析' in article_summary:
                print "article_summary:" + article_summary
                article_main_url = "https://mp.weixin.qq.com"
                article_main_urls = card.xpath('./div[@class="weui_media_bd"]/h4/@hrefs').extract()
                for tmp in article_main_urls:
                    article_main_url = article_main_url + tmp
                article_main_url = article_main_url.strip()
                print 'article_main_url:'+article_main_url
                article_3ceng = self.request_static(article_main_url)
                '''打印下载的html'''
                # with open('3ceng{0}.html'.format(i), 'wb') as fd:
                #     fd.write(article_3ceng.body)
                i+=1
                self.parse_item(article_3ceng)


    def parse_item(self, response):
        '''第三层数据处理'''
        print "####parse_item url:" + response.url
        article_title = self.get_text(response.xpath('//h2[@id="activity-name"]/text()').extract())
        article_time = self.get_text(response.xpath('//em[@id="post-date"]/text()').extract())
        print "article_time:" + article_time
        table_titles_x = response.xpath('//div[@id="js_content"]/blockquote')
        for table_title_x in table_titles_x:
            table_title = table_title_x.xpath(
                './span/strong/span/strong/span/text()|./span/strong/span/text()|./span/strong/span/span/strong/span/text()').extract()
            table_title = self.get_text(table_title)
            print 'table_title:' + table_title

            if "明日鸡苗" in table_title:
                table_div_num = 1
                article_catagory = '明日鸡苗'
                self.info_input(response,table_title,article_time,article_title,table_div_num,article_catagory)
            elif "今日毛鸡" in table_title:
                table_div_num =2
                article_catagory = '今日毛鸡'
                self.info_input(response, table_title, article_time, article_title,table_div_num,article_catagory)
            elif "今日山东麻鸡" in table_title:
                table_div_num = 3
                article_catagory = '今日山东麻鸡'
                self.info_input(response, table_title, article_time, article_title, table_div_num, article_catagory)
            elif "明日鸭苗" in table_title:
                table_div_num = 1
                article_catagory = '明日鸭苗'
                self.info_input(response, table_title, article_time, article_title, table_div_num, article_catagory)
            elif "今日毛鸭" in table_title:
                table_div_num = 2
                article_catagory = '今日毛鸭'
                self.info_input(response, table_title, article_time, article_title, table_div_num, article_catagory)


    def info_input(self,response,table_title,article_time,article_title,table_div_num,article_catagory):
        table_data_3_list = []
        if "今日毛鸭" in table_title:
            table_data_3_list.append(u'区域')
        table_data_4_list = []
        table_district_nums_list = []
        table_district_names_list = []
        tables_content_body_x = response.xpath('//div[@id="js_content"]/table[{0}]'.format(table_div_num))
        for table_content in tables_content_body_x:
            tables_detail_tr = table_content.xpath('./tbody/tr')
            for table_tr_x in tables_detail_tr:
                if len(table_tr_x.xpath('./td[not(@rowspan)]')) <= 3:
                    table_span_text = table_tr_x.xpath('./td[not(@rowspan)]/span/text()').extract()
                    for table_data_3 in table_span_text:
                        print 'table_data_3:' + table_data_3
                        table_data_3_list.append(table_data_3.encode("utf8"))
                elif len(table_tr_x.xpath('./td[not(@rowspan)]')) >= 4:
                    table_span_text = table_tr_x.xpath('./td[not(@rowspan)]/span/text()').extract() if table_tr_x.xpath('./td[not(@rowspan)]/span/text()').extract() else "空"
                    for table_data_4 in table_span_text:
                        print 'table_data_4:' + table_data_4
                        table_data_4_list.append(table_data_4.encode("utf8"))
            table_district_nums = table_content.xpath('./tbody/tr/td/@rowspan').extract()
            table_district_names = table_content.xpath('./tbody/tr/td[@rowspan]/span/text()').extract()
            if "今日毛鸭" in table_title and '2' in table_district_nums:
                table_district_names.insert(table_district_nums.index('2') + 1, u'空')
            m = 0
            for table_disctrict_num in table_district_nums:
                print 'table_district_nums:' + table_district_nums[m]
                table_district_nums_list.append(table_district_nums[m].encode("utf8"))
                if table_district_names[m] == "    （棚前）" or table_district_names[m] == "    （棚后）" or table_district_names[m] == "    ":
                    table_district_names.pop(m)
                district_name = table_district_names[m] if table_district_names[m].strip() else u'空白'
                print 'table_district_names:' + district_name
                table_district_names_list.append(district_name.encode("utf8"))
                m += 1
        self.create_csv(table_data_3_list,table_data_4_list,table_district_nums_list,table_district_names_list,table_title,article_time,article_title,article_catagory)


    def create_csv(self,table_data_3_list,table_data_4_list,table_district_nums_list,table_district_names_list,table_title,article_time,article_title,article_catagory):
        format_export = ['表名','分类',table_data_3_list[0], table_data_3_list[1], table_data_3_list[2],'日期']
        self.ExportData(format_export,article_title,article_catagory)
        m=3
        k=0
        if "今日山东麻鸡"  in table_title or "明日鸭苗" in table_title :
            table_district_nums_list=[]
            table_district_nums_list.append(int(len(table_data_3_list)/3)-1)
            table_district_names_list=[]
            table_district_names_list.append(u'无')
        for table_district_num in table_district_nums_list:
            for i in xrange(int(table_district_num)):
                table_data_0 = table_title
                table_data_1 = table_district_names_list[k]
                table_data_2 = table_data_3_list[m]
                table_data_3 = table_data_3_list[m+1]
                table_data_4 = table_data_3_list[m+2]
                table_data_5 = article_time
                m+=3
                format_export = [table_data_0,table_data_1,table_data_2,table_data_3,table_data_4,table_data_5]
                self.ExportData(format_export,article_title,article_catagory)
            k+=1
        if len(table_data_4_list) != 0:
            if "今日毛鸭" in table_title:
                table_data_4_list.insert(0,table_data_4_list[0])
            for i in xrange(0,len(table_data_4_list),4):
                table_data_0 = table_title
                table_data_1 = table_data_4_list[i]
                table_data_2 = table_data_4_list[i+1]
                table_data_3 = table_data_4_list[i+2]
                table_data_4 = table_data_4_list[i+3]
                table_data_5 = article_time
                format_export = [table_data_0, table_data_1, table_data_2, table_data_3, table_data_4, table_data_5]
                self.ExportData(format_export, article_title,article_catagory)

        #微评
        # self.ExportData([table_data_3_list[-1]],article_title,article_catagory)

    def ExportData(self,format_export,article_title,article_catagory):
        with open(os.path.join(BASE_DIR, u'近10天数据_{0}.csv'.format(cdate)), 'ab+') as csvfile:
            csvfile.write(codecs.BOM_UTF8)
            spamwriter = csv.writer(csvfile, dialect='excel')
            spamwriter.writerow(format_export)

    def get_text(self,texts):
        text = ""
        if len(texts) > 0:
            for tmp in texts:
                text = text + tmp
        return text.strip()

    def request_phantomjs(self,url):
        '''动态链接请求'''
        print "request url:"+url
        driver = webdriver.PhantomJS(
            executable_path=r'D:\ceshi\phantomjs-2.1.1-windows\bin\phantomjs.exe')  # 指定使用的浏览器，写在此处而不写在类中，是为了不每次调用都生成一个信息独享，减少内存使用
        driver.get(url)
        time.sleep(1)
        js = "var q=document.documentElement.scrollTop=10000"
        driver.execute_script(js)  # 可执行js，模仿用户操作。此处为将页面拉至最底端。
        time.sleep(3)
        body = driver.page_source
        return HtmlResponse(driver.current_url, body=body, encoding='utf-8')


    def request_static(self,url):
        '''静态链接请求'''
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; windows NT)'
        headers = {'User-Agent': user_agent}
        r = requests.post(url, headers=headers)
        time.sleep(1)
        body = r.content
        time.sleep(3)
        return HtmlResponse(url=url, body=body, encoding='utf-8')

