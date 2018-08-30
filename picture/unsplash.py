#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-08-29 15:22:26
# @Author  : Chloe
# @Link    : http://example.org
# @Version : 1.0.0
# @Intro   : 

import os
import json
import random
import requests
from subprocess import call

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Authorization': 'Client-ID fa60305aa82e74134cabc7093ef54c8e2c370c47e73152f72371c828daedfcd7', #网上据说官方无限制的access key, 可以去unsplash developer 那里申请
    'Accept-Version': 'v1'
}

idm = r'E:\app\Idm\idman_lv\IDMan.exe' #这是IDM的路径

def getPhoto(keyword, page, types):
    for i in range(1, page+1):
        url = 'https://api.unsplash.com/search/photos?page={}&query={}&per_page=30'.format(str(i), keyword)
        r = requests.get(url, headers = headers)
        data = json.loads(r.text)
        for i in data['results']:
            href = i['urls'][types]
            name = i['description']
            if name == None:
                name = str(random.randint(1,99))
            else:
                name = i['description']
            call([idm, '/d', href, '/f', 'pictures\\'+name + '.jpg', '/n', '/a'])

if __name__ == '__main__':
    keyword = input('enter the keyword to search photos: ')
    page = int(input('input the page number you want to crawl, 30 photos/page: '))
    types = input('photo type: raw, full, regular, small, thumb, choose one of them: ')
    style = ['raw', 'full', 'regular', 'small', 'thumb']
    
    if types in style:
        getPhoto(keyword, page, types)
        print('Done! already added to IDM download queue!')
    else:
        types = input('please input the photo type one of them: raw, full, regular, small, thumb \n ')


