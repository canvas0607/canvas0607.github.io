---
layout: default
title: reverse a list (翻转一个Python list)
---
{{ page.title }}

```python
def matrixElementsSum(matrix):
    price = 0
    if  len(matrix) == 1:
        n_list = matrix[:]
        for i in n_list:
            for j in i:
                if j == 0:
                    break
                price = price + j
        return price
    else:
        max_y = len(matrix)
        max_x = len(matrix[0])
        price = 0
        new_list = [ [ 0 for x in range(max_y)] for y in range(max_x)]
        n_list = new_list[:]


    for x in range(len(matrix)):
        for y in range(len(matrix[0])):

            #try:
            #print(str(y)+":"+str(x))
            n_list[len(matrix[0])-y-1][x] = matrix[x][y]


```