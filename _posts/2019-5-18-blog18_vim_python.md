---
layout: post
title:  "vim 编辑器python配置"
date:   2019-05-18 08:59:48 +0800
categories: jekyll update
---


# vim 编辑器python配置


#### python 代码提示安装

1. 替换vim编辑器为macvim
	
	```
	brew install cmake macvim
	
	```
	
2. 安装插件 这里选择安装全部插件

	```
	cd ~/.vim/bundle/YouCompleteMe
	./install.py --all
	```
	
	>可能会有些报错 跟着错误提示信息走就行了
	


	
#### 配置目录树

1. 配置插件

	```
	Plugin 'scrooloose/nerdtree'
	```
	
2. 配置自动启动插件和插件显示快捷键 crtl+n可以启动插件,加上之前配置的分屏切换,就可以来回切换

	```
	autocmd vimenter * NERDTree
	map <C-n> :NERDTreeToggle<CR>
	```
3. 忽略pyc文件

	```
	let NERDTreeIgnore=['\.pyc$', '\~$'] "ignore files in NERDTree
	```
	
#### 配置搜索

1. crtl+p 配置搜索

	```
	
	Plugin 'kien/ctrlp.vim'
	```
