# -*- coding: utf-8 -*-
"""
Created on Mon Jul 06 22:35:28 2015

@author: cenkai
"""
#import re
#import time
#import json
#import platform
#import html2text
#import gc
import urllib
import urllib2
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




class Student:
    url=None
    soup=None
    def __init__(self, number):
        self.url = 'http://sedu.sibs.ac.cn/class/particular.asp?id='+str(number)
        self.number = number
        
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
        
#输入学号查询其他信息,仅在屏幕打印
    def get_info(self):
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
        details = '-' * 50 + '\n'
        note=[u'姓名', u'内部号', u'性别', u'单位', u'导师', u'籍贯', u'专业', u'政治面貌', u'在学层次', u'毕业院校', u'年级', u'是否硕博', u'邮箱']
        note2=[self.name, self.innumber, self.gender, self.unit, self.tutor, self.hometown, self.major, self.politic, self.edu, self.graduate, self.year, self.phd, self.email]
        for i in range (1,14):
            details +=  str(i) + '. ' + note[i-1] + ':' + note2[i-1] + '\n'
        return details
                         
    def get_name(self):
        self.parser()        
        return self.soup.contents[0].contents[3].contents[4].contents[2].contents[1].contents[3].text.strip()
        
    def get_innumber(self):
        self.parser()        
        return self.soup.contents[0].contents[3].contents[4].contents[2].contents[1].contents[11].text.strip()
        
    def get_gender(self):
        self.parser()        
        return self.soup.contents[0].contents[3].contents[4].contents[2].contents[3].contents[3].text.strip()
        
    def get_unit(self):
        self.parser()        
        return self.soup.contents[0].contents[3].contents[4].contents[2].contents[3].contents[7].text.strip()        
        
    def get_tutor(self):
        self.parser()        
        return self.soup.contents[0].contents[3].contents[4].contents[2].contents[3].contents[11].text.strip()
        
    def get_hometown(self):
        self.parser()        
        return self.soup.contents[0].contents[3].contents[4].contents[2].contents[5].contents[7].text.strip()
        
    def get_major(self):
        self.parser()        
        return self.soup.contents[0].contents[3].contents[4].contents[2].contents[5].contents[11].text.strip()
        
    def get_politic(self):
        self.parser()        
        return self.soup.contents[0].contents[3].contents[4].contents[2].contents[7].contents[3].text.strip()
        
    def get_edu(self):
        self.parser()        
        return self.soup.contents[0].contents[3].contents[4].contents[2].contents[7].contents[7].text.strip()
        
    def get_graduate(self):
        self.parser()        
        return self.soup.contents[0].contents[3].contents[4].contents[2].contents[7].contents[11].text.strip()
        
    def get_year(self):
        self.parser()        
        return self.soup.contents[0].contents[3].contents[4].contents[2].contents[9].contents[3].text.strip()
        
    def get_phd(self):
        self.parser()        
        return self.soup.contents[0].contents[3].contents[4].contents[2].contents[9].contents[7].text.strip()        
        
    def get_email(self):
        self.parser()        
        return self.soup.contents[0].contents[3].contents[4].contents[2].contents[9].contents[11].text.strip()      
        
    def to_txt(self):
        tmp = self.get_info()
        if tmp != 0:
            if not os.path.isdir(os.path.join(os.path.join(os.getcwd(), "stu_info"))):
                os.makedirs(os.path.join(os.path.join(os.getcwd(), "stu_info")))
            file_name = self.number + ".txt"
            print file_name
            f = open(os.path.join(os.path.join(os.getcwd(), "stu_info"), file_name), "wt")
            f.write(tmp)
            f.close()
#下载图片，每个学生需要访问两次
    def get_img(self):
        self.parser()
        if not os.path.isdir(os.path.join(os.path.join(os.getcwd(), "imgs"))):
            os.makedirs(os.path.join(os.path.join(os.getcwd(), "imgs")))
        imgurl="http://sedu.sibs.ac.cn/class/image/" + self.soup.contents[0].contents[3].contents[4].contents[2].contents[1].contents[11].text.strip() + self.soup.contents[0].contents[3].contents[4].contents[2].contents[1].contents[3].text.strip() + ".jpg"
        file_name = self.number + ".jpg"
        u = urllib.urlopen(imgurl)
        data = u.read()
        f = open(file_name, 'wb')               
        f.write(data)
        f.close() 
            
#需要处理的一些字段：    
    def politic2(self):
        p = self.politic
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
    def city(self):
        c = self.hometown
        y = self.number[:4]
        if y == '2012':
            return u'未知'
        elif u'县' in c:
            return u'农村学生'
        else:              
            return u'城市学生'
#将年纪转为入学年，默认二年级转博，这里区分不出外博了        
    def year2(self):
        y = self.year
        e = self.edu
        if e==u'博士':
            return str(int(y)-2)
        else:
            return y
        
    def familyname(self):
        return self.name[:1]
    
    def province(self):
        return self.hometown[:3]
        
    def emailprovider(self):
        return self.email[self.email.find('@')+1:self.email.find('.')]
        
#九校联盟为0, 985为1, 211为2, 普通一本3， 非一本为4
    def level(self):
        g = self.graduate
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


#group类，传入一系列学号，从本地提取信息
class Group:
    def __init__(self, numbers):
        numbers = list(set(numbers))
        self.numbers = numbers
        self.number_of_stu = len (numbers)
        self.all = []
        for number in numbers:
            tmp = Student(number)
            file_name = number + '.txt'
            f = open (file_name, 'r')
            lines = f.readlines()
            tmp.number = number
            tmp.name = lines[1][10:].strip().decode('utf-8')
            tmp.innumber = lines[2][13:].strip()
            tmp.gender = lines[3][10:].strip().decode('utf-8')
            tmp.unit = lines[4][10:].strip().decode('utf-8')
            tmp.tutor = lines[5][10:].strip().decode('utf-8')
            tmp.hometown = lines[6][10:].strip().decode('utf-8')
            tmp.major = lines[7][10:].strip().decode('utf-8')
            tmp.politic = lines[8][16:].strip().decode('utf-8')
            tmp.politic2 = tmp.politic2()
            tmp.edu = lines[9][16:].strip().decode('utf-8')
            tmp.graduate = lines[10][17:].strip().decode('utf-8')
            tmp.year = lines[11][11:].strip()
            tmp.phd = lines[12][17:].strip().decode('utf-8')
            tmp.email = lines[13][11:].strip()
            tmp.familyname = tmp.familyname()
            tmp.province = tmp.province()
            tmp.emailprovider = tmp.emailprovider()
            tmp.level = tmp.level()
            tmp.city = tmp.city()
            tmp.year2 = tmp.year2()
            self.all.append(tmp)


#查询所有学生信息，保存成txt，img
def get_all_info():
#    numbers = query_all()
    i = 0
    while i < len(numbers):
        try:
            stu=Student(numbers[i])
            stu.to_txt()            
            time.sleep(1)
            i+=1
        except IndexError:
            print 'resting 200s'
            time.sleep(20)
        except AttributeError:
            print 'resting 300s'
            time.sleep(30)

#txt整理为xls
def txt_to_xls(filename):
    files = os.listdir(".")
    number =[]
    name = []
    innumber = []
    gender= []
    unit =[]
    tutor =[]
    hometown =[]
    major =[]
    politic=[]
    edu =[]
    graduate =[]
    year =[]
    phd =[]
    email=[]    
    for fname in files:
        if fname[-3:] == 'txt':         
            number.append(fname[:15])        
            f = open(fname, 'r')
            lines = f.readlines()
            name.append(lines[1][10:].strip().decode('utf-8'))
            innumber.append(lines[2][13:].strip())
            gender.append(lines[3][10:].strip().decode('utf-8'))
            unit.append(lines[4][10:].strip().decode('utf-8'))
            tutor.append(lines[5][10:].strip().decode('utf-8'))
            hometown.append(lines[6][10:].strip().decode('utf-8'))
            major.append(lines[7][10:].strip().decode('utf-8'))
            politic.append(lines[8][16:].strip().decode('utf-8'))
            edu.append(lines[9][16:].strip().decode('utf-8'))
            graduate.append(lines[10][17:].strip().decode('utf-8'))
            year.append(lines[11][11:].strip())
            phd.append(lines[12][17:].strip().decode('utf-8'))
            email.append(lines[13][11:].strip())
            f.close()
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Sheet 1')
    for i in range(len(number)):
        ws.write(i, 0, number[i])
        ws.write(i, 1, name[i])
        ws.write(i, 2, innumber[i])
        ws.write(i, 3, gender[i])
        ws.write(i, 4, unit[i])
        ws.write(i, 5, tutor[i])
        ws.write(i, 6, hometown[i])
        ws.write(i, 7, major[i])
        ws.write(i, 8, politic[i])
        ws.write(i, 9, edu[i])
        ws.write(i, 10, graduate[i])
        ws.write(i, 11, year[i])
        ws.write(i, 12, phd[i])
        ws.write(i, 13, email[i])    
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

#在已经得到学生信息的情况下下载图片，每个学生少访问一次。需要先进入stu_info文件夹
def get_img_from_local():
    if not os.path.isdir(os.path.join(os.path.join(os.getcwd(), "imgs"))):
        os.makedirs(os.path.join(os.path.join(os.getcwd(), "imgs")))
    files =  os.listdir(".")
    i = 0
    while i < len(files):
        file_name = files[i][:15] + '.jpg'
        f = open( files[i] , "r" )
        lines = f.readlines()
        imgurl = "http://sedu.sibs.ac.cn/class/image/" + lines[2][13:].strip() + lines[1][10:].strip() + ".jpg"
        f.close()
        try:
            u = urllib.urlopen(imgurl)
            data = u.read()
            f2 = open(os.path.join(os.path.join(os.getcwd(), "imgs"), file_name), "wb")
            f2.write(data)
            print imgurl
            f2.close()
            i+=1
        except IndexError:
            print 'resting 200s'
            time.sleep(20)
        
#固定一个字段，统计其他字段
def count2(self, cond, value, features, percent=False):
    tocount=[]    
    for stu in self.all:
        di = {'gender':stu.gender, 'unit':stu.unit, 'tutor':stu.tutor, 'hometown':stu.hometown, 'major':stu.major, 'edu':stu.edu, 'politic':stu.politic2, 'graduate':stu.graduate, 'year':stu.year, 'emailprovider':stu.emailprovider, 'phd':stu.phd, 'familyname':stu.familyname, 'province':stu.province, 'level':stu.level, 'city': stu.city, 'year2': stu.year2}
        con = di[cond]
        if con == value:
            tocount.append(stu.number)
    toc = Group(tocount)
    count(toc, features, percent)
            


    