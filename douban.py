# -*- coding: utf-8 -*-
from urllib.request import urlopen
import urllib.request
import urllib.parse #为了获取HTTP response
from bs4 import BeautifulSoup #BS4
import string # 为了去掉空白字符
import unicodedata # 字符修正
import re
# 在这里放链接
url = '' #写你想爬的人 https://www.douban.com/people/xxx/notes 这样
COOKIE = ''

def request(urlx):
    global url #引用外面的链接作为全局变量，后面还会取下一个进行循环的
    global boolean
    global COOKIE
# 使用urllib库提交cookie获取http响应
    headers = {
    'GET https':urlx,
    'Host':' www.douban.com',
    'Connection':' keep-alive',
    'Upgrade-Insecure-Requests':' 1',
    'User-Agent':' Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'Accept':' application/json, text/javascript, */*; q=0.01',
    'Accept-Language':' zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cookie':COOKIE, #改成自己的cookie，自己浏览器打开网站F12调试，自己找http请求的header
    }
    request = urllib.request.Request(url=urlx,headers=headers)
    response = urllib.request.urlopen(request)
    contents = response.read()

# 使用BS4获得所有HTMLtag
    bsObj = BeautifulSoup(contents,"html.parser")

# 使用BS4的find函数获取当前页面的所有日记链接
    article = bsObj.find("div", attrs={"class":"article"})
    titleSet = article.findAll("h3")
    # print(titleSet)
    for title in titleSet:
        titleText = title.findAll("a",attrs={"class":"j a_unfolder_n"})
        for link in titleText:
            noteUrl = str(link.attrs["href"])
            print(noteUrl)
            requestSinglePage(noteUrl)
    next = bsObj.find("a",text="后页>")
    if next==None:
        print("结束了")
        boolean=1
    else:
        url = str(next.attrs["href"]).replace("&type=note","")
        print(url)

def requestSinglePage(urly):
    global COOKIE
    headers = {
        'GET https':urly,
        'Host':' www.douban.com',
        'Connection':' keep-alive',
        'Upgrade-Insecure-Requests':' 1',
        'User-Agent':' Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'Accept':' application/json, text/javascript, */*; q=0.01',
        'Accept-Language':' zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cookie':COOKIE, #改成自己的cookie，自己浏览器打开网站F12调试，自己找http请求的header
    }
    request = urllib.request.Request(url=urly,headers=headers)
    response = urllib.request.urlopen(request)
    contents = response.read()
    # 使用BS4获得所有HTMLtag
    bsObj = BeautifulSoup(contents,"html.parser")

# 使用BS4的find函数得到想要的东西：标题、发表时间和博客正文

    title = bsObj.find("h1").get_text()
    date = bsObj.find("span", attrs={"class":"pub-date"})
    dateT = bsObj.find("span", attrs={"class":"pub-date"}).get_text()
    text = bsObj.find("div", attrs={"id":"link-report"})
    # textT = bsObj.find("div", attrs={"class":"textCont"}).get_text()

# 测试输出
    print(title)
    print(dateT)

    # 生成HTML文件。这里直接用file.open()和file.write()了，也可以用jinja2之类的框架生成。
    remove = string.whitespace+string.punctuation # 去掉日期的标点符号
    table = str.maketrans(':','：',remove)

    fileTitle=str(title)+'-'+str(dateT).translate(table)+'.html'

    print(fileTitle) #测试输出

    f = open(fileTitle,'w',encoding="utf-8") #注意用utf-8编码写入，不然会因为一些旧博文采用的gbk编码不兼容而出问题。

    # 写入message
    message = """
    <html>
    <head></head>
    <body>
    <h1>%s</h1>
    <b>%s</b>
    <br></br>
    %s
    </body>
    </html>"""%(title,dateT,unicodedata.normalize('NFD',text.prettify()))
    f.write(message)
    f.close()

# 主循环，给爷爬

boolean=0
while(boolean==0):
    a=1
    request(url)
    print('We finished page '+str(a)+' .')
    a+=1

    