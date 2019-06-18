---
layout: default
title: greedy algorithms (贪婪算法)
---
{{ page.title }}

1.问题
>如果一个小偷有一个背包 最大负载1000,现在有 啤酒,苹果,汉堡等物品可以偷走,
假设件物品都有各自的重量和价格,当然,肯定不能全部带走,小偷的条件是带走再背包能承受
最大重量的前提下,价格总和最高的物品组合。(比如啤酒和苹果组合,或者苹果和汉堡组合)


2.如何计算这个问题
>解法有很多种,可以把所有的组合一一列举出来(算法复杂度 2的n次方),计算每一个组合的重量和
价格,在挑选出最大的价值的组合。但是如果要带走的个数过多的话,计算机计算的时间会指数级
增长,因为如果有100个组合,那么计算的个数为 2**100,那么计算机计算中这个问题会很慢。

3.贪婪算法
>上面的问题并不是无解,其中之一是可以使用贪婪算法来计算,贪婪算法的结果近似于枚举。
(可能等于枚举算法,也肯能不如枚举算法的值),但是从时间效率来说,贪婪算法要好很多很多。

4.贪婪算法的解释

>小偷可以用某种方式给要拿走的东西排序,排序的结果是小偷认为最想先拿走的东西放在第一位,
然后依次排列,小偷按照自己排好的顺序来一个一个拿走,如果发现装不下了,就撤退

5.关于最想拿走的东西的解释

>小偷最想拿走的不一定是价值最高的,当然也可以用价值最高的依次排序,但是也可以用价值除以重量的比例
最大的来排序。所以重点就是在于小偷怎么给物品排序。

6.算法的实现

环境 Python 3.6 IDE:Anaconda

>代码思路
首先给每个物品排序,依次遍历所有物品,不过物品重量加上现有背包重量,未超出最大重量则拿走
,否则不拿走物品,遍历下一个物品

```python
#物品的名字
names = ['wine', 'beer', 'pizza', 'burger', 'fries','cola', 'apple', 'donut', 'cake']
#价值
values = [89,90,95,100,90,79,50,10]
#重量
calories = [123,154,258,354,365,150,95,195]

#初始化物品,每个物品都有获取价值,重量,单价,的方法
class Food(object):
    def __init__(self, n, v, w):
        self.name = n
        self.value = v
        self.calories = w
    def getValue(self):
        return self.value
    def getCost(self):
        return self.calories
    def density(self):
        return self.getValue()/self.getCost()
    def __str__(self):
        return self.name + ': <' + str(self.value)\
                 + ', ' + str(self.calories) + '>'

#建立所有食物的数组
def getItems(names,values,weights):
    items = []
    for i in range(len(names)):
        item = Food(names[i],values[i],weights[i])
        items.append(item)
    return items
#算法
def greedy(items,maxW,sortFun):
    #给要取出的物品排序
    #算法复杂度 n*log(n)
    newItems = sorted(items,key=sortFun,reverse=True)
    tokenW = 0 #已经拿取的重量
    tokenItems = [] #拿取的物品
    tokenV = 0
    #复杂度 n
    for i in range(len(newItems)):
        if newItems[i].getWeight() + tokenW <= maxW:
            tokenItems.append(newItems[i])
            tokenW += newItems[i].getWeight()
            tokenV +=newItems[i].getValue()
    #返回取出的目录和总价值
    return (tokenItems,tokenV)

#调用greedy 取出返回值
def testGreedy(items,maxW,sortFun):
    items,totalVal = greedy(items,maxW,sortFun)
    print('totalVal:'+str(totalVal))
    for i in items:
        print(' ',i)

def testGreedys(foods, maxUnits):
    #按价值排序
    print('Use greedy by value to allocate', maxUnits,
          'calories')
    testGreedy(foods, maxUnits, Food.getValue)
    #按重量排序
    print('\nUse greedy by cost to allocate', maxUnits,
          'calories')
    testGreedy(foods, maxUnits,
               lambda x: 1/Food.getWeight(x))
    #按单价排序
    print('\nUse greedy by density to allocate', maxUnits,
          'calories')
    testGreedy(foods, maxUnits, Food.getDensity)


names = ['wine', 'beer', 'pizza', 'burger', 'fries',
         'cola', 'apple', 'donut']
values = [89,90,95,100,90,79,50,10]
weights = [123,154,258,354,365,150,95,195]

items = getItems(names,values,weights)
testGreedys(items,725)
testGreedys(items,500)
testGreedys(items,1000)

```

运行函数 可以看出每个排序方式下的组合不一样,最大价值也不一样。
所以说贪婪算法不是最优的算法,但是相比下效率高 也很解决最优的组合


贪婪算法的算法复杂度:
    排序 sorted函数: n*log(n) (python sorted函数复杂度)
    遍历数组: n
    总复杂度 n*log(n) + n = O(n*log(n))

参考资料
>1.算法导论 https://courses.edx.org/courses/course-v1:MITx+6.00.2x_7+1T2017/course/

>2.图解算法 https://book.douban.com/subject/26979890/