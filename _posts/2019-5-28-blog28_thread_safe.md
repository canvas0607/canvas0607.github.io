---
layout: post
title:  "python 条件变量和线程安全的queue结构"
date:   2019-05-28 08:59:48 +0800
categories: jekyll update
---


# python 条件变量和线程安全的queue结构

#### condition的概念与使用

1. condition可以理解为条件变量,可以用来暂停线程和唤醒线程

2. conditino必须与线程锁并存

3. condtion 里面有几个重要的参数

	1. acquire([timeout])/release(): 调用关联的锁的相应方法。 
	
	2. wait([timeout]): 调用这个方法将使线程进入Condition的等待池等待通知，并释放锁。使用前线程必须已获得锁定，否则将抛出异常。 
	3. notify(): 调用这个方法将从等待池挑选一个线程并通知，收到通知的线程将自动调用 acquire()尝试获得锁定（进入锁定池）；其他线程仍然在等待池中。调用这个方法不会释放锁定。使用前线程必须已获得锁定，否则将抛出异常。 
	4. notifyAll(): 调用这个方法将通知等待池中所有的线程，这些线程都将进入锁定池尝试获得锁定。调用这个方法不会释放锁定。使用前线程必须已获得锁定，否则将抛出异常。

