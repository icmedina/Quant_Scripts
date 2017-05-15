#!/usr/bin/python2.7

import urllib2 		
#import urllib2.request		# python3.5
import re
import json

# How to get the query URL? Right click on the desired data > Inspect Elements > Select Network Tab > Select XHR (data)
# Select the source 

###### Global VARIABLES ######
market = "CUR"	# IND (index), US (stocks)
period = "1_YEAR" # 1_DAY, 1_MONTH, 1_YEAR, 5_YEAR
mode = "w"	# outfile mode (w - write; a - append)
#urls = https://www.bloomberg.com/markets/watchlist/recent-ticker/AAPL:US
#urls = https://www.bloomberg.com/markets/chart/data/1D/AAPL:US
#urls = https://www.bloomberg.com/markets/api/security/basic/AAPL%3AUS?locale=en
#urls = https://www.bloomberg.com/markets/api/security/detailed/AAPL:US?locale=en
#urls = https://www.bloomberg.com/markets/api/bulk-time-series/price/EURUSD:CUR?timeFrame=1_DAY
#######################

def main():
  # call the functions
  symbols = openSymbols()				# using list of symbols
  #symbols =("AAPL","NFLX")				# using specific symbols
  getPrice(symbols)

def openSymbols():
  symbolsFile = open("symbols.txt")
  symbolsList = symbolsFile.read()			# each line contains  \n
  symbolsFile.close()
  symbols = symbolsList.split("\n")			# convert string to array
  symbols.pop(len(symbols)-1)				# remove the last \n
  return symbols					# return the list of symbols

def getPrice(symbols):
  for symbol in symbols:
    url = 'https://www.bloomberg.com/markets/api/bulk-time-series/price/'+symbol+'%3A'+market+'?timeFrame='+period
    #htmlContent = urllib2.request.urlopen(url).read()	# python3.5
    htmlContent = urllib2.urlopen(url).read()  		
    data = json.loads(htmlContent)
    printPriceDates(symbol,data)

## Print Prices and Dates ## 
def printPriceDates(symbol,data):
  priceTime = 0
  outfile = symbol+"-"+period+".csv"
  output = open(outfile, mode)				# create output file
  output.write("Date,Price\n")

  for values in data[0]["price"]: 
#    print data[0]["price"][priceTime]["value"]		# print values only
    prices = data[0]["price"][priceTime]["date"],data[0]["price"][priceTime]["value"]
    prices = re.sub("\(?u?\'", "", str(prices))		# remove (u' and '
    prices = re.sub("\)", "\n", str(prices))		# replace )
    output.write(str(prices))
    priceTime+=1 
 
  output.close()					# close output file
  print symbol+"\tLast price: ",data[0]["lastPrice"]

main()
