{{ page.title }}

1.改写django 后台用户管理表单 继承AbstractUser类(原生auth_user表)
添加想要的字段 代码如下

```python

# _*_ coding: utf-8 _*_
from django.db import models
# 集成本来的auth_user
from django.contrib.auth.models import AbstractUser


# Create your models here.

class UserProfile(AbstractUser):
    nick_name = models.CharField(default="", max_length=50, verbose_name=u"昵称")
    birthday = models.DateField(verbose_name=u"生日", null=True, blank=True)
    gender = models.CharField(max_length=7, choices=(("male", u"男"), ("female", u"女")), default="female")
    address = models.CharField(max_length=100, default=u"")
    mobile = models.CharField(max_length=11, default="")
    image = models.ImageField(upload_to="image/%Y/%m", default=u"image/default.png", max_length=100)

    class Meta:
        verbose_name = u"用户信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username

```

settings.py,添加users的app 并且把AUTH_USER_MODEL改到上面的modle中去

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
]
AUTH_USER_MODEL = "users.UserProfile"

```
运行mkmigartions 和migrate来生成数据表
2.报错
```shell
 HINT: MySQL's Strict Mode fixes many data integrity problems in MySQL, such as data truncation upon insertion, by escalating warnings into errors. It is strongly recommended you activate it. See: https://docs.djangoproject.com/en/1.10/ref/databases/#mysql-sql-mode
```

在settings中加入OPTIONS
```python

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "xmooc",
        "USER": 'root',
        "PASSWORD": "root",
        "HOST": "127.0.0.1",
        "OPTIONS":{
            'init_command':"SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }

}

```

3.报错
```shell
The standalone TEMPLATE_* settings were deprecated in Django 1.8 and the TEMPLATES dictionary takes precedence. You must put the values of the following settings into your default TEMPLATES dict:
```
注释TEMPLATE_DIRS选项 选项在 TEMPLATE中使用就行了
```python
# TEMPLATE_DIRS = [
#     os.path.join(BASE_DIR, 'templates')
# ]

```

4.把项目移动到apps里面去,需要在settings.py中加入,把环境移植过去

```python
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

```