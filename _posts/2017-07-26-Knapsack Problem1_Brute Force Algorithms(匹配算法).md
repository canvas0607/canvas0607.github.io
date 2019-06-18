---
layout: default
title: 背包问题2,暴力算法 (Brute Force Algorithms)
---
{{ page.title }}

1.问题
>假设有 wine,apple,beer 和一个背包,把背包装有签名三个物品所有可能性
表达出来,比如 [wine,beer],[wine],[apple,wine] . etc

2.函数表达

>假设有 list [win,beer,apple]，用一个list表达所有组合

```python

def powerSet(items):
    N = len(items)
    res = []
    # enumerate the 2**N possible combinations
    # 首先生成2的次方个背包
    for i in range(2**N):
        combo = []
        for j in range(N):
            # test bit jth of integer i
            if (i >> j) % 2 == 1:
                combo.append(items[j])
        res.append(combo)
    return res


#结果
[[], ['wine'], ['beer'], ['wine', 'beer'], ['apple'], ['wine', 'apple'], ['beer', 'apple'], ['wine', 'beer', 'apple']]
```

算法解释:

>理解为使用数字代替某一个组合. 0代表不放入背包,1代表放入背包

| apple| beer | wine |
|------| ----| -----|
| 0| 0 | 0 |
| 0| 0 | 1 |
| 0| 1 | 1 |
| 0| 1 | 0 |

 .......
>把上面的组合理解成2二进制数

> 一共有 2**n 次方组合

>把生成的每个背包标号 从0开始 例如最后一个背包编号7
> 转换成二进制 111 那么每个物品都放入背包中

2.1 扩展问题, 把上面物品放入两个背包的组合

```python
def yieldAllCombos(items):
    N = len(items)
    res = []
    # Enumerate the 3**N possible combinations
    for i in range(3**N):
        bag1 = []
        bag2 = []
        for j in range(N):
            if (i // (3 ** j)) % 3 == 1:
                bag1.append(items[j])
            elif (i // (3 ** j)) % 3 == 2:
                bag2.append(items[j])
        combo = (bag1, bag2)
        res.append(combo)
    return res
```

解释,同上 把背包数字转换成三进制进行计算 0不放 1放bag1 2放bag2

| apple| beer | wine |
|------| ----| -----|
| 0| 0 | 0 |
| 0| 0 | 1 |
| 0| 0 | 2 |
| 0| 1 | 2 |


items = ['wine','beer']
结果
[([], []), (['wine'], []), ([], ['wine']), (['beer'], []), (['wine', 'beer'], []), (['beer'], ['wine']), ([], ['beer']), (['wine'], ['beer']), ([], ['wine', 'beer'])]

第二种实现方法

```Python

def maxVal(toConsider, avail):
    if toConsider == [] or avail == 0:
        result = (0, ())
    elif toConsider[0].getCost() > avail:
        #重量过大 不能拿取
        result = maxVal(toConsider[1:], avail)
    else:
        nextItem = toConsider[0]
        #遍历拿取的情况
        withVal, withToTake = maxVal(toConsider[1:],
                                     avail - nextItem.getCost())
        withVal += nextItem.getValue()
        #遍历不拿取得情况
        withoutVal, withoutToTake = maxVal(toConsider[1:], avail)
        if withVal > withoutVal:
            result = (withVal, withToTake + (nextItem,))
        else:
            result = (withoutVal, withoutToTake)
    return result
```







