import pandas
import requests
import io

def getClosePrice(stock, date, source):
    stock = stock
    startdate = date
    enddate = date

    rooturl = 'http://www.google.com/finance/historical?q='
    query = stock + '&startdate=' + startdate +'&enddate=' + enddate #+ '&output=csv'
    
    url = rooturl + query
    print url
    response = requests.get(url)

    df = pandas.read_csv(io.StringIO(response.content.decode('utf-8')))
    print(df)
    try:
        return df.get_value(0,'Close');
    except:
        return -1;    

def getClosePrice(stock, date):
    stock = stock
    startdate = date
    enddate = date

    rooturl = 'http://www.google.com/finance/historical?q='
    query = stock + '&startdate=' + startdate +'&enddate=' + enddate #+ '&output=csv'
    
    url = rooturl + query
    print url
    response = requests.get(url)

    df = pandas.read_csv(io.StringIO(response.content.decode('utf-8')))
    print(df)
    try:
        return df.get_value(0,'Close');
    except:
        return -1;    

https://ichart.yahoo.com/table.csv?s=AAPL&a=0&b=1&c=2010&d=11&e=31&f=2015&g=m&ignore=.csv
print getClosePrice('UVXY', 'Jul 27, 2017')