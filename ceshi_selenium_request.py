# -*- coding: utf-8 -*-
from selenium import webdriver
from scrapy.http import HtmlResponse
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class JavaScriptMiddleware(object):
    def process_request(self, url):
        # if spider.name == "quotes":
        print "PhantomJS is starting..."
        driver = webdriver.PhantomJS(executable_path=r'D:\ceshi\phantomjs-2.1.1-windows\bin\phantomjs.exe') #指定使用的浏览器
        # driver = webdriver.Firefox()
        driver.get(url)
        time.sleep(1)
        js = "var q=document.documentElement.scrollTop=10000"
        driver.execute_script(js) #可执行js，模仿用户操作。此处为将页面拉至最底端。
        time.sleep(3)
        body = driver.page_source
        with open('test1.html','wb') as fd:
            fd.write(body)
        print ("访问"+url)
        return HtmlResponse(driver.current_url, body=body, encoding='utf-8')
        # else:
        #     return

a=JavaScriptMiddleware()
# a.process_request('http://weixin.sogou.com/weixin?type=1&s_from=input&query=家禽信息PIB')
a.process_request('https://mp.weixin.qq.com/profile?src=3&timestamp=1515224013&ver=1&signature=6pRrV1-k4*ZUoKla6AmIZnBUqG6lFWzvxokjtRPxj8WXVNH9iJxzJexK8x8Muf*blvTO9b484JMRnZqZwX7*1A==')