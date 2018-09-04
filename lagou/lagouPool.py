#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-09-04 19:59:09
# @Author  : Chloe
# @Link    : http://example.org
# @Version : 1.0.0
# @Intro   : 加入了多进程，还需要加入多进程数据库

import os
import time
import json
import random
import sqlite3
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool

url = 'https://www.lagou.com/jobs/positionAjax.json'
headers = {
'Connection': 'keep-alive',
'Host': 'www.lagou.com',
'Origin': 'https://www.lagou.com',
'Referer': 'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%20%E5%AE%9E%E4%B9%A0?labelWords=&fromSearch=true&suginput=',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
'Cookie': '_ga=GA1.2.364769393.1530777092; user_trace_token=20180705155132-3bf53b9d-8028-11e8-bea6-525400f775ce; LGUID=20180705155132-3bf53e3c-8028-11e8-bea6-525400f775ce; index_location_city=%E6%B7%B1%E5%9C%B3; _gid=GA1.2.1815605485.1534689804; JSESSIONID=ABAAABAAAGGABCBF488C0FBE25BB912F6A1E0C2196ECDC5; _gat=1; LGSID=20180821111035-c5a3da3b-a4ef-11e8-ab1e-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1534693355,1534734769,1534752872,1534821036; LGRID=20180821111048-cd8d8879-a4ef-11e8-ab1e-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1534821049; TG-TRACK-CODE=index_search; SEARCH_ID=548744b8e4c34140a52037caa9fa5681',
# 记得修改你的cookie
'X-Anit-Forge-Code': '0',
'X-Anit-Forge-Token': 'None',
'X-Requested-With': 'XMLHttpRequest'
}
resultSize = 0
idList = []
def getId(keyword, city, first, i, results):
	while results:
		data = {
		'first' : first,
		'pn' : str(i),
		'kd' : keyword
		}
		params = {
		'city': city,
		'needAddtionalResult': 'false'		
		}
		global resultSize
		r = requests.post(url, headers = headers, data = data, params = params)
		jobs = json.loads(r.text)
		resultSize += jobs['content']['positionResult']['resultSize']
		results = jobs['content']['positionResult']['result']
		for result in results:
			idList.append(result['positionId'])
		fisrt = 'false'
		i += 1
		time.sleep(random.random()*3)
	print('共有 {} 条职业信息！'.format(resultSize))
	# print(idList)

def getDetail(jobId):
	basic = 'https://www.lagou.com/jobs/{0}.html'.format(jobId)
	r = requests.get(basic, headers = headers)
	r.encoding = 'utf-8'
	soup = BeautifulSoup(r.text, 'lxml')
	try:
		jobTitle = soup.select('div.job-name > span.name')[0].get_text()
		jobCompany = soup.select('div.job-name > div.company')[0].get_text()
		jobRequest = soup.select('div.position-content-l > dd.job_request > p')[0].get_text().replace('\n','')
		jobDetail = soup.select('#job_detail > dd.job_bt > div')[0].get_text()
		jobAddress = soup.select('#job_detail dd.job-address > input')[2]['value']

		#insertDB(jobTitle, jobCompany, jobRequest, jobDetail, jobAddress, basic)
		print('{0}\r{1}\r{2}\r{3}\r{4}\r{5}\r\n-----------------------'.format(jobTitle, jobCompany, jobRequest, jobDetail, jobAddress, basic))
	except Exception as e:
		print('Error!', e)

def creatDB(db):
	try:
		cursor.execute("CREATE TABLE Job (titel TEXT, company TEXT, request TEXT, detail TEXT, address Text, url TEXT PRIMARY KEY )")
		print('creat table job successfully!')
	except:
		cursor.execute("DROP TABLE IF EXISTS Job")
		cursor.execute("CREATE TABLE Job (titel TEXT, company TEXT, request TEXT, detail TEXT, address Text, url TEXT PRIMARY KEY )")
		print('drop table and then creat again, successfully!')

def insertDB(jobTitle, jobCompany, jobRequest, jobDetail, jobAddress, jobUrl):
	try:
		cursor.execute("INSERT INTO Job VALUES (?, ?, ?, ?, ?, ?)", (jobTitle, jobCompany, jobRequest, jobDetail, jobAddress, jobUrl))
	except Exception as err:
		print('insert failed: '+ err)

if __name__ == '__main__':
	# now = time.strftime('%Y-%m-%d_%H.%M.%S', time.localtime())
	# db = now+'.db'
	# conn = sqlite3.connect(db)
	# cursor = conn.cursor()
	# creatDB(db)

	# keyword = input('输入搜索关键词：')
	# city = input('输入你想搜索的城市： ')
	getId(keyword = 'python爬虫', city = '广州', first = 'true', i =1, results = True)
	p = Pool(10)#可以自行修改进程数量
	for i in idList:
		p.apply_async(getDetail, args = (i,))
	p.close()
	p.join()

	# cursor.close()
	# conn.commit()
	# conn.close()
