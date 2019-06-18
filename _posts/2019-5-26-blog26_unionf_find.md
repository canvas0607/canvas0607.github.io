---
layout: post
title:  "并查集"
date:   2019-05-26 08:59:48 +0800
categories: jekyll update
---

# 并查集

#### 并查集概念

1. 软件中有一种连通性的问题。判断两个点是否是联通的。如何理解这个问题就用到了并查集。并查集其实是两个单词的缩写。 union 合并的意思。find 查询的意思。我们初始化出来n个元素 [1,2,3,4,5,6,7,8,9]。他们互补相连。但是可以使用并查集中的函数,把 1，2相连接 把 2，9 相连接。那么如果需要判断 1 9 直接是否连接。其实通过这个函数就能判断出来。

2. 并查集如何去实现元素之间相连接合并呢?在最开始的时候,可以给每个节点一个父级元素。表示元素归属于哪一类。开始时每个元素都归属于自己，然后在每次的合并时候，其实就是将某个元素合并到某个另一个元素所属的类中

3. 在经过第二步之后,判断元素之间是否连通就很简单了，只需要去查找他们两个是否都属于同一个父类即可


#### 并查集具体的技术实现

1. 查找两个元素是否属于同一类: 这个很简单,只需要判断两个的父类是否相等即可

2. 合并两个元素的时候,把他们的父节点指向同一个父节点算法:

	1. 直接去关联父节点,如下图所示:

		> 1. 1,2  2,9合并  3，4  5,3 8,5合并
		> 2. 3 9 合并
		
		```
		
		1 2 3 4 5 6 7 8 9 
		
		————————————————————
		
		1  4  6 7 
		
		2  3
		
		9  5 
		   
		   8 
		——————————————————
		
		1
		  \
		2   4
		      \
		9      3
		        \
		         5
		          \
		           8
		```
		
	2. 判断哪个树高,用矮的树去合并高的树,降低维度

		```
		1 2 3 4 5 6 7 8 9 
		
		————————————————————
		
		1  4  6 7 
		
		2  3
		
		9  5 
		   
		   8 
		——————————————————
		
		
		  
		     4
		    /  \
		   1    3
		  /      \
		 2        5
		/           \
	   9	         8
		```
		
	3. 在查找节点的时候,把节点的父节点向上移动到父节点的父节点

		
		
	4. 查找节点的时候,把所有节点都移动到根节点下面去

		```
			1 2 3 4 5 6 7 8 9 
			
			————————————————————
			
			1      4  6 7 
	      /\ 	   /|\
		  2  9   3 5 8
			 
			——————————————————
			
			
			  
			        4
			    /  |  | |  \
			   1 9 2 5  3  8
			   
		 ```

		

	

3. 可以看到,并查集不同于其他的树结构,因为他的算法关心的都是父节点。而一般的树结构关心的是子节点。


#### 代码

1. 代码有四个版本,关于降低维度的

	```
	
	
	class UnionFind:
	    def __init__(self,size):
	        self.size = size
	        self.elements = []
	        self.sz = []
	        self.gen()
	
	    def gen(self):
	        for i in range(self.size):
	            self.elements.append(i)
	            self.sz.append(1)
	
	    def find_parent(self,i):
	        """
	        find node parent
	        :param i:
	        :return:
	        """
	        while i != self.elements[i]:
	            i = self.elements[i]
	        return i
	
	    def union_elements(self,q,p):
	        q_parent = self.find_parent(q)
	        p_parent = self.find_parent(p)
	        if q_parent == p_parent:
	            return True
	        else:
	            self.elements[q_parent] = p_parent
	            self.sz[p_parent] += self.sz[q_parent]
	            return True
	
	    def union_elementsv2(self,q,p):
	        q_parent = self.find_parent(q)
	        p_parent = self.find_parent(p)
	        if q_parent == p_parent:
	            return True
	        else:
	            """
	            这个版本先比较树的深度再去合并，注意合并的方向
	            被合并了之后,元素增加,那么增加他相应的sz
	            """
	            if self.sz[q_parent] < self.sz[p_parent]:
	                self.elements[q_parent] = p_parent
	                self.sz[p_parent] += self.sz[q_parent]
	            else:
	                self.elements[p_parent] = q_parent
	                self.sz[q_parent] += self.sz[p_parent]
	            return True
	
	    def is_conn(self,q,p):
	        q_parent = self.find_parent(q)
	        p_parent = self.find_parent(p)
	        return q_parent == p_parent
	        
	```
	
2. 关于降维度的代码,v0，每次遍历的时候把父节点的位置提高, 或者是每次把节点移动到根节点的下面 使用这种压缩后,时间复杂度为 log*n 相当于 O(1)


	```
	
	
	class UnionFind:
    def __init__(self,size):
        self.size = size
        self.elements = []
        self.rank = []
        self.gen()

    def gen(self):
        for i in range(self.size):
            self.elements.append(i)
            self.rank.append(1)


	 def find_parentv0(self,i):
        """
        find node parent
        :param i:
        :return:
        """
        while i != self.elements[i]:
            self.elements[i] = self.elements[self.elements[i]]
            i = self.elements[i]
        return i
        
    def find_parent(self,i):
        """
        find node parent 添加路径压缩,把父节点压缩到父节点的根点上面
        递归宏观语义,该函数能找到节点的根节点，如果不是根节点 就继续寻找,在寻找的的时候,顺便把
        父节点变为根节点,最后返回
        :param i:
        :return:
        """
        if i != self.elements[i]:
            self.elements[i] = self.find_parent(self.elements[i])
        return self.elements[i]

    def union_elements(self,q,p):
        q_parent = self.find_parent(q)
        p_parent = self.find_parent(p)
        if q_parent == p_parent:
            return True
        else:
            self.elements[q_parent] = p_parent
            return True

    def union_elementsv2(self,q,p):
        q_parent = self.find_parent(q)
        p_parent = self.find_parent(p)
        if q_parent == p_parent:
            return True
        else:
            """
            这个版本先比较树的深度再去合并，注意合并的方向
            被合并了之后,元素增加,那么增加他相应的sz
            """
            if self.rank[q_parent] < self.rank[p_parent]:
                self.elements[q_parent] = p_parent
            elif self.rank[q_parent] > self.rank[p_parent]:
                self.elements[p_parent] = q_parent
            else:
                self.elements[q_parent] = p_parent
                self.rank[p_parent] += 1
            return True

    def is_conn(self,q,p):
        q_parent = self.find_parent(q)
        p_parent = self.find_parent(p)
        return q_parent == p_parent
	
	
	```
