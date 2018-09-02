#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-09-02 11:05:06
# @Author  : Chloe
# @Link    : http://www.app-echo.com/
# @Version : 1.0.0
# @Intro   : crawl mp3 file from app-echo
# @Todo    : getSource 有点慢，后续加进程

import os, re
import json
import requests
from multiprocessing import Pool

userApi = 'http://www.app-echo.com/api/user/sound-likes'
songApi = 'http://www.app-echo.com/api/sound/info'
rEncode = 'utf-8'
songIds = [] # 歌曲id list
songs = {} # 歌曲名字和源址 dict
headers = {
	'Host': 'www.app-echo.com',
	'Referer': 'http://www.app-echo.com/',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0', 
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
	'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
} # 应对 gzip 压缩信息，也可以后续解压
def getID(userId, num = 1, songList = True):
	'''
	通过user id 得到 user的喜欢歌曲 id, 成 list
	'''
	while songList:
		params = {
			'uid': userId,
			'limit': '20',
			'page': str(num)
		}
		r = requests.get(userApi, headers = headers, params = params)
		r.encoding = rEncode
		songList = json.loads(r.text)['lists']
		for i in songList:
			songIds.append(i['id'])
		num += 1
	print('共有：{}首歌'.format(len(songIds)))
	# print(songIds)

def getSource(songId):
	'''
	通过前面获取的歌曲id得到对应的 {歌名：歌曲地址} dict
	'''
	params = {
		'id': songId,
		'comment': '1'
	}
	r = requests.get(songApi, headers = headers, params = params)
	r.encoding= rEncode
	songMes = json.loads(r.text)

	source = songMes['info']['source']
	name = songMes['info']['name']

	match = re.compile(r'[\\/:*?"<>|]+') #window新建文件时无法写入的特殊字符名
	name = match.sub('-', name)
	songs[name] = source

def getFile(name, url):
	'''
	下载歌曲
	'''
	x = {
	'Accept-Encoding': 'identity;q=1, *;q=0',
	'DNT': '1',
	'Referer': url,
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
	}
	r = requests.get(url, headers = x)
	if (r.status_code == 200):
		with open(name+'.mp3', 'ab+') as file:
			file.write(r.content)
		print('Yes! {}'.format(name))
	elif (r.status_code == 502): 
		getFile(name, url)
	else:
		print('Oops, something wrong!{}{}'.format(name, url))

if __name__ == '__main__':
	userId = input('请输入你的app-echo用户名id\n可登陆账号在好友圈→我喜欢的回声 在链接上的uid就是：')
	getID(userId)
	for i in songIds:
		getSource(i)
	p = Pool(10)
	for name, url in songs.items():
		p.apply_async(getFile, args = (name, url))
	p.close()
	p.join()
	print('Done!')

