#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-08-15 19:53:42
# @Author  : Chloe
# @Link    : http://example.org
# @Version : 1.0.0
# @Intro   : crawl proxy from www.xicidaili.com

import os,re
import requests
from bs4 import BeautifulSoup

headers = {
 	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}
basic = 'http://www.xicidaili.com/nn/' #nn是高匿代理的分类

proxyList = []
valid = []

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
		print('爬取到的代理如下：\n')
		print(proxyList)

def validator():
	'用代理连接百度验证代理可用性'
	url = 'https://www.baidu.com'
	for proxy in proxyList:
		proxies = {
		'http': proxy,
		'https': proxy,
		}
		try:
			r = requests.get(url, headers = headers, proxies = proxies, timeout = 5)
			print('valid proxy: '+proxy)
			valid.append(proxy)
		except Exception as e:
			print('error:', proxy)
	print('可用代理如下：\n')
	print(valid)

if __name__ == '__main__':
	num = int(input('高匿代理，一页100个代理，输入你想要爬取的页数：'))
	getXiCi(num)
	validator()








