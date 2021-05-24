# -*- coding: utf-8 -*-
from urllib.request import urlopen
import urllib.request
import urllib.parse #为了获取HTTP response
from bs4 import BeautifulSoup #BS4
import string # 为了去掉空白字符
import time # 防止被杀cookie
import unicodedata # 字符修正
# 在这里放第一个链接
urlx = '链接' #写你想爬的文

def request(url):
    global urlx #引用外面的链接作为全局变量，后面还会取下一个进行循环的


# 使用urllib库提交cookie获取http响应
    headers = {
    'GET https':url,
    'Host':' www.kaixin001.com',
    'Connection':' keep-alive',
    'Upgrade-Insecure-Requests':' 1',
    'User-Agent':' Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'Accept':' application/json, text/javascript, */*; q=0.01',
    'Accept-Language':' zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cookie':' ', #改成自己的cookie，自己浏览器打开网站F12调试，自己找http请求的header
    }
    request = urllib.request.Request(url=url,headers=headers)
    response = urllib.request.urlopen(request)
    contents = response.read()

# 使用BS4获得所有HTMLtag
    bsObj = BeautifulSoup(contents,"html.parser")

# 使用BS4的find函数得到想要的东西：标题、发表时间和博客正文
    title = bsObj.find("b", attrs={"class":"f14"})
    titleT = bsObj.find("b", attrs={"class":"f14"}).get_text() #开心网日记的标题是一个b标签，class属性值是f14
    date = bsObj.find("span", attrs={"class":"c6"})
    dateT = bsObj.find("span", attrs={"class":"c6"}).get_text() #开心网日记的发表时间是一个span标签，class属性值是c6
    text = bsObj.find("div", attrs={"class":"textCont"})
    textT = bsObj.find("div", attrs={"class":"textCont"}).get_text() #开心网日记的正文是一个div标签，class属性值是textCont

  

# 测试输出
    print(title)
    print(dateT)
    # print(text)
    
    
    

# 生成HTML文件。这里直接用file.open()和file.write()了，也可以用jinja2之类的框架生成。
    remove = string.whitespace+string.punctuation
    table = str.maketrans(':','：',remove)

    fileTitle=str(titleT).replace(':','：').replace('''"''','''“''')+'-'+str(dateT).translate(table).replace('发表','')+'.html'

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
    </html>"""%(title.get_text(),date.get_text(),unicodedata.normalize('NFD',text.prettify()))
    f.write(message)
    f.close()
    # webbrowser.open(fileTitle,new = 1)
   

# 定位下一篇博文的URL

    nextUrl=bsObj.find("a",text="下一篇 >").attrs["href"] #下一篇是一个a标签，使用tag对象的attrs属性取href属性的值。开心网的日记系统里，如果到了最后一篇日记，下一篇的链接内容是第一篇日记，所以不用担心从哪篇日记开始爬。
    # print(nextUrl)
    urlx="http://www.kaixin001.com"+nextUrl
    print(urlx)


# 主循环，给爷爬
num=328 #设定要爬多少次。其实也可以写个数组检测重复然后中止的啦，但我懒得弄了。
for a in range(num):
    request(urlx)    
    print('We get '+str(a+1)+' in '+str(num))
    time.sleep(1) # 慢点，慢点。测试过程中出现了没有设置限制爬一半cookie失效了的情况，可能是太快了被搞了。

    