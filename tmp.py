# -*- coding: utf-8 -*-
"""
Created on Wed Jul 08 20:01:03 2015

@author: cenkai
"""
#features为学号的list, percent为是否按百分比显示，默认关闭
def count(self, features,percent=False):
    totaltag = []
    for stu in self.all:
        di = {'gender':stu.gender, 'unit':stu.unit, 'tutor':stu.tutor, 'hometown':stu.hometown, 'major':stu.major, 'edu':stu.edu, 'politic':stu.politic2, 'graduate':stu.graduate, 'year':stu.year, 'emailprovider':stu.emailprovider, 'phd':stu.phd, 'familyname':stu.familyname, 'province':stu.province, 'level':stu.level}
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
        
