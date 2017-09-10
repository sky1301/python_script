#!/usr/bin/python
# -*-coding:utf-8-*-
import StringIO
import json
from xlwt import *

import pycurl
import urllib
'''
爬取QQ音乐分类的所有歌单
'''

def getData(url):#QQ音乐数据接口调用
    ch = pycurl.Curl()
    ch.setopt(ch.URL, url)
    info = StringIO.StringIO()
    ch.setopt(ch.WRITEFUNCTION, info.write)
    ch.setopt(ch.POST, False)
    ch.setopt(ch.SSL_VERIFYPEER, 0)
    ch.setopt(ch.SSL_VERIFYHOST, 2)
    # ch.setopt(ch.HTTPHEADER, ['Accept:application/json;charset=utf-8'])
    ch.setopt(ch.HTTPHEADER, ['Accept: */*'])
    ch.setopt(ch.REFERER, 'https://y.qq.com/portal/playlist.html')
    ch.setopt(ch.HEADER, False)
    ch.perform()
    html = info.getvalue()
    info.close()
    ch.close()
    return html


def getCategory():#获取二级分类
    allCategory = getData(
        'https://c.y.qq.com/splcloud/fcgi-bin/fcg_get_diss_tag_conf.fcg?g_tk=5381&jsonpCallback=getPlaylistTags&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0')
    allCategoryStr = allCategory[16:-1]
    jAllCategoryStr = json.loads(allCategoryStr)
    allCategoryList = jAllCategoryStr['data']['categories'][4]['items']
    return allCategoryList


def getGeDan(categoryId,sid,eid):#获取指定二级分类的指歌单，sid为歌单列表的起始index，eid为歌单列表的结束index.煤气最多只能获取60个歌单
    scategoryId = str(categoryId)
    ssid = str(sid)
    seid = str(eid)
    url = 'https://c.y.qq.com/splcloud/fcgi-bin/fcg_get_diss_by_tag.fcg?rnd=0.26661885451653644&g_tk=5381&jsonpCallback=getPlaylist&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&categoryId='+scategoryId+'&sortId=5&sin='+ssid+'&ein='+seid
    #print url
    data = getData(url)
    strData = data[12:-1]
    jsonData = json.loads(strData)
    dissidData = jsonData['data']
    return dissidData

def getSong(disstid):#获取指定歌单的所有歌曲
    sdisstid = str(disstid)
    url = 'https://c.y.qq.com/qzone/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg?type=1&json=1&utf8=1&onlysong=0&disstid='+sdisstid+'&format=jsonp&g_tk=323522908&jsonpCallback=playlistinfoCallback&loginUin=2633745997&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'
    #print url
    songs = getData(url)
    data = songs[21:-1]
    jSongData = json.loads(data)
    return jSongData


def do():
    f = Workbook()


    allCategory = getCategory()
    try:
        for i in range(len(allCategory)):#循环子分类
            categoryName = allCategory[i]['categoryName']
            categoryId = allCategory[i]['categoryId']
            sid = 0
            eid = 29
            r = 1
            sheet = f.add_sheet(categoryName,cell_overwrite_ok=True)
            sheet.write(0, 0, u'标题')
            sheet.write(0, 1, u'简介')
            sheet.write(0, 2, u'标签')
            sheet.write(0, 3, u'歌曲名')
            sheet.write(0, 4, u'歌手名')
            sheet.write(0, 5, u'专辑名')
            print '正在爬取分类',categoryName
            gnum=0
            while True:#遍历子分类中的每一页歌单

                dissidData = getGeDan(categoryId,sid,eid)
                geDanList = dissidData['list']
                if len(geDanList)<30:#判断是否为最后一页
                    for g in range(len(geDanList)):#遍历每页歌单
                        gnum=gnum+1
                        #print '正在爬取歌单',dissidData['list'][g]['dissname']
                        dissid = dissidData['list'][g]['dissid']
                        jsongdata = getSong(dissid)
                        sheet.write(r, 0, jsongdata['cdlist'][0]['dissname'])
                        sheet.write(r, 1, jsongdata['cdlist'][0]['desc'])
                        tags = ''
                        for t in range(len(jsongdata['cdlist'][0]['tags'])):
                            tags = tags+jsongdata['cdlist'][0]['tags'][t]['name']+'  '
                        sheet.write(r, 2, tags)
                        for s in range(len(jsongdata['cdlist'][0]['songlist'])):#遍历歌单中的歌曲并写入Excel
                            sheet.write(r, 3, jsongdata['cdlist'][0]['songlist'][s]['songname'])
                            sheet.write(r, 4, jsongdata['cdlist'][0]['songlist'][s]['singer'][0]['name'])
                            sheet.write(r, 5, jsongdata['cdlist'][0]['songlist'][s]['albumname'])
                            r = r + 1
                    break
                elif len(geDanList)==30:
                    for g in range(len(geDanList)):#遍历每页歌单
                        gnum = gnum + 1
                        #print r,'正在爬取歌单', dissidData['list'][g]['dissname']
                        dissid = dissidData['list'][g]['dissid']
                        jsongdata = getSong(dissid)
                        sheet.write(r, 0, jsongdata['cdlist'][0]['dissname'])
                        sheet.write(r, 1, jsongdata['cdlist'][0]['desc'])
                        tags = ''
                        for t in range(len(jsongdata['cdlist'][0]['tags'])):
                            tags = tags+jsongdata['cdlist'][0]['tags'][t]['name']+'  '
                        sheet.write(r, 2, tags)
                        for s in range(len(jsongdata['cdlist'][0]['songlist'])):#遍历歌单中的歌曲并写入Excel
                            #print r, '正在爬取歌去',jsongdata['cdlist'][0]['songlist'][s]['songname']
                            sheet.write(r, 3, jsongdata['cdlist'][0]['songlist'][s]['songname'])
                            sheet.write(r, 4, jsongdata['cdlist'][0]['songlist'][s]['singer'][0]['name'])
                            sheet.write(r, 5, jsongdata['cdlist'][0]['songlist'][s]['albumname'])
                            r = r + 1
                sid = sid+30
                eid = eid+30
            print categoryName,'歌单总数=',gnum
        f.save('/Users/sky/Documents/xinqing.xls')
        print 'finish！文件保存在/Users/sky/Documents/xinqing.xl',
    except Exception,e:
        print e.message
        print jsongdata['cdlist'][0]['songlist'][s]['songname']
        f.save('/Users/sky/Documents/xinqing.xls')


if __name__ == "__main__":
    do()

