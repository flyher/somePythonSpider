#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-08-27 15:06:09
# @Author  : Chloe
# @Link    : www.getherproxy.com
# @Version : 1.0.0
# @Intro   : crawl proxy from www.getherproxy.com

import os
import re
import time
import random
import requests
from multiprocessing import Pool, Manager

url = 'http://www.gatherproxy.com/zh/proxylist/country/?c=China' #选取国内的代理，还有其他国家，需要修改keyword
headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
	'Cookie': '_ga=GA1.2.1323676801.1533306185; _lang=zh-CN; _gid=GA1.2.1297245883.1535456823; ASP.NET_SessionId=xyi53v3flmohco40ohs1srdi',
	'Proxy-Connection': 'keep-alive',
	'Referer': 'http://www.gatherproxy.com/zh/proxylist/anonymity/?t=Elite',
	'Upgrade-Insecure-Requests': '1'
}
proxyList = []

def getProxy(num):
	'爬取代理，正则匹配过滤'
	proxies = {
	'http' : 'http://127.0.0.1:1080',
	'https' : 'http://127.0.0.1:1080',
}
	for x in range(1, num+1):
		data = {
			'Country': 'china',
			'PageIdx': str(x),
			'Filter': 'elite',
			'Uptime': '0'
		}		
		r = requests.post(url, headers = headers, proxies = proxies, data = data)
		ips = re.findall("write\('([\d.]+)'\)", r.text)
		ports = re.findall("dep\('([\w]+)'\)", r.text)
		for i, p in zip(ips, ports):
			port = int(p, 16)
			ip = 'http://'+i+':'+str(port)
			proxyList.append(ip)
		print('One page over!')
		time.sleep(random.random()*3)

def validator(proxy, q):
	'连接百度验证代理可用性'
	url = 'http://www.baidu.com'
	try:
		r = requests.get(url, 
			headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}, 
			proxies = {
			'http': proxy,
			'https': proxy,
			}, timeout = 5)
		if (r.status_code == requests.codes.ok):
			print('valid proxy:', proxy)
			q.append(proxy)
		else:
			print('failed:', proxy)
	except Exception as e:
		print('error:', proxy) #如果你想查看具体连接失败原因，可以加上e, error
	time.sleep(0.5)

if __name__ == '__main__':
	num = int(input('输入你想要爬虫的页数，一页有30个代理，总数量约不超过12页：\n'))
	getProxy(num)
	print('爬取到'+str(len(proxyList))+'个代理, 如下：')
	print(proxyList)

	m = Manager()
	q = m.list() #多线程共享list列表
	p = Pool(len(proxyList)//2)
	print('start!')
	for proxy in proxyList:
		p.apply_async(validator, args = (proxy, q))
	p.close()
	p.join()
	print('可用代理如下：')
	print(q)

