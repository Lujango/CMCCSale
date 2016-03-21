# -*- coding:utf-8 -*-
import os
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
    return items
    #for item in items:
    #    print item[0],item[1],item[2],item[3]


 # 获取文章详细信息
def getcontent(content):
    str = ''
    pattern = re.compile('<h1>(.*?)</h1>',re.S)
    results = re.findall(pattern,content)
    for result in results:
        str = str+result+"\n"
        print result
    pattern = re.compile('<span style="font-size: 16px;margin-left:16px;">(.*?)</span>     </div>     </td>   </tr></table></div>',re.S)
    results = re.findall(pattern,content)
    for result in results:
        result = result.replace('<br />','\n').replace('&nbsp;','').replace('</span>','').replace('</div>','').replace('<div>','')\
            .replace('</td>','').replace('</tr>','').replace('<td  colspan="3">','').replace('<tr>','')\
            .replace('<span style="font-size: 16px;margin-left:16px;">','\n').replace('<span style="font-size: 16px;font-weight: bold;">','\n')\
            .replace('<span style="font-weight: bold;font-size: 16px;font-weight: bold;">','\n').replace('<span style="font-size: 16px;">','')\
            .replace('<a href="http://b2b.10086.cn/">（http://b2b.10086.cn）</a>','').replace('<span style="font-size:16px;float:right; clear:both;">','\n')
        str = str+result+"\n"
        print result
    return str


#根据文章索引获取内容
def getinfo(index):
    url = 'http://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id='+str(index)
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    the_page = response.read()
    return the_page


def removeall():
    for eachFile in os.listdir('result'):
        print eachFile
        os.remove('result/'+eachFile)


if __name__ == "__main__":
    print "begin"
    #content = getdata(1,20)
    #content = content.decode('utf-8')
    #print content
    #dealdata(content)
    #getcontent(getinfo(252295))
    f=open('result/f.txt','w')
    f.write(getcontent(getinfo(252295)))
    f.close()
