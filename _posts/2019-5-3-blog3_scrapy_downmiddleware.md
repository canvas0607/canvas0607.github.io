---
layout: post
title:  "scrapy 下载中间的使用"
date:   2019-05-3 08:59:48 +0800
categories: jekyll update
---


# scrapy 下载中间的使用

接<a href="blog1_scrapy_cookiejar.md">第一篇文章</a>的登录保持,我们会发现如下问题:

1. cookie和headers都必须写在spider中,每次都在request的属性中,代码很麻烦

2. 只有单用户,那么其实被封杀的可能性很大,怎么样去不断的切换ip和用户,防止单ip被封杀也是一个问题

解决方案: 接<a href="blog2_scrapy_struct.md">第二篇文章</a>我们发现,其实scrapy在去请求每个网页之前,都会走到downloadmiddeware去,那么我们可以在downloadmiddleware中去添加header cookie等内容,以此来代替在spider中写入这些内容

## downloadmiddleware的激活与注意事项

1. 需要在settings.py中去设置开启响应的下载中间件

	```
	DOWNLOADER_MIDDLEWARES = {
		   'zhilian.middlewares.ZhilianDownloaderMiddleware': 543,
		}
	
	```
	
2. 数字中 543是中间件的处理顺序,因为有多个中间件的存在,所以需要设置他们启动的顺序,顺序会在下面讲到

## downloadmiddleware的结构与启动顺序

1. from_crawler 只在爬虫启动的时候启动一次(是一个spider.py启动的时候只会启动一次),里面包含一些初始化的内容

	```
	    @classmethod
	    def from_crawler(cls, crawler):
	        # This method is used by Scrapy to create your spiders.
	        s = cls()
	        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
	        return s
	
	```
	
2. process_request 在下载器启动之前要启动的函数

	1. 启动顺序,按照settings中的数值大小,升序启动
	2. 可以在这里加上比如cookie,header之类的值,或者是切换ip的函数,使爬虫不断的变化ip
	3. 他返回四个参数

		1. response对象

			1. 如果返回response对象,会直接去按照顺序依次执行process_response

		2. request对象
			1. 会停止当前函数,重新调用所有的process_requset


		3. None

			1. 会安装顺序继续向下去执行

		4. IgnoreRequest错误对象

			1. 启动process_exception


3. process_response 在下载器完成下载之后要启动的函数

	1. 启动顺序,按照settings里面的顺序,降序启动
	2. 他要求返回三个参数

		1. Response对象 会继续按照顺序交给其他process_response处理掉

		2. request对象 停止调用process_response方法,带上这个request	启动download下载器

		3. IgnoreRequest 启动process_exception

		
## 在中间件中去添加cookie

在中间件中去添加cookie这样就不用每次都要去在spider中添加,所有的spider都会带上cookiee值


	```
	
	def process_request(self, request, spider):
        from utils.cookies_get import make_cookie
        cookie = make_cookie()
        request.cookies.update(cookie)
        return None
	
	```
	
1. cookie应该是在请求之前就要封装好,所以应该是使用process_request

2. 在request对象中把cookie的值更新

3. 返回None,让调度器去执行其他process_reqeust，如果完成则会启动下载器
	

