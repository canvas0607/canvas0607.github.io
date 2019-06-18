{{ page.title }}

1.功能

>可以操作浏览器,主要对web进行测试

2.官方文档

>搜索 selenium python api

>http://selenium-python.readthedocs.io/api.html

3.webdiver
>selenium是一个操作浏览器的程序,需要下载特定浏览器的diver驱动.在官方文档中下载diver
下载地址
https://sites.google.com/a/chromium.org/chromedriver/downloads

4.启动selenium

>找到驱动的路径 传递给selenium就可以了

>简单使用:开打下面网址,里面有一个div的列表
每个标签都有onclick属性刷新内容,使用selenium 点击每个h3标签 触发js脚本
```python
from selenium import webdriver

path = 'D:/selenium/chromedriver.exe'
browser = webdriver.Chrome(executable_path=path)

browser.get('http://www.ttmeiju.vip/meiju/House.of.Cards.html')
elems = browser.find_element_by_css_selector(".seasonitem").find_elements_by_xpath('//h3')



for elem in elems:
    if elem.get_attribute('onclick'):
        elem.click()


source = browser.page_source()

browser.close()
```

5.chrmoe不加载图片

```python

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
path = 'D:/selenium/chromedriver.exe'
chrome_options.add_experimental_option("prefs", prefs)
browser = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)
```

