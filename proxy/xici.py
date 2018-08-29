#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-08-15 19:53:42
# @Author  : Chloe
# @Link    : http://example.org
# @Version : 1.0.0
# @Intro   : crawl proxy from www.xicidaili.com

import os,re,time
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool, Manager

headers = {
 	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}
basic = 'http://www.xicidaili.com/nn/' #nn是高匿代理的分类
proxyList = []

def getXiCi(num):
	'爬取西刺代理'
	for i in range(1, num+1):
		url = basic+str(i)
		#print(url)
		r  = requests.get(url, headers = headers)
		soup = BeautifulSoup(r.text, "lxml")
		ips = soup.select('#ip_list > tr > td:nth-of-type(2)')
		ports = soup.select('#ip_list > tr > td:nth-of-type(3)')	
		for ip, port in zip(ips, ports):
			proxy = 'http://'+ip.text+':'+port.string
			proxyList.append(proxy)
	print('爬取到的代理如下：')
	print(proxyList)

def validator(proxy, q):
	'用代理连接百度验证代理可用性'
	url = 'https://www.baidu.com'
	proxies = {
	'http': proxy,
	'https': proxy,
	}
	try:
		r = requests.get(url, headers = headers, proxies = proxies, timeout = 10)
		if (r.status_code == requests.codes.ok):
			print('valid proxy: '+proxy)
			q.append(proxy)
	except Exception as e:
		print('error:', proxy,e)
	time.sleep(0.5)

if __name__ == '__main__':
	num = int(input('高匿代理，一页100个代理，输入你想要爬取的页数：'))
	getXiCi(num)
	
	m = Manager()
	q = m.list()
	p = Pool(len(proxyList)//2)
	for proxy in proxyList:
		p.apply_async(validator, args = (proxy, q))
	p.close()
	p.join()
	print('可用代理如下：')
	print(q)








