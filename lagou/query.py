#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-08-10 13:56:12
# @Author  : Chloe
# @Link    : http://lagou.com
# @Version : 1.0.0
# @Intro   : query lagoujobs database

import os
import sqlite3

def queryDB(db): #后续查看可以使用
	with sqlite3.connect(db) as conn:
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM Job")
		values = cursor.fetchall()
		for row in values:
			print('{0}\r{1}\r{2}\r{3}\r{4}\r{5}\r\n-----------------------'.format(row[0], row[1], row[2], row[3],row[4], row[5]))

if __name__ == '__main__':
	db = input('input database name: ')
	queryDB('爬虫.db')
