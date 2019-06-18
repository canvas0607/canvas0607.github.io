---
layout: default
title: git branch and remote branch(git 分支远程分支)
---
{{ page.title }}

### 1.git分支

#### 1.本地分支理解和操作

a.HEAD指针,特殊指针,标识你目前在哪个分支下工作

b.分支只是指针,指向某个提交对象。

b.官网链接说明-->

https://git-scm.com/book/zh/v2/Git-%E5%88%86%E6%94%AF-%E5%88%86%E6%94%AF%E7%AE%80%E4%BB%8B#divergent_history

#### 关于分支的实用操作

a.新建分支
```bash
$ git branch testing
```

>分支新建后默认指向当前提交对象，但是如果有新的提交,新建的分支不会移动,因为只是
新建了分支,并木有切换到这个分支下面工作,所以如果现在有新的提交,那么你现在的默认分支
master会移动(因为HEAD指针还是指向master分支)。

b.切换分支
```bash
$ git checkout testing
```

>这个时候HEAD指针会指向testing分支,代码版本也会切换到testing分支当前指向的提交对象

c.新建并切换分支
```bash
$git checkout -b testing
```

>新建加切换一步完成

d.如果有几个分支,查看分叉历史

```bash
git log --oneline --decorate --graph --all
```

#### 2.远程分支理解和操作

官网链接

https://git-scm.com/book/zh/v2/Git-%E5%88%86%E6%94%AF-%E8%BF%9C%E7%A8%8B%E5%88%86%E6%94%AF

1.远程分支在远程仓库上面的分支,可以在本地引用它,但是不能修改它,你可以让本地的
一个分支去引用这个远程分支,这样提交这个本地分支的更新后,可以通过push来使远程仓库的
这个分支移动

2.操作:

a.比如你在本地的某个分支提交了更新(commit),那么你可以使用git push master master
把更新推送到master仓库的 master分支

b.也可以直接push不用加仓库名,前提是你把这个分支设定到跟踪远程分支,这样你每次push就行了
自动推送到你设定好的分支

修改远程引用,比如你现在master分支正在引用远程仓库的master,现在想把master分支的更新,
推送到远程的prod分支上面,不过你现在已经在跟踪master了 需要修改

```bash
$ git branch -u master/prod

```

命令解释 推送到master仓库的prod分支

c.利用远程分支的工作方式

如果有一个任务,需要修改登录的某个需求,然后在线上测试,这个时候你肯定不想直接在master主
分支修改,因为如果你在主分支修改了Login,然后没有修改好,还在测试。这个时候来了一个紧急需求,
需要关闭封号接口,这个需求很简单,把代码注释了上传上去就行了,但是你Login没有修改好,这个时候上传
肯定是影响登录了,那就完蛋了。你可以小心翼翼的把login代码改回到正常以前的版本。但是难免出错。
或者也可以用git reset --hard把本地Login回到以前的正常版本。然后上传。但是都不是优雅而且简便的方式。
因为你到头来还是要做login的需求,需要重新写代码

##### 正确的工作流是:
1.接到了login的新需求,我知道这个需求需要改一段时间,而且需要测试之类的。
所以我新建一个login_test的分支,并且切换到这个分支下面工作

```bash
$ git checkout -b login_test
```

2.按照客户需求修改代码。这个时候我不用怕,因为出了问题我大不了不要这个分支了,切换回master分支。
master的代码反正是之前的。在我修改了之后,需要传到线上测试服去测试这个功能。那么我肯定不会推送到
远程仓库的Master去。而是推送到master仓库的login_test分支(在master上面新加这个分支),然后把测试服务器
上面新加一个login_mod(随便什么名字都可以)分支,然后这个分支拖远程仓库的login_test分支。这样我本地的login_test分支就和
测试服的login_mod分支同步了。

按照上面的思路操作(第一步已经在本地创建了login_test分支了)

a.提交修改(login是你修改的文件,实际上面add你修改的文件)

```bash
$ git add (login)
$ git commit -m '修改了我的login文件'
```

b.把这个本地分支 跟踪到一个远程分支 (当然需要新加一个远程分支让本地分支推代码上去)

```bash
$ git push master login_test
```

把我目前的分支提交到master仓库的 login_test分支(这个远程会自动新建这个分支)

c.登录到远程测试服务器上面拖测试代码(拖login_test分支)

```bash
$ git fetch master
```

获取master仓库的信息更新,因为我本地向master仓库推了代码,但是服务器上面还不知道,
这个时候用

```bash
$ git branch -a
```

就可以看到远程仓库有新的信息

```bash
$ git checkout -b test master/git_test
```

我新加了一个test分支 并且切换到这个分支 并且让这个分支跟踪 master/git_test

或者
```bash
$ git checkout --track master/git_test
```


我新加了一个git_test分支 并且切换到这个分支 并且让这个分支跟踪 master/git_test
(不用指定分支名字了)

或者可以通过下面步骤完成

```bash
$ git checkout -b test
$ git branch -u master/git_test
```

不过老版本的git不能用branch -u,

现在你可以在本地修改代码 然后 push 然后在远程测试服 pull，测试更新。
如果有关闭角色查询功能,你只需要切换到master分支,然后把他注释了。
然后推送,(这时候在master分支,推送到远程仓库master分支)。然后在正式服务器
上面托代码下面就完成。这样你login代码保住了,需求也很快修改了。

然后你login代码修改完毕了,测试也通过了,这个时候要更新到正式服上面去，
需要把正式服的代码和测试完毕的代码合并。这样正式服的login代码就更新了。

```bash
$ git checkout master
$ git merge login_test
```

这样你先切换到master分支,合并login_test的修改。然后push上去就行了

最后 login_test没用了 删除他,远程仓库也有login_test没用,删除

```bash
$ git checkout -d login_test
$ git push master --delete login_test
```

完成了一次优雅的代码更新。

其他小命令

```bash
$ git branch -a
$ git branch -vv
```

1.查看所有分支包括远程分支
2.查看分支跟踪了哪个远程分支








