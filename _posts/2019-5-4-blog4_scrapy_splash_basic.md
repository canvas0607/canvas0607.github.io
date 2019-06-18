---
layout: post
title:  "splash基础操作"
date:   2019-05-4 08:59:48 +0800
categories: jekyll update
---



# splash基础操作

## 1. splash 概述

1. 在进行爬虫操作的时候,我们一般是直接去下载网页然后爬去HTML里面的内容,但是现在的网站一般为了用户体验或者反扒等等,一般都采用了ajax动态获取页面,那么如果我们还去爬去这些内容,就只能得到js文件,而python代码是不能去加载js的。

2. 解决这个问题的方法就是去模拟浏览器的方式能执行js代码即可,方法有很多,比如selenium去控制chrome,或者本篇文章所讲的splash去加载js

3. splash是运行在docker中的程序,提供python的twisted接口调用(scrapy也是twisted的底层)

4. 其他功能

	1. 异步方式处理多个网页渲染过程；
	2. 获取渲染后的页面的源代码或截图；
	3. 通过关闭图片渲染或者使用Adblock规则来加快页面渲染速度；
	4. 可执行特定的JavaScript脚本
	5. 可通过Lua脚本来控制页面渲染过程；
	6. 获取渲染的详细过程并通过HAR(HTTP Archive)格式呈现。


## 2. splash的安装

1. 安装docker

2. 下载镜像 (可能需要使用国内镜像源加速)

	```
	docker pull registry.docker-cn.com/scrapinghub/splash
	```
	
3. 启动splash

	```
	docker run -p 8050:8050 scrapinghub/splash
	```
	
## 3. splash的使用

1. 进入splash调试api环境,使用浏览器访问http://localhost:8050/

2. 最主要的是script,他通过在script中书写 lua代码来让splash去模拟用户操作,同时也可以加载dom(运行js代码),获取js代码的返回值

3. render按钮就是点击之后,他会去执行刚才的js代码逻辑

4.  在执行完代码之后,左边会有一个执行完代码的截图,通过这个可以判断代码大致执行情况

5. 执行完成后,下面就会splash返回的值的显示

## 4. splash的lua中table的函数用法

1. 入口即返回值:

		```lua
		function main(splash, args)
		  assert(splash:go(args.url))
		  return {
			    html = splash:html(),
			    png = splash:png(),
			    har = splash:har(),
			  }
			end
		```
		
	表示执行完成后返回 html png har的内容,默认启动main函数

2. 异步处理

	```
	
	function main(splash, args)
	  local example_urls={"www.baidu.com","www.taobao.com","www.zhihu.com"}
	  local urls=args.urls or example_urls
	  local results={}
	  for index,url in ipairs(urls) do
	    local ok,reason=splash:go("http://" ..url)
	    if ok then         //异常检测
	      splash:wait(2)  //等待的秒数
	      results[url]=splash:png()
	     end
	  end
	  return results
	```
	
	Splash支持异步处理，但是这里并没有显式指明回调方法，其回调的跳转是在Splash内部完成的

3. go()

	该方法是用来请求某个链接的，而且它可以模拟GET和POST请求，同时支持传入请求头、表单等数据，用法如下:
	
	```
	ok,reason=splash:go{url,baseurl=nil,header=nil,http_method="GET",body=nil,formdata=nil}
	```

	1. url：请求的URL。
	2. baseurl:可选参数，默认为空，表示资源加载相对路径
	3. headers:可选参数，默认为空，表示请求头。
	4. http_method:可选参数，默认为GET，同时支持POST。
	5. body:可选参数，默认为空，发POST请求时的表单数据，使用的Content-type为application/json
	6. formdata:可选参数，默认为空，POST的时候的表单数据，使用的Content-type为application/x-www-form-urlencoded。
	该方法的返回结果是结果ok和原因reason的组合，如果ok为空，代表网页加载出现了错误，此时reason变量中包含了错误的原因，否则证明加载成功，如下所示:
	
	```
	function main(splash, args)
	  local ok,reason=splash:go{"http://httpbin.org/post",http_method="POST",body="name=Germey"}
	  if ok then
	    return splash:html()
	   end
	end
	```

4. wait()

	此方法可以控制页面的等待时间，使用方法如下:
	
	```
	ok,reason=splash:wait{time,cancel_on_redirect=false,cancel_on_error=true}
	
	```
	
	1. time:等待的秒数
	2. cancel_on_redirect:可选参数，默认为false，表示如果发生了重定向就停止等待，并返回重定向结果。
	3. cancel_on_error:可选参数，默认为false，表示如果发生了加载错误，就停止等待。

5. jsfunc()
	此方法可以直接调用JavaScript定义的方法，但是所调用的方法需要用中括号包围，这相当于实现了JavaScript方法到Lua脚本的转换，示例如下:
```
function main(splash, args)
  local get_div_count=splash:jsfunc([[
    function(){
    var body=document.body;
    var divs=body.getElementsByTagName('div');
    return divs.length;
  }
    ]])
  splash:go("https://www.baidu.com")
  return ("There are %s DIVs"):format(get_div_count())
end
```
6. runjs()

	此方法可以执行JavaScript代码，它与evaljs（）的功能类似，但是更偏向于执行某些功能或声明某些办法。如下所示:
	
	```
	function main(splash, args)
	  splash:go("https://www.baidu.com")
	  splash:runjs("foo=function(){return 'bar'}")
	  local result=splash:evaljs('foo()')
	  return result
	end
	```
	
	这里我们用runjs()先声明了一个JavaScript定义的方法，然后通过evaljs()来调用得到的结果。
	
	
## 其他方法参考

https://cuiqingcai.com/5638.html

## 本文转载文章:

https://blog.csdn.net/qq_41338249/article/details/81180133


