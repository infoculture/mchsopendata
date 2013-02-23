#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'ibegtin'

from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
import csv
from cStringIO import StringIO

MCHS_MAP_URL = 'http://www.fire.mchs.gov.ru/fire_map/'

FIELDNAMES = ['name', 'postindex', 'address', 'contact', 'latitude', 'longitude', 'unk1', 'unk2', 'image_url', 'unk3', 'unk4']

def process():
    """Extracts MCHS data from"""
    u = urlopen(MCHS_MAP_URL)
    data = u.read()
    u.close()
    data = data.decode('windows-1251')
    pos1 = data.find('//c1')
    pos2 = data.find('ClearClasterCount(1)')
    text = data[pos1:pos2]
    lines = text.splitlines()
    io = StringIO()
    n = 0
    for l in lines:
        l = l.strip()
        if l[0:2] == '//': continue
#        print
        io.write(l.replace(']', '').replace('[', '')[14:-2].encode('utf8')+'\n')
    io.reset()
#    print io.read()
    reader = csv.DictReader(io, FIELDNAMES, dialect='excel')
    writer = csv.DictWriter(open('data/branches/branches.csv', 'w'), FIELDNAMES, delimiter="\t")
    writer.writeheader()
    for l in reader:
        s = '\t'.join(l)
#        print s
        writer.writerow(l)
#    print io.read()


if __name__ == "__main__":
    process()