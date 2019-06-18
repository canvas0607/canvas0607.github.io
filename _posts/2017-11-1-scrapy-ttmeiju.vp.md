{{ page.title }}

1.目标:使用scrapy爬取天天美剧网站的美剧资源链接和相关介绍

2.下载安装scrapy(这里使用virutalenv 和python3.6)

```shell
$mkvirtualenv my_scrapy -p python3.6
$workon my_scrapy
$pip install scrapy
```

3.创建scrapy项目 创建一个ttmeiju.vip的爬虫


```shell
$scrapy startproject my_scrapy
$scrapy genspider ttmeiju www.ttmeiju.vip
```
4.这个时候项目下会生成一个spiders目录,目录下面有个
ttmeiju.py文件,这个就是ttmeiju爬虫的主要逻辑的地方

代码

```python
# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
import re
from scrapy.loader import ItemLoader
from my_crwaler.items import TtmeijuItem
import my_crwaler.utils.common as utils


class TtmeijuSpider(scrapy.Spider):
    name = 'ttmeiju'
    allowed_domains = ['www.ttmeiju.vip']
    start_urls = ['http://www.ttmeiju.vip/index.php/user/login.html']
    login_user = ''
    login_pwd = ''

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
        'Accept-Language': "zh-CN,zh;q=0.8,en;q=0.6",
        "Host": "www.ttmeiju.vip"
    }

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], headers=self.headers, callback=self.is_login)

    def is_login(self, response):
        login_flag = response.css('#loginform')
        if login_flag is not None:
            # 登录
            params = {
                'username': self.login_user,
                'password': self.login_pwd
            }
            return [scrapy.FormRequest(
                url=self.start_urls[0],
                formdata=params,
                headers=self.headers,
                callback=self.check_login
            )]

    def check_login(self, response):
        # 成功之后请求列表页
        url = 'http://www.ttmeiju.vip/summary.html'
        yield scrapy.Request(url=url, dont_filter=True, headers=self.headers)

    def parse(self, response):
        # 解析分页 .pagination .num
        detail_urls = response.css('.latesttable a::attr(href)').extract()
        detail_pattern = "^/meiju/[^(Movie.html)]"
        for detail_url in detail_urls:
            if re.match(detail_pattern, detail_url, flags=0):
                real_detail_url = parse.urljoin(response.url, detail_url)
                yield scrapy.Request(real_detail_url, headers=self.headers, callback=self.detail_parse)

        page_urls = response.css('.pagination .num::attr(href)').extract()
        for page_url in page_urls:
            real_url = parse.urljoin(response.url, page_url)
            yield scrapy.Request(real_url, headers=self.headers)

    def detail_parse(self, response):
        # 详细链接列表
        seed_lists = response.css('#seedlist tr')
        for seed_list in seed_lists:
            tmp_urls = {"baidu": "null", "bt": "null", "xunlei": "null", "xiaomi": "null", "ed2": "null"}
            title = seed_list.css("td a").extract_first()

            dr = re.compile(r'<[^>]+>', re.S)
            dd = dr.sub('', title)
            dd = dd.replace('\t', "").replace('\n', "")
            # 数据库主键
            object_id = utils.get_md5(dd)
            # x = dd
            title_list = dd.split(" ")
            # 获取中文标题
            chinese_title = title_list[0]
            eposode_info = ""
            for info in title_list:
                if re.match("S\d+E\d+", info):
                    eposode_info = info
            eposode_position = title_list.index(eposode_info)
            # 获取集的信息
            english_split = title_list[1:eposode_position]
            # 由于英文有空格 切片链接
            english_title = " ".join(english_split)
            eposode_list = re.search(r"S(\d+)E(\d+)", eposode_info)
            season = eposode_list.group(1)
            episode = eposode_list.group(2)
            seed_list_urls = seed_list.css('td ::attr(href)').extract()
            for seed_list_url in seed_list_urls:
                if re.match("^https://pan.baidu.com*", seed_list_url, flags=0):
                    tmp_urls['baidu'] = seed_list_url
                if re.match("^https://rarbg.is/download.php*", seed_list_url, flags=0):
                    tmp_urls['bt'] = seed_list_url
                if re.match("^magnet:\?xt=urn:btih*", seed_list_url, flags=0):
                    tmp_urls['xunlei'] = seed_list_url
                if re.match("^https:d.miwifi.com*", seed_list_url, flags=0):
                    tmp_urls['xiaomi'] = seed_list_url
                if re.match("^ed2k://*", seed_list_url, flags=0):
                    tmp_urls['ed2'] = seed_list_url

            decribes = seed_list.css('td::text').extract()
            subtitles = seed_list.css('td font::text').extract()
            subtitle = '无字幕'
            for subtitle in subtitles:
                if "内嵌双语字幕" in subtitle:
                    subtitle = "内嵌双语字幕"
            additional_descs = {'subtitle': subtitle, "size": "null", "kind": "null", "release_time": "null"}
            for decribe in decribes:
                # 匹配大小
                if re.match("(^\d+M$)|(^\d+(\.\d+)G$)", decribe, flags=0):
                    additional_descs['size'] = decribe
                # 匹配类型
                if re.match("普清|熟肉|(^\d+p$)", decribe, flags=0):
                    additional_descs['kind'] = decribe
                if re.match("\d{4}-\d{2}-\d+", decribe, flags=0):
                    additional_descs['release_time'] = decribe
            item_loader = ItemLoader(item=TtmeijuItem(), response=response)
            item_loader.add_value("describes", additional_descs)
            item_loader.add_value("urls", tmp_urls)
            item_loader.add_value("title", dd)
            item_loader.add_value("baiduUrl", tmp_urls.get('baidu'))
            item_loader.add_value("xunleiUrl", tmp_urls.get('xunlei'))
            item_loader.add_value("xiaomiUrl", tmp_urls.get('xiaomi'))
            item_loader.add_value("ed2Url", tmp_urls.get('ed2'))
            item_loader.add_value("btUrl", tmp_urls.get('bt'))
            item_loader.add_value("kind", additional_descs.get('kind'))
            item_loader.add_value("size", additional_descs.get('size'))
            item_loader.add_value("release_time", additional_descs.get('release_time'))
            item_loader.add_value("subtitle", additional_descs.get('subtitle'))
            item_loader.add_value("chinese_title", chinese_title)
            item_loader.add_value("english_title", english_title)
            item_loader.add_value("season", season)
            item_loader.add_value("episode", episode)
            item_loader.add_value("object_id", object_id)
            yield item_loader.load_item()


```

5.
name 表示这个爬虫的名字 启动爬虫需要使用这个name，

allowed_domains 爬虫爬取数据的域,如果想爬取其他站点,可以把域名加上，

start_urls 第一个爬取的页面

```python
name = 'ttmeiju'
allowed_domains = ['www.ttmeiju.vip']
start_urls = ['http://www.ttmeiju.vip/index.php/user/login.html']
```

6.在爬取第一个页面的后，scrapy会默认交给parse函数处理,这里由于需要登录才能看到相关连接信息,所以先使用账户密码登录


首先把浏览器主要的几个headers写入到请求头中,以免简单的反爬虫,头信息可以在浏览器的network中找到,然后填入账户密码 使用scrapy自动的表单提交,提交本次登录信息,设置登录后回调函数 check_login判断是否登录
```python
def start_requests(self):
    yield scrapy.Request(url=self.start_urls[0], headers=self.headers, callback=self.is_login)

def is_login(self, response):
    login_flag = response.css('#loginform')
    if login_flag is not None:
        # 登录
        params = {
            'username': self.login_user,
            'password': self.login_pwd
        }
        return [scrapy.FormRequest(
            url=self.start_urls[0],
            formdata=params,
            headers=self.headers,
            callback=self.check_login
        )]
```

7.登录后,scrapy会自动存储cookies,以后所有请求都会带上.
然后请求天天美剧的排行页面,上面有所以的美剧,把请求的结果回调给默认的parse函数处理
```python
def check_login(self, response):
    # 成功之后请求列表页
    url = 'http://www.ttmeiju.vip/summary.html'
    yield scrapy.Request(url=url, dont_filter=True, headers=self.headers)

```

8.请求完毕后,可以看到网页是一个存有每个单独美剧的详细信息的连接列表,
网页下面可以翻页

首先解析出列表页下一页的url,再使用urljoin拼接url 因为有时候url不是完整url,parse.url可以帮助我们自动拼接url,
打开网页可以看到,1-10的页码条在一个class为pagination的table里面，
里面带有其他列表页的跳转信息,使用css选择器把所有带href的链接取出来,
这里是一个list 循环list取出每个href 拼接后再交给本parse函数继续解析


然后是解析详情页面的url,同上 详情页面存储在latesttable 的class中
取出里面的所有href,详情页的url都是以/meiju/开头的url,用正则表达式匹配这些合法的url，然后把这些url交给detail_parse函数处理

```python
def parse(self, response):
    # 解析分页 .pagination .num
    detail_urls = response.css('.latesttable a::attr(href)').extract()
    detail_pattern = "^/meiju/[^(Movie.html)]"
    for detail_url in detail_urls:
        if re.match(detail_pattern, detail_url, flags=0):
            real_detail_url = parse.urljoin(response.url, detail_url)
            yield scrapy.Request(real_detail_url, headers=self.headers, callback=self.detail_parse)

    page_urls = response.css('.pagination .num::attr(href)').extract()
    for page_url in page_urls:
        real_url = parse.urljoin(response.url, page_url)
        yield scrapy.Request(real_url, headers=self.headers)

```

9.parse_detail


10.将selenium嵌入到scrapy中


