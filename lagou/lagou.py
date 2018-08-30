#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-08-21 12:02:10
# @Author  : Chloe
# @Link    : http://www.lagou.com
# @Version : 1.0.0
# @Intro   : post搜索关键词和页码，返回发布职业信息id, 套入basic 工作信息链接，收集工作信息，保存至数据库，后续考虑结合代码池，为了不显示爬取太频繁还是太慢了
# @Update  : 添加多线程，添加代理池

import os
import time
import json
import random
import sqlite3
import requests
from bs4 import BeautifulSoup
#from multiprocessing import Pool

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

def existDB():
	try:
		cursor.close()
		conn.commit()
		conn.close()
	except Exception as e:
		print('exist DB failed: '+e)

def queryDB(db): #后续查看可以使用
	with sqlite3.connect(db) as conn:
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM Job")
		values = cursor.fetchall()
		for row in values:
			print('{0}\r{1}\r{2}\r{3}\r{4}\r{5}\r\n-----------------------'.format(row[0], row[1], row[2], row[3],row[4], row[5]))

url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E6%B7%B1%E5%9C%B3&needAddtionalResult=false' #默认深圳地区搜索，如果不是，修改'city=([%\w]+)'里面的Unicode地址编码
headers = {
'Connection': 'keep-alive',
'Host': 'www.lagou.com',
'Origin': 'https://www.lagou.com',
'Referer': 'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%20%E5%AE%9E%E4%B9%A0?labelWords=&fromSearch=true&suginput=',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
'Cookie': '_ga=GA1.2.364769393.1530777092; user_trace_token=20180705155132-3bf53b9d-8028-11e8-bea6-525400f775ce; LGUID=20180705155132-3bf53e3c-8028-11e8-bea6-525400f775ce; index_location_city=%E6%B7%B1%E5%9C%B3; _gid=GA1.2.1815605485.1534689804; JSESSIONID=ABAAABAAAGGABCBF488C0FBE25BB912F6A1E0C2196ECDC5; _gat=1; LGSID=20180821111035-c5a3da3b-a4ef-11e8-ab1e-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1534693355,1534734769,1534752872,1534821036; LGRID=20180821111048-cd8d8879-a4ef-11e8-ab1e-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1534821049; TG-TRACK-CODE=index_search; SEARCH_ID=548744b8e4c34140a52037caa9fa5681',
'X-Anit-Forge-Code': '0',
'X-Anit-Forge-Token': 'None',
'X-Requested-With': 'XMLHttpRequest'
}
#也许应该弄个cookie input? 需要更换
def getLaGouJobs(keyword, first, i, results):

	'''
	post搜索关键词和页码，返回发布职业信息id, 套入basic 工作信息链接，
	收集工作信息，保存至数据库
	'''
	while results:

		data = {
		'first': first,
		'pn': str(i), 
		'kd': keyword
		}
		r = requests.post(url, headers = headers, data = data)
		print('拉钩网请求信息',data)

		jobs = json.loads(r.text) #把 json 换成 jobs就ok了，OMG！！！
		results = jobs['content']['positionResult']['result']
		resultSize = jobs['content']['positionResult']['resultSize']

		print('请求页工作信息数量：', resultSize, '\r\n')

		for result in results:
			try:
				basic = 'https://www.lagou.com/jobs/{0}.html'.format(result['positionId'])
				r = requests.get(basic, headers = headers)
				r.encoding = 'utf-8'
				time.sleep(random.random()*3) #休息时间，感觉有点慢，后续结合代理池的好
				soup = BeautifulSoup(r.text, "lxml")

				jobTitle = soup.select('div.job-name > span.name')[0].get_text()
				jobCompany = soup.select('div.job-name > div.company')[0].get_text()
				jobRequest = soup.select('div.position-content-l > dd.job_request > p')[0].get_text().replace('\n','')
				jobDetail = soup.select('#job_detail > dd.job_bt > div')[0].get_text()
				jobAddress = soup.select('#job_detail dd.job-address > input')[2]['value']
				jobUrl = basic	
				
				print(('{0}\r{1}\r{2}\r{3}\r{4}\r{5}\r\n-----------------------'.format(jobTitle, jobCompany, jobRequest, jobDetail, jobAddress, jobUrl).encode('GBK','ignore').decode('GBK')))
				#encode 又decode 是因为 gbk无法转换一些Unicode中的字符，所以需要ignore，再decode，cmd中运行的话job title 和 job company 都会被ignore掉，建议使用sublime或其他环境来运行
				insertDB(jobTitle, jobCompany, jobRequest, jobDetail, jobAddress, jobUrl)
			except Exception as e:
				pass
				#print('获取工作信息页面错误：{}'.format(basic), e, '\n', r.text)
		print('one page over!')
		i += 1
		first = 'false'
		time.sleep(random.random()*5)

if __name__ == '__main__':

	now = time.strftime('%Y-%m-%d_%H.%M.%S', time.localtime())
	db = now+'.db'
	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	creatDB(db)
	print('注意，cmd中运行会忽略掉job title & job company\n因为Unicode类型的字符中，包含了一些无法转换为GBK编码的一些字符\n建议在sublime或其他环境中运行\r\n')
	
	keyword = 'python 开发'
	#keyword = input('input keyword: ')
	getLaGouJobs(keyword, first = 'true', i = 1, results = True)
	existDB()
	#queryDB()
