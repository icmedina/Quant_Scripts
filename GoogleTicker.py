# Hacking Google Finance in Real-Time for Algorithmic Traders
# 
# (c) 2014 QuantAtRisk.com, by Pawel Lachowicz
# Python-3 version --- urllib.request used instead of urllib2
# Link to related article:
# http://www.quantatrisk.com/2014/01/14/hacking-google-finance-in-real-time-for-algorithmic-traders/

import urllib.request, time, os, re, csv

def fetchGF(googleticker):
    url = "https://www.google.com/finance?&q="
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req)
    respData = resp.read()
    k=re.search(b'id="ref_(.*?)">(.*?)<', respData)
    if k:
        tmp=k.group(2)
        q=tmp.decode().replace(',','')
    else:
        q="Nothing found for: "+googleticker
    return q



# display time corresponding to your location
print(time.ctime(),"(local time)")
print()
 
# Set local time zone to NYC
os.environ['TZ']='America/New_York'
time.tzset()
t=time.localtime() # string
print(time.ctime(), "(New York)")
print()

def combine(ticker):
    quote=fetchGF(ticker) # use the core-engine function
    t=time.localtime()    # grasp the moment of time
    output=[t.tm_year,t.tm_mon,t.tm_mday,t.tm_hour,  # build a list
            t.tm_min,t.tm_sec,ticker,quote]
    return output

#ticker="NASDAQ:AAPL"

# define file name of the output record
fname="portfolio.dat"
# remove a file, if exist
os.path.exists(fname) and os.remove(fname)

# To test, set the hour and minutes according to the above printed
# time in New York so you can capture 2 or 3 values before the loop
# stops

freq=600 # fetch data every 600 sec (10 min)

tickers=["NASDAQ:AAPL","NASDAQ:GOOG","NASDAQ:BIDU","NYSE:IBM", \
         "NASDAQ:INTC","NASDAQ:MSFT","NYSEARCA:SPY"]
 
with open(fname,'a') as f:
    writer = csv.writer(f,dialect="excel") #,delimiter=" ")
    while(t.tm_hour <= 9):
        if(t.tm_hour == 9):
            while(t.tm_min < 31):
                data = combine(ticker)
                print(data)
                writer.writerow(data) # save data in the file
                time.sleep(freq)
            else:break
        else:
            for ticker in tickers:
                data=combine(ticker)
                print(data)
                writer.writerow(data) # save data in the file
                time.sleep(freq)
f.close()
print(str(t.tm_hour) + ":" + str(t.tm_min))
