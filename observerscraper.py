#!/usr/bin/env python3

# Scrape the web page from an Ambient Weather Observer.

import requests
from bs4 import BeautifulSoup
import sys
import re

prettynames = {
    'CurrTime'      : 'Current Time',
    'AbsPress'      : 'Abs Pressure',
    'RelPress'      : 'Relative Pressure',

    'avgwind'       : 'Average Wind',
    'gustspeed'     : 'Wind Gust',
    'dailygust'     : 'Max Daily Gust',
    'windir'        : 'Wind Direction',

    'rainofhourly'  : 'Hourly Rain',
    'rainofdaily'   : 'Daily Rain',
    'rainofweekly'  : 'Weekly Rain',
    'rainofmonthly' : 'Monthly Rain',
    'rainofyearly'  : 'Yearly Rain',

    'uv'            : 'UV',
    'uvi'           : 'UV Index',
    'solarrad'      : 'Solar Radiation',

    'outTemp'       : 'Outdoor Temp',
    'outHumi'       : 'Outdoor Humidity',
    'Outdoor1ID'    : 'Outdoor ID',
    'outBattSta1'   : 'Outdoor ID/Battery',

    'inTemp'        : 'Indoor Temp',
    'inHumi'        : 'Indoor Humidity',
    'IndoorID'      : 'Indoor ID',
    'inBattSta'     : 'Indoor ID/Battery',

    'Outdoor2ID'    : 'Outdoor 2 ID',
    'outBattSta2'    : 'Outdoor 2 ID/Battery',
    }

nameorder = [
    'CurrTime',

    'AbsPress',
    'RelPress',

    'avgwind',
    'gustspeed',
    'dailygust',
    'windir',

    'rainofhourly',
    'rainofdaily',
    'rainofweekly',
    'rainofmonthly',
    'rainofyearly',

    'uv',
    'uvi',
    'solarrad',

    'outTemp',
    'outHumi',
    'Outdoor1ID',
    'outBattSta1',

    'inTemp',
    'inHumi',
    'IndoorID',
    'inBattSta',

    'Outdoor2ID',
    'outBattSta2',
    ]

def parse_value(s):
    '''Parse a string value, returning float, int or str as appropriate.
    '''
    # Figure out what type val is: float, int or string.
    try:
        val = int(s)
    except ValueError:
        try:
            val = float(s)
        except ValueError:
            val = s
    return val

def prettykey(key):
    if key in prettynames:
        return prettynames[key]
    print(key, "isn't in prettynames")
    return key

def scrape_page(url):
    r = requests.get(url)
    out = ''

    soup = BeautifulSoup(r.text, "lxml")

    outdata = {}

    for item in soup.find_all('input', type='text',
                              class_=re.compile('item.*')):
        if 'name' not in item.attrs or 'value' not in item.attrs:
            print("\nThis item lacks name or value:", item)
            for key in item.attrs:
                print("  %s: %s" % (key, item[key]))
            continue

        key = item['name']
        val = parse_value(item['value'])

        outdata[key] = val

    return outdata

if __name__ == '__main__':
    vals = scrape_page(sys.argv[1])
    print("Got vals:", vals)
    for key in vals:
        print("%20s  %s" % (key, vals[key]))
