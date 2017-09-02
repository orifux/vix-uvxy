import sys
import pandas
import requests
import io
import datetime
from pandas_datareader.data import Options


#### getting vix data from cboe web site ####
#### http://www.cboe.com/publish/scheduledtask/mktdata/datahouse/vixcurrent.csv ####

#### getting uvxy data from google web site ####
#### https://www.google.com/finance/historical?q=.VIX&startdate=Jul%2027,%202017&enddate=Jul%2027,%202017&output=csv ####

def getStockClosePrice(stock, date):
    stock = stock
    startdate = date.strftime("%m/%d/%Y")
    enddate = (date + datetime.timedelta(days=1)).strftime("%m/%d/%Y")
    #print enddate
    rooturl = 'http://www.google.com/finance/historical?q='
    query = stock + '&startdate=' + startdate +'&enddate=' + enddate + '&output=csv'
    
    url = rooturl + query
    #print url
    #try:
    response = requests.get(url)
    #except:
    #print "Unexpected error:", sys.exc_info()
    df = pandas.read_csv(io.StringIO(response.content.decode('utf-8')))
    #print(df)
    try:
        return df.get_value(0,'Close');
    except:
        return -1;    
    
def getVIXClosePrice(date):
    
    url = 'http://www.cboe.com/publish/scheduledtask/mktdata/datahouse/vixcurrent.csv'
    response = requests.get(url)

    df = pandas.read_csv(io.StringIO(response.content.decode('utf-8')),skiprows=1,index_col=0)
    try:
        return df.loc[date.strftime("%m/%d/%Y"),'VIX Close']
    except:
        return -1;   


def main():
    #print getVixClosePrice('08/22/2017')
    #currDate = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%m/%d/%Y")
    currDate = (datetime.date.today() - datetime.timedelta(days=1))
    #print currDate
    #print currDate.strftime("%m/%d/%Y")
    print getVIXClosePrice(currDate)
    
    print getStockClosePrice('UVXY', currDate)
    
main()
aapl = Options('uvxy', 'yahoo')
data = aapl.get_all_data()
##print data
print '------------------'
print data.iloc[0:5, 0:5]
print '-------------'
#Show the $100 strike puts at all expiry dates:
print data.loc[(46, slice(None), 'call'),:] #.iloc[0:5, 0:5]
print '-------------'
#Show the volume traded of $100 strike puts at all expiry dates:
print data.loc[(46, slice(None), 'put'),'Vol'].head()







