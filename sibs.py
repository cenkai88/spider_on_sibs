# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 14:09:53 2015

@author: cenkai
"""
import time
import urllib
import os
from bs4 import BeautifulSoup
import sys
import xlwt
from itertools import groupby
import requests

reload(sys)
sys.setdefaultencoding('utf8')
session = None

#获取所有学生的学号
def query_all():
    global session
    numbers=[]
    #先爬博士的学号
    s = requests.session()
    login_data = {"C6": "ON", "T5": "2014", "T6": "博士".decode('utf-8').encode('gbk')}
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10162",
        'Host': "sedu.sibs.ac.cn",
        'Referer': "http://sedu.sibs.ac.cn/class/"
        }
    r = s.post('http://sedu.sibs.ac.cn/class/class.asp', data=login_data, headers=header)
    soup = BeautifulSoup(r.content)
    for n in range(1, len(soup.div.contents[2])/2):
        numbers.append(soup.div.contents[2].contents[2*n+1].contents[1].text.strip())
    #再爬硕士的
    s = requests.session()
    login_data = {"C6": "ON", "T5": "2014", "T6": "硕士".decode('utf-8').encode('gbk')}
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10162",
        'Host': "sedu.sibs.ac.cn",
        'Referer': "http://sedu.sibs.ac.cn/class/"
        }
    r = s.post('http://sedu.sibs.ac.cn/class/class.asp', data=login_data, headers=header)
    soup = BeautifulSoup(r.content)
    for n in range(1, len(soup.div.contents[2])/2):
        numbers.append(soup.div.contents[2].contents[2*n+1].contents[1].text.strip())
    return numbers

#爬取数据
def parser(self):
    s2 = requests.session()
    a = requests.adapters.HTTPAdapter(pool_connections = 3, pool_maxsize=5)
    s2.mount('http://', a)
    header = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10162",
    'Host': "sedu.sibs.ac.c",
    'Referer': "http://sedu.sibs.ac.cn/class/",'Connection': "close"
    }
    r2 = s2.get(self.url, headers=header)
    self.soup=BeautifulSoup(r2.content)
    s2.close()
    r2.close()

#需要处理的一些字段：    
def politic2(p):
    x1 = [u'中共党员', 'u党员']
    y1 = [u'共青团员', u'团员']
    z1 = [u'群众']
    if p in x1:
        return u'党员'
    elif p in y1:
        return u'团员'
    elif p in z1:
        return u'群众'
    else:
            return u'预备党员'

#2012级数据不够细，需剔除
def city(c,n):
    n = n[:4]
    if n == '2012':
        return u'未知'
    elif u'县' in c:
        return u'农村学生'
    else:              
        return u'城市学生'

#将年纪转为入学年，默认二年级转博，这里区分不出外博了        
def year2(y,e):
    if e==u'博士':
        return str(int(y)-2)
    else:
        return y
        
    def emailprovider(self):
        return 

def level(g):
    x1 = [u'北京大学',u'清华大学',u'浙江大学',u'复旦大学',u'上海交通大学',u'南京大学',u'中国科学技术大学',u'哈尔滨工业大学',u'西安交通大学']
    y1 = [u'北京大学',u'清华大学',u'北京师范大学',u'浙江大学',u'上海交通大学',u'复旦大学',u'南京大学',u'西安交通大学',u'中国人民大学',u'哈尔滨工业大学',u'北京理工大学',u'中国科学技术大学',u'南开大学',u'天津大学',u'华南理工大学',u'中山大学',u'山东大学',u'华中科技大学',u'吉林大学',u'厦门大学',u'武汉大学',u'东南大学',u'中国海洋大学',u'湖南大学',u'中南大学',u'西北工业大学',u'大连理工大学',u'重庆大学',u'四川大学',u'电子科技大学',u'北京航空航天大学',u'兰州大学',u'东北大学',u'同济大学',u'中国农业大学',u'国防科学技术大学',u'西北农林科技大学',u'中央民族大学',u'华东师范大学']
    z1 = [u'清华大学',u'北京大学',u'中国人民大学',u'北京工业大学',u'北京理工大学',u'北京航空航天大学',u'北京化工大学',u'北京邮电大学',u'对外经济贸易大学',u'中国传媒大学',u'中央民族大学',u'中国矿业大学(北京)',u'中央财经大学',u'中国政法大学',u'中国石油大学(北京)',u'中央音乐学院',u'北京体育大学',u'北京外国语大学',u'北京交通大学',u'北京科技大学',u'北京林业大学',u'中国农业大学',u'北京中医药大学',u'华北电力大学(北京)',u'北京师范大学',u'中国地质大学(北京)',u'复旦大学',u'华东师范大学',u'上海外国语大学',u'上海大学同济大学',u'华东理工大学',u'东华大学',u'上海财经大学',u'上海交通大学',u'南开大学',u'天津大学',u'天津医科大学',u'',u'重庆大学',u'西南大学',u'华北电力大学(保定)',u'河北工业大学',u'太原理工大学',u'内蒙古大学',u'大连理工大学',u'东北大学',u'辽宁大学',u'大连海事大学',u'吉林大学',u'东北师范大学',u'延边大学',u'东北农业大学',u'东北林业大学',u'哈尔滨工业大学',u'哈尔滨工程大学',u'南京大学',u'东南大学',u'苏州大学',u'河海大学',u'中国药科大学',u'中国矿业大学(徐州)',u'南京师范大学',u'南京理工大学',u'南京航空航天大学',u'江南大学',u'南京农业大学',u'浙江大学',u'安徽大学',u'合肥工业大学',u'中国科学技术大学',u'厦门大学',u'福州大学',u'南昌大学',u'山东大学',u'中国海洋大学',u'中国石油大学(华东)',u'郑州大学',u'武汉大学',u'华中科技大学',u'中国地质大学(武汉)',u'华中师范大学',u'华中农业大学',u'中南财经政法大学',u'武汉理工大学',u'湖南大学',u'中南大学',u'湖南师范大学',u'中山大学',u'暨南大学',u'华南理工大学',u'华南师范大学',u'广西大学',u'四川大学',u'西南交通大学',u'电子科技大学',u'西南财经大学',u'四川农业大学',u'云南大学',u'贵州大学',u'西北大学',u'西安交通大学',u'西北工业大学',u'陕西师范大学',u'西北农林科大',u'西安电子科技大学',u'长安大学',u'兰州大学',u'新疆大学',u'石河子大学',u'海南大学',u'宁夏大学',u'青海大学',u'西藏大学',u'第二军医大学',u'第四军医大学',u'国防科学技术大学']
    u1 = [u'北京大学',u'中国人民大学',u'清华大学',u'北京交通大学',u'北京工业大学',u'北京航空航天大学',u'北京理工大学',u'北京科技大学',u'北京化工大学',u'北京邮电大学',u'中国农业大学',u'北京林业大学',u'首都医科大学',u'北京中医药大学',u'北京外国语大学',u'北京第二外国语学院',u'北京语言大学',u'中国传媒大学',u'中央财经大学',u'对外经济贸易大学',u'北京体育大学',u'中央民族大学',u'中国政法大学',u'华北电力大学(北京)',u'中国矿业大学(北京)',u'中国石油大学(北京)',u'中国地质大学(北京)',u'北京大学医学部',u'北京邮电大学(宏福校区)',u'南开大学',u'天津大学',u'天津医科大学',u'天津中医药大学',u'河北工业大学',u'华北电力大学(保定)',u'河北医科大学',u'燕山大学',u'东北大学秦皇岛分校',u'内蒙古大学',u'辽宁大学',u'大连理工大学',u'东北大学',u'大连海事大学',u'沈阳农业大学',u'中国医科大学',u'大连医科大学',u'东北财经大学',u'吉林大学',u'延边大学',u'东北师范大学',u'哈尔滨工业大学',u'哈尔滨工程大学',u'东北石油大学',u'东北农业大学',u'东北林业大学',u'哈尔滨医科大学',u'黑龙江中医药大学',u'复旦大学',u'同济大学',u'上海交通大学',u'华东理工大学',u'东华大学',u'上海中医药大学',u'上海外国语大学',u'上海财经大学',u'华东政法大学',u'上海大学',u'上海交通大学医学院',u'南京大学',u'苏州大学',u'东南大学',u'南京航空航天大学',u'南京理工大学',u'中国矿业大学',u'河海大学',u'江南大学',u'江苏大学',u'南京信息工程大学',u'南京农业大学',u'中国药科大学',u'南京师范大学',u'中国人民大学(苏州校区)',u'浙江大学',u'安徽大学',u'中国科学技术大学',u'合肥工业大学',u'合肥工业大学(宣城校区)',u'厦门大学',u'福州大学',u'南昌大学',u'山东大学',u'中国海洋大学',u'中国石油大学(华东)',u'哈尔滨工业大学(威海)',u'山东大学威海分校',u'郑州大学',u'武汉大学',u'华中科技大学',u'中国地质大学(武汉)',u'武汉理工大学',u'华中农业大学',u'华中师范大学',u'中南财经政法大学',u'湘潭大学',u'湖南大学',u'中南大学',u'湖南师范大学',u'中山大学',u'暨南大学',u'华南理工大学',u'华南农业大学',u'广州中医药大学',u'华南师范大学',u'广东外语外贸大学',u'南方医科大学',u'广西大学',u'广西医科大学',u'重庆大学',u'西南大学',u'西南政法大学',u'四川大学',u'西南交通大学',u'电子科技大学',u'四川农业大学',u'成都中医药大学',u'西南财经大学',u'云南大学',u'西北大学',u'西安交通大学',u'西北工业大学',u'西安电子科技大学',u'陕西科技大学',u'长安大学',u'西北农林科技大学',u'陕西师范大学',u'兰州大学',u'山西大学',u'太原理工大学',u'山西农业大学',u'山西医科大学',u'山西财经大学']
    if g in x1:
        return u'九校联盟'
    elif g in y1:
        return u'985高校'
    elif g in z1:
        return u'211高校'
    elif g in u1:
        return u'普通A类一本'
    else:
        return u'非一本高校'

#初始化时若有本地文件读取本地信息（目录设为stu_info所在目录，不需进入），否则从网络爬取，效率很低
class Student:
    soup=None
    def __init__(self, number):
        self.url = 'http://sedu.sibs.ac.cn/class/particular.asp?id='+str(number)
        self.number = number
        try:
            file_name = number + '.txt'
            f = open (os.path.join(os.path.join(os.getcwd(), "stu_info"), file_name), 'r')
            lines = f.readlines()
            self.name = lines[1][10:].strip().decode('utf-8')
            self.innumber = lines[2][13:].strip()
            self.gender = lines[3][10:].strip().decode('utf-8')
            self.unit = lines[4][10:].strip().decode('utf-8')
            self.tutor = lines[5][10:].strip().decode('utf-8')
            self.hometown = lines[6][10:].strip().decode('utf-8')
            self.major = lines[7][10:].strip().decode('utf-8')
            self.politic = lines[8][16:].strip().decode('utf-8')
            self.edu = lines[9][16:].strip().decode('utf-8')
            self.graduate = lines[10][17:].strip().decode('utf-8')
            self.year = lines[11][11:].strip()
            self.phd = lines[12][17:].strip().decode('utf-8')
            self.email = lines[13][11:].strip()
            self.details = ''.join(lines)
            self.politic2 = politic2(self.politic)
            self.familyname = self.name[:1]
            self.province = self.hometown[:2]
            self.emailprovider = self.email[self.email.find('@')+1:self.email.find('.')]
            self.level = level(self.graduate)
            self.city = city(self.hometown, self.number)
            self.year2 = year2(self.year, self.edu)
        except IOError:
            print '从网络获取中...'
            self.parser()
            self.name = self.soup.contents[0].contents[3].contents[4].contents[2].contents[1].contents[3].text.strip()
            self.innumber = self.soup.contents[0].contents[3].contents[4].contents[2].contents[1].contents[11].text.strip()
            self.gender = self.soup.contents[0].contents[3].contents[4].contents[2].contents[3].contents[3].text.strip()
            self.unit = self.soup.contents[0].contents[3].contents[4].contents[2].contents[3].contents[7].text.strip()
            self.tutor = self.soup.contents[0].contents[3].contents[4].contents[2].contents[3].contents[11].text.strip()
            self.hometown = self.soup.contents[0].contents[3].contents[4].contents[2].contents[5].contents[7].text.strip()
            self.major = self.soup.contents[0].contents[3].contents[4].contents[2].contents[5].contents[11].text.strip()
            self.politic = self.soup.contents[0].contents[3].contents[4].contents[2].contents[7].contents[3].text.strip()
            self.edu = self.soup.contents[0].contents[3].contents[4].contents[2].contents[7].contents[7].text.strip()
            self.graduate = self.soup.contents[0].contents[3].contents[4].contents[2].contents[7].contents[11].text.strip()
            self.year = self.soup.contents[0].contents[3].contents[4].contents[2].contents[9].contents[3].text.strip()
            self.phd = self.soup.contents[0].contents[3].contents[4].contents[2].contents[9].contents[7].text.strip()
            self.email = self.soup.contents[0].contents[3].contents[4].contents[2].contents[9].contents[11].text.strip()
            self.politic2 = politic2(self.politic)
            self.familyname = self.name[:1]
            self.province = self.hometown[:2]
            self.emailprovider = self.email[self.email.find('@')+1:self.email.find('.')]
            self.level = level(self.graduate)
            self.city = city(self.hometown, self.number)
            self.year2 = year2(self.year, self.edu)
            details = '-' * 50 + '\n'
            note=[u'姓名', u'内部号', u'性别', u'单位', u'导师', u'籍贯', u'专业', u'政治面貌', u'在学层次', u'毕业院校', u'年级', u'是否硕博', u'邮箱']
            note2=[self.name, self.innumber, self.gender, self.unit, self.tutor, self.hometown, self.major, self.politic, self.edu, self.graduate, self.year, self.phd, self.email]
            for i in range (1,14):
                details +=  str(i) + '. ' + note[i-1] + ':' + note2[i-1] + '\n'
            self.details = details
            if self.details != 0:
                if not os.path.isdir(os.path.join(os.path.join(os.getcwd(), "stu_info"))):
                    os.makedirs(os.path.join(os.path.join(os.getcwd(), "stu_info")))
                file_name = self.number + ".txt"
                print file_name
                f = open(os.path.join(os.path.join(os.getcwd(), "stu_info"), file_name), "wt")
                f.write(self.details)
                f.close()
                
    #输入学号查询其他信息,仅在屏幕打印
    def show_info(self):
        print self.details
    
    #下载图片      
    def get_img(self):
        if not os.path.isdir(os.path.join(os.path.join(os.getcwd(), "imgs"))):
            os.makedirs(os.path.join(os.path.join(os.getcwd(), "imgs")))
        imgurl="http://sedu.sibs.ac.cn/class/image/" + self.innumber + self.name.encode('utf-8') + ".jpg"
        file_name = self.number + self.name + ".jpg"
        u = urllib.urlopen(imgurl)
        data = u.read()
        f = open(file_name, 'wb')               
        f.write(data)
        f.close() 
        print '成功抓取' + self.name.encode('utf-8') + '的照片'


#group类，传入一系列学号，从本地提取信息，默认为全体学生学号
class Group:
    def __init__(self, numbers = query_all()):
        numbers = list(set(numbers))
        self.all = []
        for number in numbers:
            self.all.append(Student(number))
    
    def save_as_xls(self,filename):
        wb = xlwt.Workbook()
        ws = wb.add_sheet('Sheet 1')
        for i in range(len(self.all)):
            stu = self.all[i]
            ws.write(i+1, 0, stu.number)
            ws.write(i+1, 1, stu.name)
            ws.write(i+1, 2, stu.innumber)
            ws.write(i+1, 3, stu.gender)
            ws.write(i+1, 4, stu.unit)
            ws.write(i+1, 5, stu.tutor)
            ws.write(i+1, 6, stu.hometown)
            ws.write(i+1, 7, stu.major)
            ws.write(i+1, 8, stu.politic)
            ws.write(i+1, 9, stu.edu)
            ws.write(i+1, 10, stu.graduate)
            ws.write(i+1, 11, stu.year)
            ws.write(i+1, 12, stu.phd)
            ws.write(i+1, 13, stu.email)    
        wb.save( filename + '.xls') 
    
    #features为学号的list, percent为是否按百分比显示，默认关闭
    def count(self, features,percent=False):
        totaltag = []
        for stu in self.all:
            di = {'gender':stu.gender, 'unit':stu.unit, 'tutor':stu.tutor, 'hometown':stu.hometown, 'major':stu.major, 'edu':stu.edu, 'politic':stu.politic2, 'graduate':stu.graduate, 'year':stu.year, 'emailprovider':stu.emailprovider, 'phd':stu.phd, 'familyname':stu.familyname, 'province':stu.province, 'level':stu.level, 'city': stu.city, 'year2': stu.year2}
            stu_f = [di[feature] for feature in features]
            tag = []
            for feature in stu_f:
                tag.append(feature)
            totaltag.append(tag)
        if percent:
            if len(features)>1:
                results = []
                for k, r in groupby(sorted(totaltag),lambda x:x[0]):
                    nt = 0
                    tmp = []
                    for r1 in r:
                        nt+=1
                        tmp.append(''.join(r1))
                        tmps = set(tmp)
                    for item in tmps:
                        dec = '%.3f' % (tmp.count(item) / float (nt) * 100)
                        results.append(str(item) + u'占' + str(dec) + '%')
                results = sorted(results)
                for result in results:
                    print result
            else:
                results = []
                totaltag = [''.join(t) for t in totaltag]
                total = set(totaltag)
                nt = len(totaltag)
                for item in total:
                    dec = '%.3f' % (totaltag.count(item) / float(nt) * 100)
                    results.append(str(item) + u'占' + str(dec) + '%')            
                results = sorted(results)
                for result in results:
                    print result
        else:
            totaltag = [''.join(t) for t in totaltag]
            total = set(totaltag)
            results = []
            for item in total:
                results.append(str(item) + str(totaltag.count(item)) + u'人')
            results = sorted(results)
            for result in results:
                print result  
    
    #固定一个字段，统计其他字段
    def count2(self, cond, value, features, percent=False):
        tocount=[]    
        for stu in self.all:
            di = {'gender':stu.gender, 'unit':stu.unit, 'tutor':stu.tutor, 'hometown':stu.hometown, 'major':stu.major, 'edu':stu.edu, 'politic':stu.politic2, 'graduate':stu.graduate, 'year':stu.year, 'emailprovider':stu.emailprovider, 'phd':stu.phd, 'familyname':stu.familyname, 'province':stu.province, 'level':stu.level, 'city': stu.city, 'year2': stu.year2}
            con = di[cond]
            if con == value:
                tocount.append(stu.number)
        toc = Group(tocount)
        toc.count(features, percent)
        
    #下载图片存到imgs文件夹
    def get_all_imgs(self):
        if not os.path.isdir(os.path.join(os.path.join(os.getcwd(), "imgs"))):
            os.makedirs(os.path.join(os.path.join(os.getcwd(), "imgs")))
        i = 0
        while i < len(self.all):
            try:
                self.all[i].get_img()
                i+=1
            except IndexError:
                print 'resting 200s'
                time.sleep(20)