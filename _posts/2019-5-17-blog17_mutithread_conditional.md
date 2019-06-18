---
layout: post
title:  "多线程切换,通信"
date:   2019-05-17 08:59:48 +0800
categories: jekyll update
---


# 多线程切换,通信

#### 1. 线程间切换基础 wait notify

1. 多线程提供了暂停和恢复暂停的操作, wait的操作是释放锁和阻塞线程(类似于Input函数)，由于wait会生成一个阻塞,所以需要一个操作去解开阻塞, 类似于input操作,input操作开始会阻塞,但是有键盘操作后,就会向下执行。notify就是这个操作。执行了notify之后,wait就会向下执行。

2. 细节用法:

	1. wait,

	2. notify
