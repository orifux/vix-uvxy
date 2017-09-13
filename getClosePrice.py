import csv
import numpy as np
import pandas as df
import requests
import io
import datetime 
import os.path
import shutil 
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
    df_ = df.read_csv(io.StringIO(response.content.decode('utf-8')))
    #print(df)
    try:
        return df_.get_value(0,'Close');
    except:
        return 'NaN';  

def getVIXClosePrice(date):
    
    path ='./temp/'
    fileName = datetime.datetime.now().strftime("%d-%m-%Y") + '.csv'

    #print df
    if not(os.path.isfile(path+fileName)):
        url = 'http://www.cboe.com/publish/scheduledtask/mktdata/datahouse/vixcurrent.csv'
        response = requests.get(url)
        df_ = df.read_csv(io.StringIO(response.content.decode('utf-8')),skiprows=1,index_col=0)
        shutil.rmtree(path,ignore_errors=True, onerror=None)
        os.makedirs(path)
        df_.to_csv(path+fileName)
    try:
        df_ = df.read_csv(path+fileName,index_col=None, header=0)
        df_ = df_.loc[date.strftime("%m/%d/%Y"),'VIX Close']
        #print df
        return df_
    except:
        return 'NaN';


def main():
    #print getVixClosePrice('08/22/2017')
    #currDate = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%m/%d/%Y")
    date = (datetime.date.today() - datetime.timedelta(days=3))
    #endDate = (datetime.date.today() - datetime.timedelta(days=1))
    print 'for date:' , date
    #print currDate.strftime("%m/%d/%Y")
    #print getVIXClosePrice(date)
    #print df_vixClosePrice
    #print getStockClosePrice('UVXY', startDate)
    
      
    todays_date = datetime.datetime.now().date()
    dateArr = df.date_range(todays_date-datetime.timedelta(4), periods=4, freq='D')
    #print index[1]
    
    #columns = ['pos_num','open_pos_date','vix_pos_price','uvxy_pos_price','uvxy_vix_pos_ratio','uvxy_vix_curr_pos','os_vix_qty','pos_vix_op_price','pos_vix_strick','pos_vix_exp','pos_uvxy_qty','pos_uvxy_op_price','pos_uvxy_strick','pos_uvxy_exp','pos_vix_amount','pos_uvxy_amount','curr_pos_vix_value','curr_pos_uvxy_value','days_pass','is_55_days_pass','pos_ratio*0.75 >=curr_ratio','pos_status','pos_gain']
    columns = ['pos_num','open_pos_date']##,'vix_pos_price','uvxy_pos_price','uvxy_vix_pos_ratio','uvxy_vix_curr_pos','pos_vix_qty','pos_vix_op_price','pos_vix_strick','pos_vix_exp','pos_uvxy_qty','pos_uvxy_op_price','pos_uvxy_strick','pos_uvxy_exp','pos_vix_amount','pos_uvxy_amount','curr_pos_vix_value','curr_pos_uvxy_value','days_pass','is_55_days_pass','pos_ratio*0.75 >=curr_ratio','pos_status','pos_gain']
      
    np_array_list = []
    
    for i in range(4):
        print i ,'------'
        open_pos_date = dateArr[i]
        vix_pos_price = getVIXClosePrice(dateArr[i])
        uvxy_pos_price=getStockClosePrice('UVXY',dateArr[i])
        if vix_pos_price != 'NaN': 
            uvxy_vix_pos_ratio = (uvxy_pos_price/vix_pos_price)
            uvxy_vix_curr_pos = uvxy_vix_pos_ratio
            pos_vix_qty = (vix_pos_price/uvxy_pos_price)
            if pos_vix_qty < 1:
                pos_vix_qty=round(pos_vix_qty)
                pos_uvxy_qty =1
            else:
                pos_vix_qty = 1
                pos_uvxy_qty =round(pos_vix_qty)
            pos_vix_op_price = 999
            pos_vix_strick = 99
            pos_vix_exp = '2018-01-01'
            pos_uvxy_op_price = 999
            pos_uvxy_strick = 99
            pos_uvxy_exp= '2018-01-01'
            pos_vix_amount = pos_vix_op_price * pos_vix_qty
            pos_uvxy_amount = pos_uvxy_op_price*pos_uvxy_qty         
        else:
            uvxy_vix_pos_ratio = 'NaN'
            uvxy_vix_curr_pos = 'NaN'
            pos_vix_op_price = 'NaN'
            pos_vix_strick = 'NaN'
            pos_vix_exp = 'NaN'
            pos_uvxy_op_price = 'NaN'
            pos_uvxy_strick = 'NaN'
            pos_uvxy_exp = 'NaN'
            pos_vix_amount = 'NaN'
            pos_uvxy_amount = 'NaN'
            
        res = np.array([open_pos_date,vix_pos_price,uvxy_pos_price,uvxy_vix_pos_ratio,uvxy_vix_curr_pos, pos_vix_qty,pos_vix_op_price, pos_vix_strick,pos_vix_exp, pos_uvxy_qty,pos_uvxy_op_price,pos_uvxy_qty,pos_uvxy_strick,pos_uvxy_exp,pos_vix_amount,pos_uvxy_amount])
        np_array_list.append(res)
    print np_array_list
    print '-------'
    comb_np_array = np.vstack(np_array_list)
    big_frame = df.DataFrame(comb_np_array)
    #df_ = pandas.DataFrame(result_array,index=index, columns=columns)
    #df_ = df_.fillna(0) # with 0s rather than NaNs
    print big_frame
    
main()

'''
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

'''












