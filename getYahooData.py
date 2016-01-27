#!/usr/bin/env python 

import re
from bs4 import BeautifulSoup
import requests
import requests_cache
#requests_cache.install_cache('etables', backend='sqlite', expire_after=360) # uncomment for production

## Pull data from yahoo finance given a ticker symbol
def getYahooData(tick):
    url = "http://finance.yahoo.com/q/ks?s=%20" 
    url += str(tick) + "%20+Key+Statistics"
    s = requests.Session()
    r = s.get(url)
    sdata = r.text
    soup = BeautifulSoup(sdata)
    trs = soup.find_all("tr")
    data = {}
    for tr in trs:
        head = tr.find("td", class_="yfnc_tablehead1")
        if head:
            [x.extract() for x in head.findAll('font')] # remove weird superscript text
        val = tr.find("td", class_="yfnc_tabledata1")
        if (head and val):
            data[head.getText()] = val.getText()
    return data
 
## Example:
yahooData = getYahooData("AAPL")
if 'Qtrly Revenue Growth (yoy):' in yahooData:
  print yahooData['Qtrly Revenue Growth (yoy):']
if 'Qtrly Earnings Growth (yoy):' in yahooData:
  print yahooData['Qtrly Earnings Growth (yoy):']
