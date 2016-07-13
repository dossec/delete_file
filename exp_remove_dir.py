#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#-------------------------------------------------------------------------------
# Name:
#
# Author: Small White
#
# Created: 2014-10-23
#
# Python Tested: 3.4.1
#
# dependency:
# 1)
#
# Modification History:
#-------------------------------------------------------------------------------
import os, sys, datetime
import shutil
import time

def removeFilesBeforeDate(beforeTime, path = "."):
    for eachFile in os.listdir(path):
        f = path + os.sep + eachFile
        lastMTime = os.stat(f).st_mtime
        if lastMTime <= beforeTime:
            try:
                if os.path.isfile(f):
                    os.remove(f)
                elif os.path.isdir(f):
                    shutil.rmtree(f)
                else:
                    os.remove(f)
                print ("删除 {0}, 成功！".format(eachFile))
            except Exception as e:
                print("删除 {0}, 失败！ 错误如下：".format(eachFile))
                print(e)



if __name__=="__main__":
    currTime = time.time()
    deltTime = 3600*24*7 # 7天前
    path = r"F:\\Download"
    removeFilesBeforeDate(currTime - deltTime, path)
#该片段来自于http://www.codesnippet.cn/detail/2410201410791.html
