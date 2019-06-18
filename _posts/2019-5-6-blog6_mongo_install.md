---
layout: post
title:  "mongodb 安装与启动命令"
date:   2019-05-6 08:59:48 +0800
categories: jekyll update
---


# mongodb 安装与启动命令

#### 1. mongodb 安装步骤

1. mongodb 官网链接地址

	```
	https://www.mongodb.com/download-center/community
	```
2. 下载 解包安装

	```
	tar -zxvf xxx.gz
	```
	
#### 2. mongodb 服务端启动(进入到mongodb的解压目录)

1. 默认简单启动启动方式

	1. 启动
	
		```
		./bin/mongod
		```
	2. 对应连接方式

		```
		./bin/mongo
		```
	
2. 定制化启动方式

	1. 启动参数说明:
		

		
#### 3. 连接方式

	```
	mongo mongodb://mongodb0.example.com:28015
	```
	
	```
	mongo --host mongodb0.example.com:28015
	```
	
	```
	mongo --host mongodb0.example.com --port 28015
	```

