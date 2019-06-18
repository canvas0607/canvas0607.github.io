---
layout: post
title:  "线段树"
date:   2019-05-25 08:59:48 +0800
categories: jekyll update
---

# 线段树

#### 1. 什么是线段(区间)树

1. 区间树最适合场景是做动态的数据统计,设想一个场景,统计一年之中消费总和,或者最大消费数量,或者最小消费数量。传统的思想是遍历每个数据,然后统计总和。但是这样会有性能的问题<b>这种的时间复杂度是O(n)</b>

2. 性能问题，接着上面的问题继续。如果我在统计的时候,不断有新的数据插入,那么我的统计数据也会不断的更新。这个时候就要考虑性能问题，每次我在新加数据的时候，整体的数据就会发生变化,那么这个时候时候统计的数据就不再有效,我们需要重新更新数据,每次更新又需要去做O(n)级别的操作。那么我们使用线段是去降低这个操作的维度

3. 线段树的样子,线段是其实是不断的把一堆统计数据不断的向下去降维,那么这个有什么用呢?比如我们统计数据是统计和,那么我们可以把线段中的 (1,2,3,4)换成 sum(1,2,3,4) = 10,那么我们求和时候就不用再去遍历数组了,直接取出符合区间范围的和就行了。比如求 1，2，3和和,那么只需要求 sum(1,2)加上sum(3)就可以了。这种的时间复杂度是logn。

	```
	
	
	 (1,2,3,4)      
	  /     \    
	(1,2)   (3,4)   
	/  \   /   \    
   1   2  3    4   
	```
4. <b>所以我们说,区间树是很适合用来做动态数据计算的,因为他的时间复杂度更低</b>
	
#### 2. 线段树的技术细节

1. 线段是是满二叉树还是 完全二叉树呢 还是平衡二叉树呢?看下面的图

    >可以看到,线段树既不是满二叉树也是完全二叉树 但是他是一个平衡二叉树
       
	```
		
					 (1,2,3,4,5,6)      
					  /           \    
					(1,2,3)        (3,4,6)  
				    /     \       /     \
				  （1,2）   3    (3,4)    6   
				  /  \          /   \    
				 1   2         3     4  
		
	```
		
2. 不过我们把线段树当成是满二叉树,(因为满二叉树可以用list数据结构来表示)

	>把区间中空的部分填充为None就可以了

	```
		
					 (1,2,3,4,5,6)      
					  /           \    
					(1,2,3)        (3,4,6)  
				    /     \       /      \
				  （1,2）   3    (3,4)     6   
				  /  \    / \     /   \   /  \
				 1   2   N   N   3     4  N   N
		
	```
	
3. 填充的list需要多大的空间才能满足?

	1. 最好的情况当然是满足刚好是 len=2^k的情况

		>那么如果有 n个数据(这里是4个) 满足是2的k次方,我们需要多少个节点(数组的下标) 来表示呢? 等比数列 (2^0 + 2^1 + .. + )+2^k = N。使用等比数列公司求得 k-1次项的和为 2^k-1,那么其实可以变为 2^k-1 + 2^k = N。又知2^k=len,所以N= 2len - 1约等于 2len。所以如果长度是4需要8个节点。
		
		```
			 (1,2,3,4)      
			  /     \    
			(1,2)   (3,4)   
			/  \   /   \    
		   1   2  3    4   
		```
		
	2. 最差的情况是

		>本来是一个满二叉树,但是又比满二叉树又多一个节点,那么就会新加一个层,他的下面全是None。 那么比满二叉树又多一层是 4len。（因为满二叉树树是2len,多一层多一倍）
		
		```
			 (1,2,3,4,5)      
			  /     \    
			(1,2)   (3,4,5)   
			/  \   /   \    
		   1   2  3   (4,5)
		              /    \   
		             4       5
		```
		
	3. 结论,你开4len的空间出来肯定不会有错

4. 需要一个merge函数,他是你的业务需求,可以使sum,max,min等等等，总之,每个节点存放的是merge之后的结果,那么你想求 3 4 5的最大值,只需要把 3 4 5 的区间统计数据之间拉出来。

5. 那么在更新的时候,也只需要跟更新值所在的区间内就行了,比如你想更新3，那么就只用去更新 根节点(因为他只含3)，根节点下面的右节点和右节点下面的左节点。不用更新所有节点。<b>更新的方式是先更新最下面的节点值,然后上面的节点值其实是下面的节点值递归运算merge函数得到的</b>


#### 3. 具体代码实现

```
	class SegmentTree:
	    """
	    data是用于存放数据的
	    tree是用于存储要查询的业务的线段树
	    """
	
	    def __init__(self, data):
	        self.data = data
	        self.tree = [None for _ in range(len(self.data) * 4)]
	        self.build_tree()
	
	    def get_size(self):
	        return len(self.data)
	
	    def build_tree(self):
	        self._build_tree(0, 0, len(self.data) - 1)
	
	    def find(self, l, r):
	        """
	        判断边界范围
	        :param l:
	        :param r:
	        :return:
	        """
	        if l < 0:
	            raise IndexError('边界不能为0')
	        if l > r:
	            raise IndexError('左边界不能大于右边界')
	        if r > (len(self.data) - 1):
	            raise IndexError('超出边界范围')
	        # 在以根节点的线段树开始搜索区间
	        return self._find(0, 0, self.get_size() - 1, l, r)
	
	    def _find(self, tree_index, tree_l, tree_r, l, r):
	        if tree_l == l and tree_r == r:
	            return self.tree[tree_index]
	        tree_mid = self._get_mid(tree_l, tree_r)
	        if l > tree_mid:
	            """
	            去右边递归
	            """
	            return self._find(self._right_index(tree_index), tree_mid + 1, tree_r, l, r)
	        elif r <= tree_mid:
	            """
	            去左边递归
	            """
	            return self._find(self._left_index(tree_index), tree_l, tree_mid, l, r)
	        else:
	            """
	            去两边递归
	            """
	            left_res = self._find(self._left_index(tree_index), tree_l, tree_mid, l, tree_mid)
	            right_res = self._find(self._right_index(tree_index), tree_mid + 1, tree_r, tree_mid + 1, r)
	
	            return self._merge(left_res, right_res)
	
	    def _build_tree(self, index, l, r):
	        """
	        创建树 里面放入元素
	        index 是在哪个位置放入元素
	        l r是放入元素的data的界限
	        :param index:
	        :return:
	        """
	        if l == r:
	            # 如有只有一个元素,则可以认为已经到达子元素
	            self.tree[index] = self.data[l]
	            return
	        # 获取中间节点值
	        mid = self._get_mid(l, r)
	        left_index = self._left_index(index)
	        right_index = self._right_index(index)
	        self._build_tree(left_index, l, mid)
	        self._build_tree(right_index, mid + 1, r)
	        self.tree[index] = self._merge(self.tree[left_index], self.tree[right_index])
	
	    def update(self, index, val):
	        self.data[index] = val
	        self._update(0, 0, self.get_size() - 1, index, val)
	
	    def _update(self, tree_index, tree_l, tree_r, index, val):
	        """
	        递归更新操作
	        :param tree_index:
	        :param tree_l:
	        :param tree_r:
	        :param index:
	        :param val:
	        :return:
	        """
	        if tree_l == tree_r:
	            self.tree[tree_index] = self.data[index]
	            return
	        left_index = self._left_index(tree_index)
	        right_index = self._right_index(tree_index)
	
	        mid = self._get_mid(tree_l, tree_r)
	        if index > mid:
	            self._update(right_index, mid + 1, tree_r, index, val)
	        else:
	            self._update(left_index, tree_l, mid, index, val)
	
	        self.tree[tree_index] = self._merge(self.tree[left_index], self.tree[right_index])
	
	    def _get_mid(self, l, r):
	        return (l + r) // 2
	
	    def _left_index(self, index):
	        return index * 2 + 1
	
	    def _right_index(self, index):
	        return index * 2 + 2
	
	    def _merge(self, left, right):
	        return left + right
	
	
	if __name__ == "__main__":
	    l = [1, 2, 3, 4]
	    s = SegmentTree(l)
	
	    y = s.find(1, 2)
	
	    x = s.update(0, 5)
	    x = 1

```


		
#### 其他话题

1. 算法题 LeetCode 303,307
2. 		
	
