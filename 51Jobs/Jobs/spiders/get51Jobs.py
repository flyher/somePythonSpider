#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-08-13 16:16:07
# @Author  : Chloe
# @Link    : http://example.org
# @Version : 1.0.0
# @Intro   : 输入51job网站的搜索链接，会返回搜索的工作信息列表保存为csv文件。

import os
import csv
import time
import random
import scrapy
import requests

# jobAdd 不设置 try, except 会报错，但是salary不会
now = time.strftime("%Y-%m-%d_%H.%M.%S", time.localtime())
with open(now+'.csv', 'a+', newline = '') as f:
	writer = csv.writer(f)
	writer.writerow(['jobCpy','jobTitle','jobMes','jobSal','jobCon','jobAdd','jobUrl'])

url = input('输入51job开始搜索链接：')

class get51Jobs(scrapy.Spider):
	name = 'get51Jobs'

	start_urls = [url]

	def parse(self, response):
		jobList = response.css('#resultList >.el>.t1>span>a::attr(href)')
		next_page = response.css('.p_in ul>li:last-child a::attr(href)').extract_first()

		if next_page is not None:
			yield response.follow(next_page, callback = self.parse)
			time.sleep(random.random()*5)
			print('Page Again!')

		for job in jobList:
			jobUrl = job.extract()
			yield scrapy.Request(jobUrl, callback = self.parsePage)
			# yield response.follow(jobUrl, callback = self.parsePage)

	def parsePage(self, response):

		jobTitle = response.css('div[class = "cn"] > h1::text').extract_first().replace('\t','').replace('\xa0','')
		jobMes = response.css('p[class ="msg ltype"]::text').extract_first().replace('\t','').replace('\xa0','')
		jobSal = response.css('div[class = "cn"] > strong::text').extract_first()
		jobCpy = response.css('p.cname > a[class = "catn"]::attr(title) ').extract_first()
		
		try:
			jobAdd = response.css('div[class = "bmsg inbox"]> .fp::text').extract()[1].replace('\t','').replace('\xa0','')
		except Exception as err:
			print('error raised: ', err)
			jobAdd = 'None'
		#问题点1， 是否可以使用css selector 来获取所有的job detail信息，在一个div 中，但是结构不一，最好的办法是使用xpath div//text()
		Con = response.xpath('*//div[@class="bmsg job_msg inbox"]//text()').extract()
		jobCon = '\n'.join(Con).replace("微信", "").replace("分享", "").replace("邮件", "").replace('\xa0','').replace("\t", "").strip().replace('\r\n\n','')

		with open(now+'.csv', 'a+', newline = '') as f:
			writer = csv.writer(f)
			writer.writerow([jobCpy, jobTitle, jobMes, jobSal, jobCon, jobAdd, response.url])

	

