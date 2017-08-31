import pandas
import requests
import io
import datetime
from datetime import timedelta  

#http://www.cboe.com/publish/scheduledtask/mktdata/datahouse/vixcurrent.csv



def getUVXYClosePrice(stock, date, source):
    stock = stock
    startdate = date
    enddate = date

    rooturl = 'http://www.google.com/finance/historical?q='
    query = stock + '&startdate=' + startdate +'&enddate=' + enddate + '&output=csv'
    
    url = rooturl + query
    print url
    response = requests.get(url)

    df = pandas.read_csv(io.StringIO(response.content.decode('utf-8')))
    print(df)
    try:
        return df.get_value(0,'Close');
    except:
        return -1;    
    
def getVIXClosePrice(date):
    
    url = 'http://www.cboe.com/publish/scheduledtask/mktdata/datahouse/vixcurrent.csv'
    response = requests.get(url)

    df = pandas.read_csv(io.StringIO(response.content.decode('utf-8')),skiprows=1,index_col=0)
    try:
        return df.loc[date,'VIX Close']
    except:
        return -1;   

#print getVixClosePrice('08/22/2017')
currDate = (datetime.date.today() - datetime.timedelta(days=2)).strftime("%m/%d/%Y")
print currDate
print getVIXClosePrice(currDate)