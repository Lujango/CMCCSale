# -*- coding:utf-8 -*-
import urllib
import urllib2
import re

__author__ = 'pro'


def getdata(currentpage,pagesize):
    url = 'http://b2b.10086.cn/b2b/main/listVendorNoticeResult.html?noticeBean.noticeType=2'
    values = {
        "page.currentPage":currentpage,
        "page.perPageSize":pagesize,
        "noticeBean.sourceCH":"",
        "noticeBean.source":"",
        "noticeBean.title":"",
        "noticeBean.startDate":"",
        "noticeBean.endDate":"",
    }
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    the_page = response.read()
    return the_page


def dealdata(content):
    pattern = re.compile('onclick="selectResult\(\'(.*?)\'\)">.*?<td style="width:70px;" align="left">(.*?)</td>.*?<td style="'
                         'width:80px;" align="left">.*?</td>.*?<td style="width:280px;" align="left">.*?<a href="#this".*?>(.*?)<'
                         '/a>.*?</td>.*?<td style="width:100px" align="left">(.*?)</td>',re.S)

    items = re.findall(pattern,content)
    print len(items)
    for item in items:
        print item[0],item[1],item[2],item[3]


 # 获取文章详细信息
def getcontent(content):
    pattern = re.compile('<h1>(.*?)</h1>',re.S)
    results = re.findall(pattern,content)
    for result in results:
        print result


#根据文章索引获取内容
def getinfo(index):
    url = 'http://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id='+str(index)
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    the_page = response.read()
    return the_page


if __name__ == "__main__":
    print "begin"
    #content = getdata(1,20)
    #content = content.decode('utf-8')
    #print content
    #dealdata(content)
    getcontent(getinfo(252295))