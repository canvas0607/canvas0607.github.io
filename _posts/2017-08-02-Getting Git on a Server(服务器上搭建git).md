---
layout: default
title: git on server (服务器上面搭建git)
---
{{ page.title }}

1.首先在远程服务器上面建立一个空仓库

```bash
$ mkdir test
$ cd test
$ git init
```

2.建立裸仓


```bash
# on server
$ git clone test cqz.git
```

cqz.git这个目录就是远程仓库 已经初始化好了

3.在本地添加这个远程仓库然后跟踪远程分支,并且推送

```bash
$ git remote add re root@192.168.1.189:/www/test.git
$ git push re copy
```

如果显示
```
error: src refspec [branch] does not match any.
error: failed to push some refs to 'https://github.com/kkammo/yonseitree.git'
```

直接推送head
连接 https://stackoverflow.com/questions/26701683/src-refspec-does-not-match-any

```bash
$ git show-ref
$ git push re HEAD:master
```

4.另外一个本地托代码(git clone)





