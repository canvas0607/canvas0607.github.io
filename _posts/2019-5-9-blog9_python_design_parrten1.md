---
layout: post
title:  "python 设计模式1 策略模式"
date:   2019-05-1 08:59:48 +0800
categories: jekyll update
---


# python 设计模式1 策略模式

#### 1. 设计需求

1. 电商领域(比如京东)有多种多样的优惠政策 但是用户只能使用其中一种

2. 折扣如下

	1. 有1000或以上积分的顾客,每个订单享5%的优惠
	2. 同一个订单中,单个商品10个或者以上的,该商品享10%的折扣
	3. 订单中的不同商品达到2个或以上,享7%的折扣

#### 2. 需要的类

1. 用户模型

2. 优惠模型

	1. 下面有具体的不同优惠

3. 订单


#### 3. 模型设计
1. 用户模型  包含用户的名字和积分情况

	```
	from collections import namedtuple
	Customer = namedtuple('Customer', 'name fidelity')
	
	```

2. 购买商品的模型 里面包含商品的名称,数量,和单价

	```
	
	class LineItem:
	
	    def __init__(self, product, quantity, price):
	        self.product = product
	        self.quantity = quantity
	        self.price = price
	
	    def total(self):
	        return self.price * self.quantity
	
	```
	
3. 订单模型设计 里面包含订单的用户,购买商品的购物车,折扣信息和折扣价格计算

	```
	class Order:
    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion

    def total(self):
        if not hasattr(self, "_total"):
            self._total = sum(item.total() for item in self.cart)
        return self._total

    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion.discount(self)
        return self.total() - discount

    def __repr__(self):
        fmt = "<Order total: {:.2f} due: {:.2f}>"
        return fmt.format(self.total(), self.due())
	
	
	```
	
4. 折扣定义, 有多种多样的折扣策略可以定义 所以需要先定义折扣的抽象功能,然后定义折扣的具体实现功能

	```
	
		class Promotion(ABC):
	    @abstractmethod
	    def discount(self, order):
	        """
	        计算优惠方式
	
	        :return:
	        """
	
	
	class OnePromotion(Promotion):
	    """
	    如果用户的积分大于1000 打95折
	    """
	
	    def discount(self, order):
	        return order.total() * 0.05 if order.customer.fidelity >= 1000 else 0
	
	
	class TwoPromotion(Promotion):
	    """
	    单个商品大于20个,该商品折扣 10%
	    """
	
	    def discount(self, order):
	        discount = 0
	        for item in order.cart:
	            if item.quantity >= 10:
	                discount += item.total() * 0.1
	
	        return discount
	
	
	class ThreePromotion(Promotion):
	    """
	    不同种类商品有 3种或以上,所有折扣 7%
	    """
	
	    def discount(self, order):
	        discount = 0
	        products = {item.product for item in order.cart}
	        if len(products) >= 2:
	            discount += order.total() * 0.07
	        return discount
	
	```
	
5. <a href="code/c9_1.py">代码地址</a>



##### 算法计算

1. 具体算法使用 定义两个person,再定义商品的列表, 然后定义一个购物车的生成函数,商品和购买数量等随机定义 ,最后去计算每个商品购买的方案不同的价格

	```
	
	 joe = Customer("joe", 1001)
    sam = Customer('sam', 990)
    customer_list = [joe, sam]
    product_list = [('apple', 2), ("banna", 8), ("peer", 4), ("orange", 3), ("water", 1.0)]
    promotion_list = [OnePromotion, TwoPromotion, ThreePromotion]


    def gen_item(product_list):
        from copy import deepcopy
        copy_list = (deepcopy(product_list))
        random.shuffle(copy_list)
        item_list = []
        for i in range(random.randint(1, len(copy_list))):
            name, price = copy_list.pop()
            item = LineItem(name, random.randint(5, 15), price)
            item_list.append(item)

        return item_list


    for customer in customer_list:
        product_list_copy = gen_item(product_list)
        print(customer.name, '---------')
        for p in promotion_list:
            order = Order(customer, product_list_copy, p())
            print('order--> total:{},  dum:{}'.format(order.total(), order.due()))
	
	
	```
	
#### 4. 改造为函数

1. 初级版本

	```
	
	from collections import namedtuple
	from abc import ABC, abstractmethod
	import random
	
	Customer = namedtuple('Customer', 'name fidelity')
	
	
	class LineItem:
	
	    def __init__(self, product, quantity, price):
	        self.product = product
	        self.quantity = quantity
	        self.price = price
	
	    def total(self):
	        return self.price * self.quantity
	
	
	class Order:
	    def __init__(self, customer, cart, promotion=None):
	        self.customer = customer
	        self.cart = list(cart)
	        self.promotion = promotion
	
	    def total(self):
	        if not hasattr(self, "_total"):
	            self._total = sum(item.total() for item in self.cart)
	        return self._total
	
	    def due(self):
	        if self.promotion is None:
	            discount = 0
	        else:
	            discount = self.promotion(self)
	        return self.total() - discount
	
	    def __repr__(self):
	        fmt = "<Order total: {:.2f} due: {:.2f}>"
	        return fmt.format(self.total(), self.due())
	
	
	class Promotion(ABC):
	    @abstractmethod
	    def discount(self, order):
	        """
	        计算优惠方式
	
	        :return:
	        """
	
	
	def one_promotion(order):
	    """
	    如果用户的积分大于1000 打95折
	    """
	    return order.total() * 0.05 if order.customer.fidelity >= 1000 else 0
	
	
	
	
	def two_promotion(order):
	    discount = 0
	    for item in order.cart:
	        if item.quantity >= 10:
	            discount += item.total() * 0.1
	    return discount
	
	
	
	
	def three_promotion(order):
	    discount = 0
	    products = {item.product for item in order.cart}
	    if len(products) >= 2:
	        discount += order.total() * 0.07
	    return discount
	
	
	if __name__ == "__main__":
	    joe = Customer("joe", 1001)
	    sam = Customer('sam', 990)
	    customer_list = [joe, sam]
	    product_list = [('apple', 2), ("banna", 8), ("peer", 4), ("orange", 3), ("water", 1.0)]
	    promotion_list = [one_promotion,two_promotion,three_promotion]
	
	
	    def gen_item(product_list):
	        from copy import deepcopy
	        copy_list = (deepcopy(product_list))
	        random.shuffle(copy_list)
	        item_list = []
	        for i in range(random.randint(1, len(copy_list))):
	            name, price = copy_list.pop()
	            item = LineItem(name, random.randint(5, 15), price)
	            item_list.append(item)
	
	        return item_list
	
	
	    for customer in customer_list:
	        product_list_copy = gen_item(product_list)
	        print(customer.name, '---------')
	        for p in promotion_list:
	            order = Order(customer, product_list_copy, p)
	            print('promotion-->{},order--> total:{},  dum:{}'.format(p.__name__,order.total(), order.due()))
	```
	
2. 外加一个计算最优化方案的函数,使用内省自动获取到优惠函数

	1. 内省 globals() 是一个获取到全局所有符号,自动找到所有的函数名 等

		```
		[name for name in globals() if name.endswith('_promotion') and name != "best_promotion"])
		```
	

	1. <a href="code/c9_2.py">代码地址</a>
