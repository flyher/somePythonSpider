#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-08-12 18:37:51
# @Author  : Chloe
# @Link    : http://example.org
# @Version : 1.0.0
# @Intro   : crawl novel content from website www.52shuku8.com, example: https://www.52shuku8.com/wenxue/0807/hqjF.html

import os
import time
import random
import scrapy

class getContent(scrapy.Spider):
	name = 'get52shuku'
	url = input('输入52shuku8.com 书籍链接, 例如https://www.52shuku8.com/wenxue/0710/hpIk.html ：\n ')
	start_urls = [url]

	def parse(self, response):
		name =  response.xpath('*//span[@class="muted"]/a/text()').extract_first()
		content = response.xpath('*//article[@class = "article-content"]/p/text()').extract()
		content = '\n'.join(content)
		
		path = 'C:\\Users\\Joker\\Downloads\\'+name+'.txt'
		#设定路径下载小说到指定目录
		with open(path, 'ab+') as f:
			f.write((content+'\r\n').encode('utf-8','ignore'))# a+模式不需要encode, 这是为了防止cmd运行 unicode encode error的问题

		next_page = response.css('.pagination2 ul a::attr(href)').extract()[-2]
		if next_page is not None:
			next_page = response.urljoin(next_page)
			yield scrapy.Request(next_page, callback = self.parse)
			time.sleep(random.random()*2) #设置休息时间
		self.log("one page over!")
