# some python spider
crawl book, picture and something else interesting from internet :see_no_evil:  :notebook_with_decorative_cover:

## install

 ``` 
 git clone https://github.com/ChloeandShawn/somePythonSpider.git
 ```
------
 ## 51Job.com spider :office:
 crawl 51job.com job detail and sava data to csv file
 
 :boom: preview
 ![51jobs](https://github.com/ChloeandShawn/somePythonSpider/raw/master/demo/51jobs.png)

 ### *steps*
 1. search jobs in 51jobs.com and copy url
 2. run the scrapy
 3. paste 51job url
  
 ```
 cd Jobs
 scrapy crawl get51Jobs
 ```
 ![search](https://github.com/ChloeandShawn/somePythonScrapy/blob/master/demo/search.gif)
 ![csv file](https://github.com/ChloeandShawn/somePythonScrapy/blob/master/demo/data.gif)
 
 ------
 ## lagou.com jobs' detail spider
 input job keywords to crawl jobs' detail and save to sqlite3 database, default search in ShenZhen city
 
 :boom: preview 
 ![lagou](https://github.com/ChloeandShawn/somePythonSpider/blob/master/demo/lagou.png)
 
 ### *setps*
 ```
 1. cd lagouJobSpider
 2. python run lagou.py 
 # suggest run in sublime, cmd will cause unicode encode error and ignore job title & job company 
 # you can choose change keyword in file or input the keyword
 # and later, you can query job detail with sqlite3 database
 ```
 query lagoujobs database
 ![query](https://github.com/ChloeandShawn/somePythonSpider/blob/master/demo/query.png)
 
 ------
 ## get proxy spider
 crawl proxy from xicidaili.com & gatherproxy.com
 
 ### *gatherproxy.com spider*
 ```
 cd proxy
 python getProxy.py
 ```
 ![gatherProxy](https://github.com/ChloeandShawn/somePythonSpider/blob/master/demo/getproxy.png)
 
 ### *xicidaili.com spider*
 ```
 cd proxy
 python xici.py
 input the page number (100 proxies/page)
 ```
 :boom: preview, i used pillow to merge this two pictures
 ![xici](https://github.com/ChloeandShawn/somePythonSpider/blob/master/demo/getxici.png)
 
 ------
 ## douban books spider :books:
 crawl douban books info and save data to mysqlite3 database
 
 ### *steps*
 1. run douban spider
 2. enter books keyword
 3. enter the number of books you want to save
 
 ```
 cd douban
 python doubanBook.py
 ```
 ![douban](https://github.com/ChloeandShawn/somePythonScrapy/blob/master/demo/douban.gif)
 
 query doubanbooks database
 ![querybooks](https://github.com/ChloeandShawn/somePythonSpider/raw/master/demo/querybooks.png)
