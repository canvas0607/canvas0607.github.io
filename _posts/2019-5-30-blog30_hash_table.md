---
layout: post
title:  "hash表"
date:   2019-5-30 08:59:48 +0800
categories: jekyll update
---

# hash表

#### 什么是hash表

1. hash和之前的二叉树 红黑树一样 是一种数据结构 用于存储数据,但是之前上面数据结构他的算法复制度都是logn级别的,hash表的算法复杂度是 O(1)级别

#### 具体的hash表存储

1. 存储结构图

	```
		 
		| 0 | -->{data,data }
		| 1 | -->{ data,data}
		| 2 | -->{ }
		| 3 | -->{ }
		| 4 | -->{ }	
							    
	```
	
2. 解释 hash表首先开辟n个桶,把每个数据计算一个特征值,然后放入桶内,那么如果两个数据的特征值一样,就会放入同一个桶里面。这个时候就是所谓的hash冲突,解决这个冲突的方式有各种各样,其实可以把冲突的值放入链表中或者树结构中去。

3. 为什么hash的复杂度为 O(1)?上面开辟的空间只有4个桶,那么100w条数据插入进去,不就是插入在四个树里面?时间复杂度不是O(logn)吗?

	> 其实可以动态的去增加桶的个数或者减少桶的个数,可以只保证桶里面的树最多能存储 10个元素,一旦多余10个元素,那么我就增加桶,重新的分配元素所在的桶,那么可以桶一个指标去衡量
	
	
4. 桶的个数和元素在哪个桶里面的hash值计算。对于int 那么直接有整数值,对于float可以把float的二进制表示看做成整数表示,进而使用int来表示。对于字符或者字符串类型也可以使用int来表示(这里只是粗略的计算)。那么可以把计算出来的值,和桶的数量做模运算。运算出来的余数就可以作为桶的编号。为了能让元素能均匀的分配在所有的桶中,可以把桶的数量变为素数。


5. 每次增加元素,可以计算整个hash表中的元素个数,然后去和桶的数量做比较,如果比较的结果是 10.那么说明某个桶肯定里面有10个元素了。那么根据上面的性质。就可以把元素重新的分配位置

	>扩展数组的个数,重新分配所有元素
		
	```
		 
		| 0 | -->{data }
		| 1 | -->{ data}
		| 2 | -->{ }
		| 3 | -->{ data}
		| 4 | -->{ }				
		| 5 | -->{data }
		| 6 | -->{ data}
		| 7 | -->{ }
		| 8 | -->{ }
		| 9 | -->{data }					    
	```


#### 代码


```

from avl.avl_test import AVL


class MyHash:
    def __init__(self):
        self.init_size = 2
        # 初始化数组来作为桶
        self.buckets = [AVL() for _ in range(self.init_size)]
        # 动态的计算桶冲突,增加空间
        self.upper_tol = 2
        self.low_tol = 1
        self.size = 0

    def _get_rating(self):
        return self.size/self.init_size

    def put(self, val):
        bucket_num = self._get_bucket_num(val)
        tree = self.buckets[bucket_num]
        tree.add(val)
        self.size += 1
        if self._get_rating() > self.upper_tol:
            self.init_size *= self.init_size
            new_buckets = [AVL() for _ in range(self.init_size)]
            for bucket in self.buckets:
                for val in bucket:
                    bucket_num = self._get_bucket_num(val.data)
                    tmp_tree = new_buckets[bucket_num]
                    tmp_tree.add(val.data)
            self.buckets = new_buckets

    def _get_bucket_num(self, val):
        hash_val = abs(hash(val))
        bucket_num = hash_val % self.init_size
        return bucket_num

    def find(self, val):
        bucket_num = self._get_bucket_num(val)
        tree = self.buckets[bucket_num]
        return val in tree


if __name__ == "__main__":
    h = MyHash()
    print(h.put(1))
    print(h.put(2))
    print(h.put(3))
    print(h.put(4))
    print(h.put(5))
    print(h.put(55))

```


#### 其他话题

# 更多处理hash冲突的处理方式

1. 开放地址法 --> 线性探测 |平方探测法 |二次哈希
2. 再哈希法
3. coalesced hashing
