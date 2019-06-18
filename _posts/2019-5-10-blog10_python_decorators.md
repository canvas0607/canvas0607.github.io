---
layout: post
title:  "python 装饰器"
date:   2019-05-10 08:59:48 +0800
categories: jekyll update
---


# python 装饰器

#### 1. 装饰器基础

1. 装饰器原理-> 装饰器其实就是一个函数,所谓装饰就可以对原函数进行加工而已。当然是通过一些小技巧,python里面的装饰器用到了函数是一等对象的原理,也就是说函数可以作为变量传递到另一个函数的参数中

	```
	
	def target():
        print("running target()")
	def deco(func):
	    def inner(func):
	        func()
	        print("running inner")
	    return inner
	
	target = deco(target)
	```
	
	>这个例子就是装饰器的最原始使用方式,定义了deco函数,函数接受变量(函数),然后可以做装饰的功能,最后返回给target 这样就定义完成了
	
2. python 语法糖

	```
	@deco
	def target():
    	print("running target()")
	```
	
	>python 通过加上@号,实现上面繁琐的装饰器定义方式,其实两个都一样
	
#### 2. 装饰器的启动方式

1. python会先启动装饰器,在下面这个例子中,我们没有去启动函数,但是装饰器依然运行了。而且在import的时候,装饰器也会先运行


	> 运行如下代码
		
		```
		
		registry = []
		
		def register(func):
		    print("running register(%s)" % func)
		    registry.append(func)
		    return func
		
		
		@register
		def f2():
		    print("running f2()")
		
		@register
		def f1():
		    print("running f1()")
		
		def f3():
		    print("running f3()")
		def main():
		    f3()
		if __name__ == "__main__":
		    main()
		```
		
	>运行结果
	
	```
	running register(<function f2 at 0x10a4fbc80>)
	running register(<function f1 at 0x10a4fbd90>)
	running f3()
	
	```
	
	>列1.1不会出结果,因为函数被包裹在装饰器的inner函数中了,这个例子是直接调用函数
	

#### 3. python的作用域
