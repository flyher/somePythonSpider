# somePythonScrapy
crawl book, novel, pictures and something else from internet :see_no_evil:  :notebook_with_decorative_cover:

## install

 ``` 
 git clone https://github.com/ChloeandShawn/somePythonScrapy.git
 ```

 ## using Jobs spider
 crawl 51job.com job detail and sava data to csv file
 
 ```
 cd Jobs
 scrapy crawl get51Jobs
 ```
 1. search jobs in 51jobs.com and get url
 2. run the scrapy
 3. paste 51job url
 
 ![search](https://github.com/ChloeandShawn/somePythonScrapy/blob/master/demo/search.gif)
 ![csv file](https://github.com/ChloeandShawn/somePythonScrapy/blob/master/demo/data.gif)
 
 ## Using douban spider
 crawl douban books info and save data to mysqlite3 database
 1. run douban spider
 2. enter the keyword to search books
 3. enter the number of books you want to save
 
 ```
 cd douban
 python doubanBook.py
 ```
 ![douban](https://github.com/ChloeandShawn/somePythonScrapy/blob/master/demo/douban.gif)
 
