#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-08-21 19:22:01
# @Author  : Chloe
# @Link    : http://example.org
# @Version : 1.0.0
# @Intro   : crawl proxy from www.getherproxy.com

import os
import re
import pprint
import requests
from multiprocessing import Pool

url = 'http://www.gatherproxy.com/zh/proxylist/country/?c=China' #选取国内的代理，还有其他的keyword
headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
	'Cookie': '_ga=GA1.2.1323676801.1533306185; _gid=GA1.2.1840628868.1534850289; _lang=zh-CN; ASP.NET_SessionId=l02z0s33f32vgh0jaaf4sj3d; _gat=1',
	'Proxy-Connection': 'keep-alive',
	'Referer': 'http://www.gatherproxy.com/zh/proxylist/anonymity/?t=Elite',
	'Upgrade-Insecure-Requests': '1'
}
proxies = {
	'http' : 'http://127.0.0.1:1080',
	'https' : 'http://127.0.0.1:1080',
}
valid = []
proxyList = []

def getProxy():
	r = requests.get(url, headers = headers, proxies = proxies)
	ips = re.findall('"PROXY_IP":"([\d.]+)"', r.text)
	ports = re.findall('"PROXY_PORT":"([\w]+)"', r.text)

	for i, p in zip(ips, ports):
		p = int(p,16)
		ip = 'http://'+i+':'+str(p)
		proxyList.append(ip)
	print('爬取到的代理如下： \n')
	print(proxyList)
# getProxy()

def validator(proxy):
	url = 'http://www.baidu.com'
	try:
		r = requests.get(url, 
			headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}, 
			proxies = {
			'http': proxy,
			'https': proxy,
			}, timeout = 5)
		if (r.status_code == requests.codes.ok):
			valid.append(proxy)
			print('valid proxy:', proxy)
		else:
			print('failed:', proxy)
	except Exception as e:
		print('error:', proxy)



if __name__ == '__main__':
	getProxy()
	# validator()
	p = Pool(4)
	for proxy in proxyList:
		p.apply_async(validator, args = (proxy,))
	p.close()
	p.join()
	# print('可用代理如下：\n')
	# print(valid)
	print('over!')