{{ page.title }}

1.搭建django

2.在pycharm tools里面使用 run manage.py Task命令会出现命令行django命令行

3.每个功能都在自己单独的app中,使用django命令行建立django项目

```django
startapp project
```

4.还需要在项目中补充static文件存放css,js文件，log文件夹保存日志,media文件夹存入用户上传目录

5.可以建立apps 存入app

6.目录结构
>django_study 项目配置文件

>apps 存放项目app

>log 日志

>static js,css文件

>templates html文件

>manage.py 启动文件


7.在settings.py配置需要的数据库配置

```python

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "testdjango",
        'USER': "root",
        "PASSWORD": "root",
        "HOST": "127.0.0.1"
    }
}

```

8.windows环境下会报错没有 mysql-db 这个时候使用pip安装 mysqlclient

9.在manage.py中的使用makemigrations初始化数据表

>settings里面单独templates已经启用,使用配置

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        #'DIRS': [],
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```
在DIRS里面配置templates的目录 让路由能够找到模板目录

10.在manage.py中的使用migrate生成数据表

11.在pycharm中使用debug project就可以运行项目了

12.使用视图,在项目文件views.py中配置这个request到
模板文件的路径

```python

def getForm(request):
    return render(request, "message_form.html")

```

在urls.py中加入路由配置

```python
from message.views import getForm

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^form/$', getForm)
]
```

这样方位form就可以访问tem文件

13.配置静态文件,在settings配置中加入static的文件夹路径

```python
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

```

14.django orm模型 在moldes.py里面定义好数据类型

```ptyhon

class UserMessage(models.Model):
    object_id = models.CharField(primary_key=True,max_length=20,default="")
    name = models.CharField(max_length=20, verbose_name=u"用户名")
    email = models.EmailField(verbose_name=u"邮箱")
    address = models.CharField(max_length=100, verbose_name=u"地址")
    message = models.CharField(max_length=500, verbose_name=u"留言信箱")

    class Meta:
        verbose_name = u"用户留言信息"

```
在setttings中加入这个app

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'message',
]

```

使用manage.py命令生成数据表

```python
makemigrations message
migrate message
```

> 数据库表名是
app名称小写_class名称小写
这个数据表名称是 message_usermessage

15.django数据的curd

>数据查询

```python
def getForm(request):
     #all_messages = UserMessage.objects.all()
     #for message in all_messages:
     #    print(message.name)
         
     all_messages = UserMessage.objects.filter(name=xxx)
     for message in all_messages:
         print(message.name)
    return render(request, "message_form.html")

```

可以通过UserMessage.objects.filter(name=xxx)查询想要的条件 获取过滤后的List

>数据保存

```python

def getForm(request):
    if request.method == "POST":
        user_message.name = 'canvastest'
        user_message.email = 'qq121@qq.com'
        user_message.address = 'tttt'
        user_message.message ='hello'
        user_message.object_id = 'testid'
        user_message.save()
    return render(request, "message_form.html")

```
将数据实例化后 调用 save方法 保存数据

```python
def getForm(request):
    all_messages = UserMessage.objects.filter(name='canvas')
    for message in all_messages:
        print(message.name)
        message.delete()
    return render(request, "message_form.html")

```

调用message.delete()删除数据

16.django url别名设置
在python中设置了url的别名 这样以后修改url就不用
再去修改html中的url了

```python
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^form_go/$', getForm, name='go_form')
]

```
在html中使用Url别名

```html
<form action='{\% url "go_form" %\}' method="post" class="smart-green">
```



