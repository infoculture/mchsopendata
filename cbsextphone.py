#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'ibegtin'

from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
import json
import csv

MCHS_URL = 'http://www.mchs.gov.ru'
MCHS_EP_URL = 'http://www.mchs.gov.ru/get_ep?regionCode=%s'

def listRegions():
    """Extracts list of regions from MCHS website"""
    u = urlopen(MCHS_URL)
    data = u.read()
    soup = BeautifulSoup(data)
    div = soup.find('div', attrs={'class': 'emphcb-body clearfix'})
    ul = div.find('ul')
    lis = ul.findAll('li')
    regions = []
    for li in lis:
        a = li.find('a')
        regions.append({'id' : a['rel'], 'name' : a.string})
    return regions

def process():
    """For each region extracts phone data"""
    regions = listRegions()
    allops = []
    for o in regions:
        o.update(extract_phones(o['id']))
        print o['name'].encode('utf8')
        for op in o['ops']:
            if op not in allops:
                allops.append(op)
#        for s in o['phones']:
 #           print '-', s['op'], s['service'], s['phone']
    # dump operators
    wr = csv.writer(open('data/phones/ops.csv','w'), dialect=csv.excel)
    wr.writerow(['name',])
    for op in allops:
        wr.writerow([op.encode('utf8'), ])

    # dump regions
    wr = csv.writer(open('data/phones/regions.csv','w'), dialect=csv.excel)
    wr.writerow(['id', 'name'])
    for r in regions:
        wr.writerow([r['id'].encode('utf8'), r['name'].encode('utf8')])

    # dump services
    wr = csv.writer(open('data/phones/services.csv','w'), dialect=csv.excel)
    wr.writerow(['id', 'region_name', 'service_name'])
    for r in regions:
        for s in r['services']:
            wr.writerow([r['id'].encode('utf8'), r['name'].encode('utf8'), s.encode('utf8')])

    # dump phones
    wr = csv.writer(open('data/phones/phones.csv','w'), dialect=csv.excel)
    wr.writerow(['id', 'region_name', 'service_name', 'op_name', 'phone'])
    for r in regions:
        for p in r['phones']:
            wr.writerow([r['id'].encode('utf8'), r['name'].encode('utf8'), p['service'].encode('utf8'), p['op'].encode('utf8'), p['phone'].encode('utf8') if p['phone'] is not None else ""])


def extract_phones(regcode):
    """Extracts urgency phones from MCHS website"""
    u = urlopen(MCHS_EP_URL % regcode)
    data = u.read()
    j = json.loads(data)
    h = j['body']
    ops = []
    services = []
    phones = []
    soup = BeautifulSoup(h)
    thead = soup.find('thead')
    tds = thead.findAll('td')
    for td in tds[1:]:
        i = td.find('i')
        ops.append(i['title'])
    tbody = soup.find('tbody')
    trs = tbody.findAll('tr')
    trcount = 0
    for tr in trs:
        th = tr.find('th')
        services.append(th.string)
        tds = tr.findAll('td')
        i = 0
        for td in tds:
            phones.append({'phone' : td.string, 'op' : ops[i], 'service' : services[trcount]})
            i += 1
        trcount += 1
    return {'phones' : phones, 'ops' : ops, 'services' : services}
#    print soup


if __name__ == "__main__":
    process()
