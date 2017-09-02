import numpy as np
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
    
def getVIXClosePrice(startDate,endDate):
    
    url = 'http://www.cboe.com/publish/scheduledtask/mktdata/datahouse/vixcurrent.csv'
    response = requests.get(url)

    df = pandas.read_csv(io.StringIO(response.content.decode('utf-8')),skiprows=1,index_col=0)
    #print df
    try:
        df=df.loc[startDate.strftime("%m/%d/%Y"):endDate.strftime("%m/%d/%Y"),'VIX Close']
        return df
    except:
        return -1;   


def main():
    #print getVixClosePrice('08/22/2017')
    #currDate = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%m/%d/%Y")
    startDate = (datetime.date.today() - datetime.timedelta(days=4))
    endDate = (datetime.date.today() - datetime.timedelta(days=1))
    #print currDate
    #print currDate.strftime("%m/%d/%Y")
    df_vixClosePrice=getVIXClosePrice(startDate,endDate)
    print df_vixClosePrice.index.values
    #print getStockClosePrice('UVXY', startDate)
    
        
    todays_date = datetime.datetime.now().date()
    index = pandas.date_range(todays_date-datetime.timedelta(4), periods=4, freq='D')
    #print index[1]
    
    #columns = ['pos_num','open_pos_date','vix_pos_price','uvxy_pos_price','uvxy_vix_pos_ratio','uvxy_vix_curr_pos','os_vix_qty','pos_vix_op_price','pos_vix_strick','pos_vix_exp','pos_uvxy_qty','pos_uvxy_op_price','pos_uvxy_strick','pos_uvxy_exp','pos_vix_amount','pos_uvxy_amount','curr_pos_vix_value','curr_pos_uvxy_value','days_pass','is_55_days_pass','pos_ratio*0.75 >=curr_ratio','pos_status','pos_gain']
    columns = ['pos_num','open_pos_date']##,'vix_pos_price','uvxy_pos_price','uvxy_vix_pos_ratio','uvxy_vix_curr_pos','os_vix_qty','pos_vix_op_price','pos_vix_strick','pos_vix_exp','pos_uvxy_qty','pos_uvxy_op_price','pos_uvxy_strick','pos_uvxy_exp','pos_vix_amount','pos_uvxy_amount','curr_pos_vix_value','curr_pos_uvxy_value','days_pass','is_55_days_pass','pos_ratio*0.75 >=curr_ratio','pos_status','pos_gain']
    #A = np.array([[1,2],[4,5]])
    Alist = []
    Alist = df_vixClosePrice.values
    print Alist
    for i in range(100):
        print i
      #  newrow = np.array([i,getVIXClosePrice(index[i])])
       # print newrow
       # Alist.append(newrow)
    A = np.array(Alist)
    print A
    print '-------'
    df_ = pandas.DataFrame(A,index=index, columns=columns)
    #df_ = df_.fillna(0) # with 0s rather than NaNs
    print df_
    
main()
aapl = Options('uvxy', 'yahoo')
data = aapl.get_all_data()
##print data
print data.loc[(46, '2018-03-16','call'),('Last','Underlying_Price')].head()
print data.loc[(46, '2018-03-16','call'),'Vol'].head()
print '------------------'
print data.iloc[0:5, 0:5]
print '-------------'
#Show the $100 strike puts at all expiry dates:
print data.loc[(46, slice(None), 'call'),:] #.iloc[0:5, 0:5]
print '-------------'














