# python-crawler-exercise
 python爬虫练手项目

我本科有个很幽默风趣的量子力学老师，他说了很多批话，跟个公知似的。

他的很多文章都放在了开心网（kaixin001.com）上。我突发奇想，趁着这个傻逼过气网站还没关，我先爬一波，留个纪念。就看了Ryan Mitchell的《Python网络数据采集》这本书，研究了一天，爬了下来。

所以用了BeautifulSoup4，请先安装。

```powershell
pip install beautifulsoup4
```

哎呀不要问为什么没有settings.py，好麻烦，随手写的小玩具，懒得优化了能用就行。可能以后心情好了弄个窗口界面方便操作吧。

## 开心网日记爬取

kaixin001.py

### 使用

登录开心网，浏览器F12看http请求的header，获取自己的cookie。

填写cookie，要爬的日记的url，要爬的总次数。走你。

之后会生成HTML文件，格式是<:title>-\<YYYYMMDDHHMMSS\>

## 豆瓣日记爬取

douban.py

### 使用

登录豆瓣，浏览器F12看http请求的header，获取自己的cookie。

填写变量COOKIE，要爬的日记页的url。走你。

之后会生成HTML文件，格式是<:title>-\<YYYYMMDDHHMMSS\>
