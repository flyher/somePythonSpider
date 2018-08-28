# Some Python Spider
从互联网爬取一些实用或者有趣的信息

## Get Code

 ``` 
 git clone https://github.com/Chloe-Y/somePythonSpider.git
 ```
------
## Jobs
- [Lagou.com](#Lagou.com) 
- [51job.com](#51Job.com)

## Proxy Pool
* [xicidaili.com](xicidaili.com)
* [gatherproxy.com](gatherproxy.com)

## Books info
* [douban](douban) 

## Picture
* [unplash.com](unplash.com)

## Novel
* [sto.cc](sto.cc)
* [52shuku.com](52shuku.com)

------
## Lagou.com
输入工作关键词爬取拉勾网工作信息并保存到 mysqlite3 数据库，默认深圳地区

### *setps*
```
cd lagou
python run lagou.py 
# suggest run in sublime, cmd will cause unicode encode error and ignore job title & job company 
# you can choose change keyword in file or input the keyword
# and later, you can query job detail with sqlite3 database
```
preview
![lagou](https://github.com/Chloe-Y/somePythonSpider/blob/master/demo/lagou.png)

query lagoujobs database
![query](https://github.com/Chloe-Y/somePythonSpider/blob/master/demo/query.png)
 

## 51Job.com
通过51job链接爬取页面的工作详情，并且保存到csv文件中

preview
 ![51jobs](https://github.com/Chloe-Y/somePythonSpider/blob/master/demo/51jobs.png)

### *steps*
 ```
 cd 51Jobs
 scrapy crawl get51Jobs
 # search jobs in 51jobs.com and copy url
 # run the scrapy
 # paste 51job url, get jobs detail and save into csv file
 ```
 在51job.com 查询工作信息，复制链接，爬虫运行后黏贴链接
 ![search](https://github.com/Chloe-Y/somePythonSpider/blob/master/demo/search.gif)
 爬虫下来的csv文件，需要整理一下
 ![csv file](https://github.com/Chloe-Y/somePythonSpider/blob/master/demo/data.gif)
 
 ------
## xicidaili.com
爬取西刺代理的高匿代理，再使用线程池连接百度验证代理可用性

### *steps*
 ```
 cd proxy
 python xici.py
 input page number you want to crawl (100 proxies/page)
 ```
preview, i used pillow to merge this two pictures
![xici](https://github.com/Chloe-Y/somePythonSpider/blob/master/demo/getxici.png)

## gatherproxy.com
爬取 gatherproxy的国内代理，再使用线程池连接百度验证代理可用性

### *steps*
 ```
 cd proxy
 python getProxy.py
 ```
 preview
![gatherProxy](https://github.com/Chloe-Y/somePythonSpider/blob/master/demo/getproxy.png)
 
 ------
## douban
:books: 输入标签或者关键词爬取豆瓣的图书信息，ID, 书名，作者，简介等
 
### *steps* 
 ```
 cd douban
 python doubanBook.py
 # enter books keyword
 # enter the number of books you want to save
 ```
 query doubanbooks database
 ![querybooks](https://github.com/Chloe-Y/somePythonSpider/blob/master/demo/querybooks.png)
 
 ------
## sto.cc
爬取sto.cc网站的小说，需要使用代理连接
 
### *steps* 
```
cd book
python stocc.py
# paste sto.cc website novel link
```

## 52shuku.com
使用scrapy 爬虫 52shuku.com的小说，保存成txt文件

### *steps*
```
cd book/52shuku
scrapy crawl get52shuku
# paste novel link and start download novel to txt file
