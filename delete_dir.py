#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#-------------------------------------------------------------------------------
# Name: dossec
#
# file_path ='/Users/Downloads'
#
# file_way = 1：按日期
# file_way = 2：按剩余磁盘空间
#
# 配置文件改为：config.cfg
# .ini用记事本编辑会被加上乱码
#-------------------------------------------------------------------------------

import os
import sys
import time
import datetime
import shutil
import psutil
import configparser
import re

config_path = 'config.cfg'

if not os.path.exists(config_path):
	print('config is not exists!!!')
	os.system('pause')
	sys.exit()

conf = configparser.ConfigParser()

conf.read(config_path)
file_way = conf.get('set', 'file_way')
over_days = int(conf.get('set', 'over_days'))
retain_disk = int(conf.get('set', 'retain_disk'))
file_path = conf.get('set', 'path')

print('文件删除方式：{}'.format(file_way))
print('删除多少天前：{} 天'.format(over_days))
print('磁盘保留空间：{} G'.format(retain_disk))


if not os.path.exists(file_path):
	print('{} is not exists!!!'.format(file_path))
	os.system('pause')
	sys.exit()

new_file_list = {}

def now_time():
	new_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
	return new_time

def delete_info(content=None,update_log = 'delete_info.log'):
	with open('delete_linfo.log','a', encoding='utf-8') as f:
		f.write(now_time() + '\t' + content + '\n')


def follow_day(days, get_file):
	if days > over_days:
		if os.path.isfile(get_file):
			try:
				os.remove(get_file)
			except Exception as e:
				content = '{} 删除失败'.format(e)
				delete_info(content)
				print(content)
			else:
				content = 'remove file：{}'.format(get_file)
				delete_info(content)
				print(content)

		elif os.path.isdir(get_file):
			try:
				shutil.rmtree(get_file)     # 方法一：直接删除整个目录包括非空目录
			except Exception as e:
				content = '{} 删除失败'.format(e)
				delete_info(content)
				print(content)
			else:
				print('remove dir：{}'.format(get_file))

			# get_file_time(get_file)     # 方法二：循环判断，先删除文件
			# if len(os.listdir(get_file)) == 0:   # 如果目录里文件为空，再删除空目录
			#   try:
			#   	os.rmdir('remove dir：{}'.format(get_file))
			# 	except Exception as e:
			# 		print('{} 删除失败'.format(e))
			# 	else:
			# 		print('remove dir：{}'.format(get_file))

	# else:
	# 	print('没有大于 {} 天的文件'.format(over_days))


# follow_day(240, 'E:\\liyong\\Temp\\Tencent\\')

def current_time():
	curr_struct_time = time.localtime(time.time())     # time.struct_time()
	curr_day = time.strftime('%Y-%m-%d', curr_struct_time)  # 2016-07-12
	year, month, day = curr_day.split('-')
	cur_ctime = datetime.datetime(int(year), int(month), int(day))  # 2016-07-12 00:00:00
	return(cur_ctime)


def get_file_time(file_path):
	if len(os.listdir(file_path)) > 0:
		iterms = os.listdir(file_path)
		for eachfile in iterms:
			get_file = os.path.join(file_path, eachfile)
			#get_file = file_path + '/' + eachfile
			try:
				modify_struct_time = time.gmtime(os.stat(get_file).st_mtime)  # time.struct_time()
			except Exception as e:
				content = '获取文件时间错误: {} '.format(e)
				delete_info(content)
				print(content)
			else:
				modify_day = time.strftime("%Y-%m-%d",  modify_struct_time)    # 2016-04-27
				year, month, day = modify_day.split('-')
				file_mtime = datetime.datetime(int(year), int(month), int(day))   # 2016-04-27 00:00:00

				# 现在的日期减去文件的日期，算出文件距离今天的天数。
				days = (current_time() - file_mtime).days  # 76

				# 把获取到的路径和天数作为字典的键值，追加到字典里。
				new_file_list.update({get_file: days})

			if file_way == '1':
				follow_day(days, get_file)

		#print(new_file_list)
		if file_way == '2':

			# 将上面的字典按照值（天数）从小到大，组成新的字典。
			sort_list = ((k, new_file_list[k]) for k in sorted(new_file_list, key=new_file_list.get, reverse=True))
			pre_delete = []

			# 循环新的字典，把路径追加到上面的空列表中
			for k, v in sort_list:
					pre_delete.append(k)
			# print(pre_delete)

			disk_info = psutil.disk_usage(file_path)
			# sdiskusage(total=120108089344, used=65924751360, free=53921193984, percent=54.9)
			free_disk = round(disk_info.free / 1024 / 1024 / 1024, 2)
			total_disk = round(disk_info.total / 1024 / 1024 / 1024, 2)
			print('total_disk: {} G'.format(total_disk))
			print('free_disk: {} G'.format(free_disk))
			print(total_disk - free_disk)

			# 当磁盘剩余空间小于保留值，就一直循环执行
			while free_disk < retain_disk:
				print('free_disk is {} G'.format(free_disk))
				print(pre_delete[0])

				# 列表第0个元素，就是时间最长的文件，先删除，然后再从列表里移出。
				if os.path.isfile(pre_delete[0]):
					print('remove file：{}'.format(pre_delete[0]))
					try:
						os.remove(pre_delete[0])
						pre_delete.pop(0)
					except Exception as e:
						content = '{} 删除失败'.format(e)
						print(content)
					else:
						print('remove file：{}'.format(pre_delete))
				elif os.path.isdir(pre_delete[0]):
					print('remove dir：{}'.format(pre_delete[0]))
					try:
						shutil.rmtree(pre_delete[0])
						pre_delete.pop(0)
					except Exception as e:
						content = '{} 删除失败'.format(e)
						print(content)
					else:
						print('remove dir：{}'.format(pre_delete))
				else:
					os.remove(pre_delete[0])
					pre_delete.pop(0)
	else:
		print('目录 {} 为空！！！'.format(file_path))

if __name__ == '__main__':

	get_file_time(file_path)
	# os.system('pause')
