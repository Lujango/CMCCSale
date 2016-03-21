# coding:utf-8
import os
import urllib
import urllib2
import re
import datetime
from html2text import html2text
import nltk as nltk

__author__ = 'pro'


def getdata(currentpage, pagesize):
    url = 'http://b2b.10086.cn/b2b/main/listVendorNoticeResult.html?noticeBean.noticeType=2'
    values = {
        "page.currentPage": currentpage,
        "page.perPageSize": pagesize,
        "noticeBean.sourceCH": "",
        "noticeBean.source": "",
        "noticeBean.title": "",
        "noticeBean.startDate": "",
        "noticeBean.endDate": "",
    }
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    the_page = response.read()
    return the_page


def dealdata(content):
    pattern = re.compile(
        'onclick="selectResult\(\'(.*?)\'\)">.*?<td style="width:70px;" align="left">(.*?)</td>.*?<td style="'
        'width:80px;" align="left">.*?</td>.*?<td style="width:280px;" align="left">.*?<a href="#this".*?>(.*?)<'
        '/a>.*?</td>.*?<td style="width:100px" align="left">(.*?)</td>', re.S)

    items = re.findall(pattern, content)
    print "获取".decode('utf-8').encode('gbk'), len(items)
    return items


    # 获取文章详细信息


def getcontent(content):
    str = ''
    pattern = re.compile('<h1>(.*?)</h1>', re.S)
    results = re.findall(pattern, content)
    for result in results:
        str = str + result + "\n"
    pattern = re.compile('<td colspan="2">(.*?)</td>.*?</tr>', re.S)
    results = re.findall(pattern, content)
    for result in results:
        result = result.replace('<br />', '\n').replace('&nbsp;', '').replace('</span>', '').replace('</div>',
                                                                                                     '').replace(
            '<div>', '') \
            .replace('</td>', '').replace('</tr>', '').replace('<td  colspan="3">', '').replace('<tr>', '') \
            .replace('<span style="font-size: 16px;margin-left:16px;">', '\n').replace(
            '<span style="font-size: 16px;font-weight: bold;">', '\n') \
            .replace('<span style="font-weight: bold;font-size: 16px;font-weight: bold;">', '\n').replace(
            '<span style="font-size: 16px;">', '') \
            .replace('<a href="http://b2b.10086.cn/">（http://b2b.10086.cn）</a>', '').replace(
            '<span style="font-size:16px;float:right; clear:both;">', '\n')
        str = str + result + "\n"
    return str


# 根据文章索引获取内容
def getinfo(index):
    url = 'http://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=' + str(index)
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    the_page = response.read()
    return the_page


def removeall():
    if not os.path.isdir("result"):
        os.mkdir("result")
    for eachFile in os.listdir('result'):
        print eachFile
        os.remove('result/' + eachFile)


def savefile(title, content):
    title = re.sub(':|\\\|\/|\*|\?|"|<|>|\|',"", title)
    f = open('result/' + title + '.txt', 'w')
    f.write(content.encode('utf-8'))
    f.close()


if __name__ == "__main__":
    print "开始获取数据......".decode('utf-8').encode('gbk')
    pagenum = raw_input("请输入时间!(例如：2016-3-21)".decode('utf-8').encode('gbk'))
    print pagenum
    mytime = datetime.datetime.strptime(pagenum, '%Y-%m-%d')
    removeall()
    errornum = 0
    for i in range(1, 30):
        content = getdata(i, 20)
        content = content.decode('utf-8')
        mytime1 = datetime.datetime.strptime(pagenum, '%Y-%m-%d')
        for item in dealdata(content):
            if u"四川" in item[1] or u"重庆" in item[1] or u"物联网" in item[1] or u"基地" in item[1] or u"终端" in item[1]:
                try:
                    savefile(item[2], html2text(getinfo(item[0]).decode('utf-8')))
                    print "已写入".decode('utf-8').encode('gbk'), item[0], item[1], item[2], item[3]
                except IOError, e:
                    errornum += 1
                    print '写入错误'.decode('utf-8').encode('gbk'), e, item[3]
            mytime1 = datetime.datetime.strptime(item[3], '%Y-%m-%d')
        if mytime > mytime1:
            print '共'.decode('utf-8').encode('gbk'), i, '页'.decode('utf-8').encode('gbk')
            break
    print '错误'.decode('utf-8').encode('gbk'), errornum, '个'.decode('utf-8').encode("gbk")
    # print html2text(getinfo(252083).decode('utf-8'))
