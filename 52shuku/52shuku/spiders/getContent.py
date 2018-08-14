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
	name = 'getContent'

	start_urls = [
	'https://www.52shuku8.com/wenxue/0807/hqjF.html', #52shuku8的链接替换，第一章就可以了
	]

	def parse(self, response):
		name =  response.xpath('*//span[@class="muted"]/a/text()').extract_first()
		content = response.xpath('*//article[@class = "article-content"]/p/text()').extract()
		content = '\n'.join(content)
		
		path = 'E:\\novel\\还没看的\\'+name+'.txt'
		#设定路径下载小说到指定目录
		with open(path, 'a+') as f:
			f.write(content+'\r\n')

		next_page = response.css('.pagination2 ul a::attr(href)').extract()[-2]
		if next_page is not None:
			next_page = response.urljoin(next_page)
			yield scrapy.Request(next_page, callback = self.parse)
			time.sleep(random.random()*5) #设置休息时间
		self.log("one page over!")

