---
layout: post
title:  "mongodb CURD"
date:   2019-05-7 08:59:48 +0800
categories: jekyll update
---




# mongodb CURD

#### insert

1. 插入语句

mongodb的数据是创建在collection（集合）中的,如果不指定的插入一条_id字段,那么mongodb会自动的插入一条_id字段并且生成一个自动的值

2. 插入一条数据
		
	```
	db.inventory.insertOne(
	   { item: "canvas", qty: 100, tags: ["cotton"], size: { h: 28, w: 35.5, uom: "cm" } }
	)
	```

3. 插入多条数据

	```
	db.inventory.insertMany([
	   { item: "journal", qty: 25, tags: ["blank", "red"], size: { h: 14, w: 21, uom: "cm" } },
	   { item: "mat", qty: 85, tags: ["gray"], size: { h: 27.9, w: 35.5, uom: "cm" } },
	   { item: "mousepad", qty: 25, tags: ["gel", "blue"], size: { h: 19, w: 22.85, uom: "cm" } }
	])
	
	```

4. 插入一条或者多条数据

	```
	db.collection.insert(
	   <document or array of documents>,
	   {
	     writeConcern: <document>,
	     ordered: <boolean>
	   }
	)
	```
	
5. 复合插入数据

	```
	for(i=0;i<100;i++) db.test5.insert({x:i,y:i*i})
	```
	


#### 查询语句

首先插入下面语句

```
db.inventory.insertMany([
   { item: "journal", qty: 25, size: { h: 14, w: 21, uom: "cm" }, status: "A" },
   { item: "notebook", qty: 50, size: { h: 8.5, w: 11, uom: "in" }, status: "A" },
   { item: "paper", qty: 100, size: { h: 8.5, w: 11, uom: "in" }, status: "D" },
   { item: "planner", qty: 75, size: { h: 22.85, w: 30, uom: "cm" }, status: "D" },
   { item: "postcard", qty: 45, size: { h: 10, w: 15.25, uom: "cm" }, status: "A" }
]);
```

1. 查找所有文档

	```
	db.inventory.find( {} )
	```

2. 筛选文档

	```
	
	db.inventory.find( { status: "D" } )
	```

3. 模拟mysql in语句 

	```
	db.inventory.find({'status':{$in:["A","D"]}})
	```

4. 模拟sql > 语句
	
	```
	db.inventory.find( { status: "A", qty: { $lt: 30 } } )
	```
5. 模拟or查询语句

	```
	db.inventory.find({$or:[{status:"A"},{qty:{$lt:20}}]})
	```
	
6. and和or语句联用

	```
	db.inventory.find( {
     status: "A",
     $or: [ { qty: { $lt: 30 } }, { item: /^p/ } ]
} )
	```
	
7. 统计查询个数

	```
	db.inventory.find().count()
	```
	
8. 查询后排序

	> 1表示正序 -1表示倒序
	> 下面语句表示按qty的正序排列
	
	```
	db.inventory.find().sort({"qty":1})
	```
	
9. 查询个数限时(类似于mysql的limit)

	>使用skip跳过几条数据 使用limit限制查询的条数 使用sort来对某个字段排序
	
	```
	db.test1.find().skip(1).limit(2).sort({x:1})
	```

	
	
#### 更新语句

1. 首先插入数据

	```
	
	db.inventory.insertMany( [
	   { item: "canvas", qty: 100, size: { h: 28, w: 35.5, uom: "cm" }, status: "A" },
	   { item: "journal", qty: 25, size: { h: 14, w: 21, uom: "cm" }, status: "A" },
	   { item: "mat", qty: 85, size: { h: 27.9, w: 35.5, uom: "cm" }, status: "A" },
	   { item: "mousepad", qty: 25, size: { h: 19, w: 22.85, uom: "cm" }, status: "P" },
	   { item: "notebook", qty: 50, size: { h: 8.5, w: 11, uom: "in" }, status: "P" },
	   { item: "paper", qty: 100, size: { h: 8.5, w: 11, uom: "in" }, status: "D" },
	   { item: "planner", qty: 75, size: { h: 22.85, w: 30, uom: "cm" }, status: "D" },
	   { item: "postcard", qty: 45, size: { h: 10, w: 15.25, uom: "cm" }, status: "A" },
	   { item: "sketchbook", qty: 80, size: { h: 14, w: 21, uom: "cm" }, status: "A" },
	   { item: "sketch pad", qty: 95, size: { h: 22.85, w: 30.5, uom: "cm" }, status: "A" }
	] );
	
	```
	
2. 更新数据

	1. 普通的更新<b>一条</b>数据

		>使用$set 来更新 size中的uom字段 和 status字段
		
		>使用$currentDate来更新 lastModified:True 的时间字段
	
		```
		db.inventory.updateOne({item:"paper"},{$set:{"size.uom":"cm",status:"p"},$currentDate:{lastModified:true}})
		```
		
	2. 更新多条数据
		
		```
		db.inventory.updateMany(
   { "qty": { $lt: 50 } },
   {
     $set: { "size.uom": "in", status: "P" },
     $currentDate: { lastModified: true }
   }
)
		```
		
	3. 直接把数据替换而不更新

		```
		db.inventory.replaceOne(
   { item: "paper" },
   { item: "paper", instock: [ { warehouse: "A", qty: 60 }, { warehouse: "B", qty: 40 } ] }
)
		```
		
	4. replaceOne的等价语句 update

		> 把匹配到的x全部给换成新的数据
		
		```
		
		db.test5.update({x:1},{z:3})
		```
		
	5. 更新或者插入(如果有数据就插入,没有数据就更新数据)

		```
		db.test5.update({x:0},{$set:{z:3}},true)
		```
		
	6. updateMany的替换语句

		>	批量更新操作必须用$set,第三个参数设为false,第四个参数设为true表示批量
		
		```
		
		db.test5.update({x:0},{$set:{z:3}},false,true)
		```
		
#### 删除数据

1. 删除一条数据（匹配到的）

	```
	db.inventory.deleteOne( { status: "D" } )
	```

2. 删除所有数据（匹配到的）

	```
	db.inventory.deleteMany( { status: "D" } )
	```
	
		
		
#### 其他语句

1. 查看所有数据库

	```
	show dbs
	```
	
2. 查看集合

	```
	show collections
	```
	或者
	
	```
	show talbes
	```
3. 切换所在数据库

	```
	use db
	```
	
4. 创建数据库

	>切换数据库 如果没有数据库就新建一个数据库
	
	```
	use db
	```
	
5. 删除数据库

	> 首先切换到数据库 然后执行删除命令
	
	```
	use test2
	db.dropDatabase()
	```
	
6. 删除集合

	```
	db.test5.drop()
	```

		

	
	
	
	

	
	
