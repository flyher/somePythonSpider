#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-09-04 19:59:09
# @Author  : Chloe
# @Link    : http://example.org
# @Version : 1.0.0
# @Intro   : 加入数据库

import os
import time
import json
import random
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
'Cookie': '_ga=GA1.2.364769393.1530777092; user_trace_token=20180705155132-3bf53b9d-8028-11e8-bea6-525400f775ce; LGUID=20180705155132-3bf53e3c-8028-11e8-bea6-525400f775ce; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; LG_LOGIN_USER_ID=685a780d01d253c359f4f60ad82d580b1d13014dbfb7a94a; JSESSIONID=ABAAABAABEEAAJA59335DAFB632284F12C8954757279F8D; LGSID=20180913153031-e4d8c1ba-b726-11e8-b815-5254005c3644; _putrc=8A2E696B0577F975; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1536572012,1536733021,1536810739,1536823833; login=true; unick=%E6%98%93%E9%9D%92; gate_login_token=30c2dcedc481064f975449faa9c3ebdf7fec3dfb0e515114; TG-TRACK-CODE=index_search; SEARCH_ID=b8e4aa16f2df42fc9948954ae970fa32; hasDeliver=0; index_location_city=%E6%B7%B1%E5%9C%B3; _gat=1; LGRID=20180913161748-80578185-b72d-11e8-95f1-525400f775ce; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1536826670',# 记得修改你的cookie
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

		print('{0}\r{1}\r{2}\r{3}\r{4}\r{5}\r\n-----------------------'.format(jobTitle, jobCompany, jobRequest, jobDetail, jobAddress, basic))
	except Exception as e:
		print('Error!', e)

if __name__ == '__main__':

	# keyword = input('输入搜索关键词：')
	# city = input('输入你想搜索的城市： ') # cmd运行会有unicode encode error, cmd 字符集不同，无法编码一些字符，建议换环境运行
	getId(keyword = 'python实习', city = '深圳', first = 'true', i =1, results = True)
	p = Pool(10)#可以自行修改进程数量
	for i in idList:
		p.apply_async(getDetail, args = (i,))
	p.close()
	p.join()
