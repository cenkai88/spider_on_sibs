# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 10:28:39 2015

@author: cenkai
"""
from sibs import Group
from sibs import Student

def main():
    testG = Group()
    testG.count(['unit'])
    testG.count(['gender'],True)
    testG.count2('unit','植生生态所', ['year', 'gender'])
    ex = Student('201328010015193')
    ex.show_info()

if __name__ == '__main__':
    main()