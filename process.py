#!/usr/bin/env python
# -*- coding: utf-8 -*-

import  urllib2
from BeautifulSoup import BeautifulSoup
from urlparse import urljoin
import time
import mechanize


CALEND_URLPAT = "http://www.mchs.gov.ru/articles/emergency_info/digest/%d/%d/"
BASE_URL = 'http://www.mchs.gov.ru'

def extract_links():
    """Extracts all reports of MCHS to the alllinks.csv"""
    br = mechanize.Browser()
    br.open(BASE_URL)
    f = open('data/svodki/alllinks.csv', 'w')
    calurls = []
    # Collect all calendar urls with reports
    for year in range(2005, 2013):
        for month in range(1, 13):
            calurls.append([year, month, CALEND_URLPAT  %(year, month)])

    # Update for current year (needs fixes later)
    for year in range(2013, 2014):
        for month in range(1, 3):
            calurls.append([year, month, CALEND_URLPAT  %(year, month)])
    # Process calendar urls one by one
    for year, month, calurl in calurls:
        print calurl
        u = br.open(calurl)
        data = u.read()
        u.close()
        soup = BeautifulSoup(data)
        slist = soup.find('ul', attrs={'class': 'emergency_list'})
        urls = slist.findAll('a')
        for url in urls:
            s = '%s\t%s\t%s\t%s\t' % (unicode(year), unicode(month), url.text, urljoin(BASE_URL, url['href']))
            f.write((s + '\n').encode('utf8'))
            print s
    f.close()

def process_links():
    """Reads all MCHS reports from web and imports to the MongoDB"""
    from pymongo import Connection
    conn = Connection()
    db = conn['mchs']
#    db.drop_collection('svodki')
    coll = db['svodki']
    coll.ensure_index("url")
    f = open('alllinks.csv', 'r')
    for l in f:
        parts = l.strip().split('\t')
        if len(parts) < 4: continue
        year, month, day, url = parts
        o = coll.find_one({'url' : url})
        if o is not None: 
            print url, 'passed'
            continue
        u = urllib2.urlopen(url)
        data = u.read()
        u.close()
        data = data.decode('cp1251')
        record = {'year' : int(year), 'month' : int(month), 'day' : int(day), 'url' : url, 'text' : data.encode('utf8')}
        coll.save(record)
        # MCHS site is badly designed and it could block us if we will download pages too often
        time.sleep(5)
        print url, 'processed'



if __name__ == "__main__":
    extract_links()
#    process_links()
#     parse_all()
