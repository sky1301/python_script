#!/usr/bin/python
import sys,os

def exec_chengge():
    file = open('/home/sky/Downloads/conf.c', 'r+')
    lines = file.readlines()
    if sys.argv[1]=='0':
        lines[16] = 'const char* QINIU_UP_HOST               = "http://up-z2.qiniu.com";\n'
        file = open('/home/sky/Downloads/conf.c', 'w+')
        file.writelines(lines)
        file.close()
        os.system('cocos deploy -p android')
    elif sys.argv[1]=='1':
        lines[16] = 'const char* QINIU_UP_HOST				= "http://upload.qiniu.com";\n'
        file = open('/home/sky/Downloads/conf.c', 'w+')
        file.writelines(lines)
        file.close()
        os.system('lua package_all_androids.lua')
exec_chengge()
