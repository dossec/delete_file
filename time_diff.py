#create by chenhuajie 2007-11-24

import os, sys,datetime,time
from stat  import *

path='c:\\test\\'
path2='c:\\test\\'
filelist=[]
filelist=os.listdir(path)
for i in range(len(filelist)):
        t1 = time.gmtime(os.stat(path+filelist[i])[ST_MTIME])  #get file's mofidy time
        t11 =  time.strftime('%Y-%m-%d',t1)
        year,month,day=t11.split('-')
        t111= datetime.datetime(int(year),int(month),int(day))        
        t2 = time.gmtime()
        t22 =  time.strftime('%Y-%m-%d',t2)
        year,month,day=t22.split('-')
        t222= datetime.datetime(int(year),int(month),int(day))        
        days =  (t222-t111).days
        if days>5 :  # if over 5 days then remove file
                try:
                        os.remove(path+filelist[i])
                        log=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"  remove "+path+filelist[i]+"  success \n"
                except:
                        log=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"  remove "+path+filelist[i]+"  fail \n"                
                fTemp=open(path2+"remove_file.log", 'a')        
                fTemp.write(log)