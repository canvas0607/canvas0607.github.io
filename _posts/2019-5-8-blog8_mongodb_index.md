---
layout: post
title:  "mongodb 索引"
date:   2019-05-8 08:59:48 +0800
categories: jekyll update
---

# mongodb 索引

#### 1. 什么是索引

1. mongodb使用类似于btree的数据结构来加速查询速度

2. mongodb默认的每条数据都有一个_id来作为索引结构

#### 2. 索引的创建

1. 对单个字段创建索引

	```
	db.records.createIndex( { score: 1 } )
	```
	
2. 对单个字段的嵌套结构中创建索引

	```
	db.records.createIndex( { "location.state": 1 } )
	```
	
3. 创建组合索引

	```
	db.events.createIndex( { "username" : 1, "date" : -1 } )
	```
	
	>组合索引要满足最左原则
	
	>测试最左原则
	
	>生成100条数据
	
	```
	for(i=0;i<100;i++) db.test6.insert({score:i,name:i})
	```
	
	>创建索引
	
	```
	db.test6.createIndex({score:1,name:1})
	```
	
	>分别对三条语句进行性能分析
	
	```
	db.test6.find({score:4}).explain('executionStats')
	db.test6.find({score:3,name:4}).explain('executionStats')
	db.test6.find({name:4}).explain('executionStats')
	```
	
	>可以看到 光是查找name的语句是不会有索引的,因为name不在左边 不符合最左原则

#### 3. 性能分析

> 查看Needtime

```
db.recored.find({score:{$gt:20}}).explain('executionStats')
```

不难发现 如果创建索引后 查询时间 needtime会显著降低

#### 4. 注意点

1. 索引之后查询是有方向的 分为 forward和backward

2. 在创建索引的时候,有一个字段为 score:1 表示为正序的索引,如果我们在查询的时候,使用了sort 之后,如果score是-1,那么会使用backward的方式去查询
