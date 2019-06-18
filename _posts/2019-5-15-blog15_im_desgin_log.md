---
layout: post
title:  "im系统设计 日志系统设计"
date:   2019-05-15 08:59:48 +0800
categories: jekyll update
---


# im系统设计 日志系统设计

### 1. 概述

日志系统设计,每个框架都应该设计合理的日志系统,供开发或者运维人员使用


本日志系统设计的要求如下:
	
	
1. 可以有不同级别的日志, 如debug, info, error等不同的等级

2. 可配置,在配置文件中配置日志的等级,比如配置error等级,那么debug,info等日志的输出信息就不能显示出来

3. 支持不同的引擎抽象,可以配置日志输出到终端,也可以配置日志输出到日志文件,输出到redis,并且在配置文件中可配置(插件形式)


### 2. 日志系统设计思路

1. 由于是多日志系统(插件形式),所以必须规范日志系统的函数,所有的日志系统都满足同一个规范.现有的设计规范是日志系统必须有debug,info,warn,error四个级别,所有的日志也必须满足这四个级别的设计。跟着这个思路走,那应该设计一个抽象基类,去控制子类必须实现几个功能

	>baselogger.py
	
	```
	from abc import ABCMeta,abstractmethod
	
	
	class BaseLogger(metaclass=ABCMeta):
	
	    def __init__(self,level,fmt):
	        self.fmt = fmt
	        self.level = level
	    @abstractmethod
	    def info(self,sender,msg):
	        pass
	    @abstractmethod
	    def debug(self,sender,msg):
	        pass
	
	    @abstractmethod
	    def warn(self,sender,msg):
	        pass
	
	    @abstractmethod
	    def error(self,sender,msg):
	        pass
	
	```
	
2. 在定义了抽象基类的之后,就可以去实现日志类了,首先实现一个基于文件的类,日志输出到文件,如果没有执行文件,则输出到终端

	>1. 首先让FileHandler去继承 BaseLogger 实现具体的error,info等方法
	
	>2. 实现一个log_out,对比当前系统日志的级别,如果大于等于系统设置的日志级别,就输出日志
	

	```
	
	from my_loggers.baselogger import BaseLogger
	from settings import BASE_DIR
	import sys
	import os
	
	sys.path.append(os.path.dirname(BASE_DIR))
	from my_loggers.configs import LOG_LEVEL
	import sys
	import datetime
	
	
	class FileHandler(BaseLogger):
	    def __init__(self, level, fmt=None, file=None):
	        super().__init__(level, fmt)
	        self.file = file
	        if not self.file:
	            self._file = sys.stdout
	        else:
	            self._file = open(file, 'w')
	        if not self.fmt:
	            self.fmt = "%Y-%m-%d %H:%M:%S"

    def __log_out(self, level, sender, massage):
        # 到达相应的日志基本才会输出
        if LOG_LEVEL[self.level] <= LOG_LEVEL[level]:
            log_msg = "发生时间:{}日志级别:{}产生日志文件:{}:消息:{}\n".format(datetime.datetime.now().strftime(self.fmt), level,
                                                               sender, massage)
            self._file.write(log_msg)
            """
            关闭handler
            """

    def __del__(self):
        self._file.close()

    def info(self, sender, msg):
        self.__log_out("info", sender, msg)

    def debug(self, sender, msg):
        self.__log_out("debug", sender, msg)

    def warn(self, sender, msg):
        self.__log_out("warn", sender, msg)

    def error(self, sender, msg):
        self.__log_out("error", sender, msg)

	
	if __name__ == "__main__":
	    logger = FileHandler("error")
	    logger.warn('aaa', '错误')
	    logger.info('aaa', '错误')
	    logger.error('aaa', '错误')
	    logger.debug('aaa', '错误')

	
	```
	
3. 设计日志的级别,给debug info每个一个值,使用二进制位移来做

	```
	LOG_LEVEL = {
	    "debug": 1 << 0,
	    "info": 1 << 1,
	    "warn": 1 << 2,
	    "error": 1 << 3,
	    "fatal": 1 << 4
	}
	
	```
	
4. 设计自动加载配置文件,从配置文件中读取, my_loggers.file.FileHandler 类似于django的设计,  my_loggers.file代表文件夹和文件,FileHandler代表类,也就是上面的file类,再通过 importlib.import_module 去引入模块,这样我们就能加载模块。也能从配置文件去修改类的路径来修改引入的模块

	```
	from settings import LOGGER, BASE_DIR
	import sys
	import importlib
	
	sys.path.append(BASE_DIR)
	_module_path = LOGGER["BACKEND"]
	_module_path, _cls = _module_path.rsplit(".", 1)
	log_module = importlib.import_module(_module_path)
	_logger_cls = getattr(log_module, _cls)
	
	logger = _logger_cls(LOGGER["LEVEL"], LOGGER["FORMAT"], **LOGGER['OPTIONS'])
	
	info = logger.info
	debug = logger.debug
	warn = logger.warn
	error = logger.error
	```
