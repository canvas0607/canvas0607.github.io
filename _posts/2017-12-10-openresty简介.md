## 简介

OpenResty（也称为 ngx_openresty）是一个全功能的 Web 应用服务器。它打包了标准的 Nginx 核心，很多的常用的第三方模块，以及它们的大多数依赖项。
通过揉和众多设计良好的 Nginx 模块，OpenResty 有效地把 Nginx 服务器转变为一个强大的 Web 应用服务器，基于它开发人员可以使用 Lua 编程语言对 Nginx 核心以及现有的各种 Nginx C 模块进行脚本编程，构建出可以处理一万以上并发请求的极端高性能的 Web 应用。

## CentOS 平台安装

```bash

sudo yum-config-manager --add-repo https://openresty.org/yum/cn/centos/OpenResty.repo
sudo yum install openresty
```

## HelloWorld

#### 创建工作目录

```bash

$ mkdir ~/openresty-test ~/openresty-test/logs/ ~/openresty-test/conf/
$
$ tree ~/openresty-test
openresty-test
├── conf
└── logs

```

#### 创建配置文件

nginx.conf

```nginx
worker_processes  1;        #nginx worker 数量
error_log logs/error.log;   #指定错误日志文件路径
events {
    worker_connections 1024;
}

http {
    server {
        #监听端口，若你的6699端口已经被占用，则需要修改
        listen 6699;
        location / {
            default_type text/html;

            content_by_lua_block {
                ngx.say("HelloWorld")
            }
        }
    }
}

```

#### 启动

```bash

nginx -p ~/openresty-test

```

# 干货

楚乔传服务器bak

管理地址
http://123.58.150.83:6699/html/request_time.html

账户 admin

拦截地址
http://123.58.150.83:6699/app.php/api/cqz/simplified/sl/login

代码
https://coding.net/u/liubaoling/p/ipblock

http://123.58.150.83:36699/param?a=1

