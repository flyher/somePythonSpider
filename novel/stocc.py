#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-07-21 21:56:58
# @Author  : Chloe
# @Link    : https://www.sto.cc/book-165256-1.html
# @Version : 1.0

import os,re
import requests
import time
from bs4 import BeautifulSoup
try:
	import urllib3.contrib.pyopenssl
	urllib3.contrib.pyopenssl.inject_into_urllib3()
except ImportError:
	print('error') #这个是为了防止requests连接https抛出的ssl error

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
'referer': 'https://www.sto.cc/sbn.aspx?c=0',
'upgrade-insecure-requests': '1'
}
proxies = {
	'http' : 'http://127.0.0.1:1080',
	'https' : 'http://127.0.0.1:1080',
}#sto.cc 这个网站国内的好像都上不去，需要借助海外的代理，如果你自己能翻墙的话就能通过本地IP的端口号用代理连接
url = input('请输入链接，例如：https://www.sto.cc/book-165256-1.html \n')
r = requests.get(url, headers = headers, proxies = proxies, allow_redirects = False)
#防止重定向是最后一个章节如果超出的话会默认重定向到最后一个章节的url
soup = BeautifulSoup(r.text, "lxml")
name = soup.select('.bookbox h1')[0].string
contents = soup.select('.bookbox #BookContent')[0].get_text('\n','br/')#新办法获取一个div里面的全部的文字，如果文字是使用br/分行的话，超酷
with open(name+'.txt','a+') as f:
		f.write(contents)
urls = soup.select('.paginator > a')[-1]['href']#获取url list里面的最后一个，因为页面分析最末页的a链接是最后一个
last = re.search('-(\d+).html', urls).group(1)#通过最末页的url获取最后章节数
for i in range(2,int(last)+1):#因为小说名字在前面的第一章已经获取过了，所以需要从2开始
	try:#是为了无措运行
		basic = url[0:-6] +str(i)+'.html'
		s = requests.Session()#跨请求保持参数，感觉是为了保持cookie之类的吧
		r = s.get(basic, headers = headers, proxies = proxies, allow_redirects = False, timeout = 5)
		soup = BeautifulSoup(r.text, "lxml")
		contents = soup.select('.bookbox #BookContent')[0].get_text('\n','br/')
		with open(name+'.txt','a+') as f:#a+是读写模式，ab+是二进制的读写模式，如果需要加\r\n, 需要后面加一个encode('utf-8')
			f.write(contents+'\r\n')
		time.sleep(3)
	except Exception as e:#报error
		print(basic, e)
print('Done!')

#原先设想过三个获取最后章节的办法
#method 1
#直接查看页面最后一章的链接，然后for i in range()循环的去，最省事的办法，自动化不高
# for i in range(1,73):
# 	basic = 'https://www.sto.cc/book-173692-'+i+'.html'
# 	r = requests.get(basic, headers = headers, proxies = proxies, allow_redirects = False)
# 	soup = BeautifulSoup(r.text, "lxml")
# 	contents = soup.select('.bookbox #BookContent')[0].get_text('\n','br/')
# 	with open(name+'.txt','ab+') as f:
# 		f.write((contents+'\r\n').encoding('utf-8'))

#method 2
#链接的章节数一直加的去，然后while r.status_code == requests.codes.ok
#就说明这个章节是存在的，但是注意要去除重定向，因为一般超出的话会自动定向到最后一章节
# 	basic = 'https://www.sto.cc/book-173692-'+i+'.html'
# 	i += 1

#method 3
#就是这个里面的，先解析页面，然后查到最后一章节的url,然后for i in range
#感觉这网站做的挺不错的，学到很多，例如proxies，session, 'ab+', ssl errors 之类的

#感想之一就是网络要好，vps也要稳定