"""
流畅python 第六章

知识点 策略模式 uml图 简单的

设计一个购物优惠计算的模型,可以计算用户的订单优惠值
"""

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
            discount = self.promotion.discount(self)
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


if __name__ == "__main__":
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
            print('promotion-->{},order--> total:{},  dum:{}'.format(p.__name__,order.total(), order.due()))
