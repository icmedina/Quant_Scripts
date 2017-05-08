#!/usr/bin/python


def getYahooStockQuote(symbol): 
  "input: a stock symbol output: a dict of stock infomation" 
  url = "http://download.finance.yahoo.com/d/quotes.csv?s=%s&f=sl1d1c1hgv" % symbol 
  f = urllib2.urlopen(url) 
  s = f.read() 
  f.close() 
  s = s.strip() 
  L = s.split(',') 
  D = {} 
  D['symbol'] = L[0] #.replace('"',") 
  D['last'] = L[1] 
  D['date'] = L[2]#.replace('"',") 
  D['change'] = L[3] 
  D['high'] = L[4] 
  D['low'] = L[5] 
  D['vol'] = L[6] 

 print D 
  return D

