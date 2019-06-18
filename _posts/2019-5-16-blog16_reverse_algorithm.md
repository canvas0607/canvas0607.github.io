---
layout: post
title:  "反转算法"
date:   2019-05-16 08:59:48 +0800
categories: jekyll update
---



# 反转算法

#### 1. 概述的算法基本概要

反转算法顾名思义,就是如何把一条列表如何反转过来。

[1,2,3,4,5,6,7,8,9] 经过算法变成 --> [9,8,7,6,5,4,3,2,1]

#### 2. 算法如果理解

假如 1 2 3 4 那么算法的步骤是 2 1 3 4  -->   3 2 1 4  --> 4 3 2 1 只需要每次把 1的右边的数据 放在最左边即可


#### 3. 简单的list算法实现

1. 按照 2的算法 实现了list

	```
	l1 = list((i for i in range(10)))
	
	print(l1)
	
	
	def reverse(l):
	    i = 0
	    while i < len(l) - 1:
	        move_node = l[i + 1]
	        del l[i + 1]
	        l.insert(0, move_node)
	        i += 1
	        print(l)
	    return l
	
	
	print(reverse(l1))
	```
	
#### 4. 双向链表的交换实现

1. 双向链表的实现的思想和上面的一模一样,不过要注意维护链表的结构

2. 基本算法,和上面的一样, 不过要先找到替换的头,也就是第一个移动的元素和最后一个移动的元素,第一个移动的元素是头指针指向的下一个元素,找到第一个元素, 找到第一个元素的下一个元素,也就是要移动的元素 next_node 然后把移动的元素的结构改变,把移动的上一个指针指向第头指针。

```

from liu.link import Link


# 翻转函数
def rev(l, m):
    def recusive(first_node_father, m):

        first_node = first_node_father.next

        if first_node is None:
            return

        n = m - 1
        move_node = first_node.next

        while n:
            if move_node is None:
                return

            # 移动move_node到左边去
            first_node.next = move_node.next
            if first_node.next is None:
                return
                #更高移动指针的下一个元素,由于移动元素已经移走,所以他的下一
                #指针指向第一个元素
            move_node.next.prev = first_node
				#把移动元素的上一个指针指向第头指针
            move_node.prev = first_node_father
            #移动元素移动到了第一个元素,所以第二个元素要指向他
            move_node.next = first_node_father.next
            first_node_father.next.prev = move_node
            #头指针的下一个元素也要指向移动元素
            first_node_father.next = move_node
				#租后更改移动元素,下一步移动的元素就是第一个元素的下一个元素
            move_node = first_node.next

            n -= 1
        recusive(first_node, m)

    recusive(l.head, m)


test = Link([1, 2, 3, 4, 5, 6, 7])
rev(test,5)
for i in test:
    print(i)

```

#### 附录:

双向链表

```
__all__ = ["Link", "list"]

import queue


class Node:
    def __init__(self):
        self.data = None
        self.next = None
        self.prev = None


class Link:
    def __init__(self, data=()):
        self.head = Node()
        self.tail = self.head
        self.length = 0
        for d in data:
            self.append(d)

    def __find_node_by_pos(self, pos):
        """
            find the node with the given position.
            +------+      +-------+      +------+
            | head |--->  | data  | ---> | data |
            +------+      +-------+      +------+
        :param pos:
        :return:
        Note: the position will be started with the head node.
        """
        try:
            assert pos <= len(self) - 1
        except AssertionError:
            raise IndexError

        node_ptr = self.head
        while pos:
            node_ptr = node_ptr.next
            pos -= 1
        return node_ptr

    def __remove_node_by_pos(self, pos):
        """
        remove the node with specified position
        :param pos:
        :return: the deleted node.
        """
        try:
            assert pos <= len(self) - 1
        except AssertionError:
            raise IndexError

        node = self.__find_node_by_pos(pos).next
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        if next_node:
            next_node.prev = prev_node
        if node == self.tail:
            self.tail = prev_node
        return node

    def append(self, data):
        node = Node()
        node.data = data
        self.tail.next = node
        node.prev = self.tail
        self.tail = node
        self.length += 1

    def pop(self, i=-1):
        if i == -1:
            if self.head == self.tail:
                raise IndexError

            node = self.tail
            self.tail = node.prev
            self.tail.next = None
            self.length -= 1
            return node.data
        else:
            node = self.__remove_node_by_pos(i)
            return node.data

    def insert(self, i, data):
        try:
            assert i <= len(self) - 1
        except AssertionError:
            raise IndexError

        node_ptr = self.head
        while i:
            node_ptr = node_ptr.next
            i -= 1

        third_node = node_ptr.next
        node = Node()
        node.data = data

        node.next = third_node
        third_node.prev = node

        node_ptr.next = node
        node.prev = node_ptr
        self.length += 1

    def remove(self, object):
        node_ptr = self.head.next
        while node_ptr:
            if node_ptr.data == object:
                break
            else:
                node_ptr = node_ptr.next

        if not node_ptr:
            return

        prev_node = node_ptr.prev
        next_node = node_ptr.next
        prev_node.next = next_node
        if next_node:
            next_node.prev = prev_node

    def extend(self, iterable):
        for d in iterable:
            self.append(d)

    def __len__(self):
        return self.length

    def __iter__(self):
        return LinkIterator(self)

    def __setitem__(self, key, value):
        try:
            assert key <= len(self) - 1
        except AssertionError:
            raise IndexError

        node = self.__find_node_by_pos(key)
        node.next.data = value

    def __getitem__(self, item):
        try:
            assert item <= len(self) - 1
        except AssertionError:
            raise IndexError

        node_ptr = self.head.next
        while item:
            node_ptr = node_ptr.next
            item -= 1
        return node_ptr.data

    def __contains__(self, item):
        for d in self:
            if d == item:
                return True
        return False

    def __add__(self, other):
        l = Link()
        for i in self:
            l.append(i)
        for i in other:
            l.append(i)
        return l

    def __iadd__(self, other):
        # for i in other:
        #     self.append(i)
        # return self
        return self.__add__(other)

    def __sub__(self, other):
        pass

    def __isub__(self, other):
        pass

    def __mul__(self, other):
        pass

    def __divmod__(self, other):
        pass

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        for i in range(len(self)):
            if self[i] != other[i]:
                return False
        return True


class LinkIterator:
    def __init__(self, link):
        self._node_ptr = link.head

    def __next__(self):
        self._node_ptr = self._node_ptr.next
        if self._node_ptr is None:
            raise StopIteration
        data = self._node_ptr.data
        return data


# i = 1
# print(id(i))
# i += 2
# print(id(i))
l = list()

list = Link

if __name__ == "__main__":
    x = list()
    y = list()
    m = (x, y)

    m[0].append(1)
    m[1].append(2)

    # print(id(x), id(y))
    # print(x == y)

#
# x += y
# for m in x:
#     print(m)

# x[2] = 4
# x.insert(3, 8)
# print(x.pop())
# x.append(1)
# x.append(2)
# x.append(3)
# while x:
#     print(x.pop())

# x[0] = 1
# y = x[0]
#
# for d in x:
#     for y in x:
#         print(y)


# x.insert(1, 8)
# for d in x:
#     print(d)
#
# print("\n")
# x.remove(1)
# for d in x:
#     print(d)

# if 2 in x:
#     print("2 is in list")
#
# print("The 2th is: %d" % x[1])

x = [1, 2, 3, 4]
y = [5, 6, 7, 8]

z = x + y
x += y

```



  
