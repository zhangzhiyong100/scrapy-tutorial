
环境：python 2.7 64bit，win7 64bit
工具：scrapy、selenium、PhantomJS（需要自己下载）
学习scrapy时，写的入门代码

微信公众号文章爬取器--具体表格
实验公众号:家禽信息PIB
搜狗搜索链接:http://weixin.sogou.com/weixin?type=1&s_from=input&query=家禽信息PIB
搜狗搜索提供近10天的公众号文章，需要更久的历史文章则需要selenium模拟用户登录后
## <a name="Demo">Demo</a>
为了确保能正常运行示例脚本，请安装所需的第三方包。

```
pip install -r requirements.txt
```
## <a name="Demo">启动</a>


```
python begin.py
```


注：下面演示一下最终的结果。

<div align=center>
<img src="https://github.com/zhangzhiyong100/scrapy-tutorial/blob/master/imgs/0.PNG" width="500" height="550"/>
</div>


爬虫第一层请求，动态请求，页面js动态生成的
<div align=center>
<img src="https://github.com/zhangzhiyong100/scrapy-tutorial/blob/master/imgs/1.PNG" width="320" height="211"/>
</div>


爬虫第二层请求，动态请求，页面js动态生成的
<div align=center>
<img src="https://github.com/zhangzhiyong100/scrapy-tutorial/blob/master/imgs/2.PNG" width="320" height="211"/>
</div>


爬虫第三层请求
<div align=center>
<img src="https://github.com/zhangzhiyong100/scrapy-tutorial/blob/master/imgs/1.PNG" width="320" height="211"/>
</div>


通过xpath定位表格的每一个元素
