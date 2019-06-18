{{ page.title }}

1.ansible简介

2.ansible安装
安装python2.7或以上版本
使用get_pip.py 安装pip
使用pip安装ansible
```
pip install ansible
```

3.ansible启动寻找配置文件顺序
ansible 会首先寻找 本目录下面 ansible.cfg文件,
然后会寻找 /etc/ansible/ansible.cfg 文件

4.ansible.cfg 基本配置

```
[defaults] #用户组
inventory = ./inventory #hosts配置
remote_user = vagrant #登录使用的host
private_key_file = /root/.vagrant.d/insecure_private_key #ssh密钥
host_key_checking = False
```

5.inventory 介绍

```
[centos]
centos2 ansible_ssh_host=127.0.0.1 ansible_ssh_port=2204
centos3 ansible_ssh_host=127.0.0.1 ansible_ssh_port=2205
centos4 ansible_ssh_host=127.0.0.1 ansible_ssh_port=2206
centos5 ansible_ssh_host=127.0.0.1 ansible_ssh_port=2207
centos7 ansible_ssh_host=127.0.0.1 ansible_ssh_port=2208

```
[centos]表示是centos组,下面centos2-centos7表示单个主机

ansible_ssh_host->表示操作ip地址 ansible_ssh_port 表示端口号

6.
