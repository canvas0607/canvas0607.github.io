# 上课笔记
f
1. 队列结构fifo

2. 堆栈结构 filo

3. 迷宫算法可以用堆栈来实现(状态机?)

4. python += 实现 iadd

5. python ==(__eq__)运算 一般实现的迭代两个元素,一一计算是否值相等

6. 翻转 1 2 3-->    ||2 -->1  -->3||  3-->2--->1|| 1不动,移动2到1左边,然后1就在3的前面了,再把3移动到最前面 完成翻转| 只会循环 3-1=2次  liu->lib->3

7. 条件变量 condition wait notify

8. __all__=["link","list"]  import *的时候用 指定 需要用到的块

9. 闭包函数,递归,翻转节点

10. 还要完成递归

11. sys.flush() 把数据流(缓存中的数据) 输出到磁盘上面去

12. pdb   

13. knn算法作业

14. 对象的取值是 __dict__

15. 类属性 

```
class A:
	attr = 'sdaf'
```
attr不在 __dict__ 但是attr在__class__的 __dict__里面

__getattr__ 当对象么有值的时候,就会调用这个方法,比如 a.name 如果没有设置name 调用这个方法

调用属性的时候 __getitem__, __setitem__

16. django 中间件 django中间件如何挂载的?

17. poll epoll 模型的时候, 二进制的与操作的应用

18. poll epoll返回的只是文件描述符

19. drawio



