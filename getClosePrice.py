import csv
import glob
import numpy as np
import pandas as df
import requests
import io
import datetime 

import os.path
import shutil 
from pandas_datareader.data import Options
from dircache import listdir
from pip._vendor.distlib._backport.tarfile import TUREAD
from pyasn1.compat.octets import null
from dateutil.relativedelta import relativedelta

g_daysToClase = 5
#### getting vix data from cboe web site ####
#### http://www.cboe.com/publish/scheduledtask/mktdata/datahouse/vixcurrent.csv ####

#### getting uvxy data from google web site ####
#### https://www.google.com/finance/historical?q=.VIX&startdate=Jul%2027,%202017&enddate=Jul%2027,%202017&output=csv ####


def getOptClosePrice(stock,source,expDate, strick):
    
    df_opt = Options(stock, source)
    data = df_opt.get_all_data()
    '''
    print data.loc[(46, '2018-03-16','call'),('Last','Underlying_Price')].head()
    print data.loc[(46, '2018-03-16','call'),'Vol'].head()
    print '------------------'
    print data.iloc[0:5, 0:5]
    print '-------------'
    #Show the $100 strike puts at all expiry dates:
    '''
    #print '1: ' , data.loc[(strick, expDate, 'call'),:] #.iloc[0:5, 0:5]
    res = data.loc[(strick, expDate, 'call'),('Last','Underlying_Price')] #.iloc[0:5, 0:5]
    print '1: ' , res
    print '--------------'
    return res

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
    existfile = listdir(path)[0].split(".csv",1)[0] #glob.glob(path + '*')
    existFileDate = datetime.datetime.strptime(existfile, "%d-%m-%Y")
    if (existFileDate < date): # create new file with updated vix data
        url = 'http://www.cboe.com/publish/scheduledtask/mktdata/datahouse/vixcurrent.csv'
        response = requests.get(url)
        df_ = df.read_csv(io.StringIO(response.content.decode('utf-8')),skiprows=1,index_col=0)
        shutil.rmtree(path,ignore_errors=True, onerror=None)
        os.makedirs(path)
        df_.to_csv(path+fileName)
    try:
        df_ = df.read_csv(path+existfile + '.csv',index_col='Date', header=0)
        df_ = df_.loc[date.strftime("%m/%d/%Y"),'VIX Close']
        return df_
    except:
        return 'NaN';


def main():
    #print getVixClosePrice('08/22/2017')
    #currDate = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%m/%d/%Y")
    df_opt = Options('UVXY', 'yahoo')
    data1 = df_opt.get_all_data()
    print data1
    date = (datetime.date.today() - datetime.timedelta(days=20))
    #endDate = (datetime.date.today() - datetime.timedelta(days=1))
    print 'for date:' , date
    #print currDate.strftime("%m/%d/%Y")
    #print getVIXClosePrice(date)
    #print df_vixClosePrice
    #print getStockClosePrice('UVXY', startDate)
    print getOptClosePrice('UVXY', 'yahoo', '2018-03', 46 ).iloc[0]['Last']
    
      
    todays_date = datetime.datetime.now().date()
    dateArr = df.date_range(todays_date-datetime.timedelta(5), periods=5, freq='D')
    newFileName = './temp/positionFile.csv'
    #print index[1]
    
    #columns = ['pos_num','open_pos_date','vix_pos_price','uvxy_pos_price','uvxy_vix_pos_ratio','uvxy_vix_curr_pos','os_vix_qty','pos_vix_op_price','pos_vix_strick','pos_vix_exp','pos_uvxy_qty','pos_uvxy_op_price','pos_uvxy_strick','pos_uvxy_exp','pos_vix_amount','pos_uvxy_amount','curr_pos_vix_value','curr_pos_uvxy_value','days_pass','is_55_days_pass','pos_ratio*0.75 >=curr_ratio','pos_status','pos_gain']
    columns = ['pos_num','open_pos_date','vix_pos_price','uvxy_pos_price','uvxy_vix_pos_ratio','uvxy_vix_curr_pos','pos_vix_qty','pos_vix_op_price','pos_vix_strick','pos_vix_exp','pos_uvxy_qty','pos_uvxy_op_price','pos_uvxy_strick','pos_uvxy_exp','pos_vix_amount','pos_uvxy_amount','curr_pos_vix_value','curr_pos_uvxy_value','days_pass','is_55_days_pass','pos_ratio*0.75 >=curr_ratio','pos_status','pos_gain']
  
    np_array_list = []
    
    for i in range(5):
        print i ,'------'
        open_pos_date = dateArr[i]
        vix_pos_price = getVIXClosePrice(dateArr[i])
        uvxy_pos_price=getStockClosePrice('UVXY',dateArr[i])
        print 'date: ' , open_pos_date, 'vix: ', vix_pos_price, 'uvxy: ',  uvxy_pos_price
        if vix_pos_price != 'NaN': 
            uvxy_vix_pos_ratio = round(uvxy_pos_price/vix_pos_price,2)
            uvxy_vix_curr_pos = uvxy_vix_pos_ratio
            pos_vix_qty = round(vix_pos_price/uvxy_pos_price,2)
            if pos_vix_qty < 1:
                pos_vix_qty=round(1/pos_vix_qty)
                pos_uvxy_qty =1
            else:
                pos_vix_qty = 1
                pos_uvxy_qty =round(pos_vix_qty)
            pos_vix_exp = (dateArr[i] + relativedelta(months=5)).strftime("%m-%Y")        
            pos_vix_strick = round(vix_pos_price*1.5)        
            curr_vix_op_price = getOptClosePrice('VIX', 'yahoo', pos_vix_exp, pos_vix_strick ).iloc[0]['Last']
            pos_vix_op_price = curr_vix_op_price
            pos_uvxy_exp= (dateArr[i] + relativedelta(months=6)).strftime("%m-%Y")
            pos_uvxy_strick = round(uvxy_pos_price*1.5)            
            curr_uvxy_op_price = getOptClosePrice('UVXY', 'yahoo', pos_uvxy_exp, pos_uvxy_strick ).iloc[0]['Last']
            pos_uvxy_op_price = curr_uvxy_op_price
            pos_vix_amount = round(pos_vix_op_price * pos_vix_qty)
            pos_uvxy_amount = round(pos_uvxy_op_price*pos_uvxy_qty)     
            curr_pos_vix_value = round(pos_vix_qty * curr_vix_op_price)
            curr_pos_uvxy_value = round(pos_uvxy_qty * curr_uvxy_op_price)
            days_pass  = (datetime.datetime.now() - open_pos_date).days
            is_55_days_pass = True if days_pass >=g_daysToClase else False
            pos_ratio_075 = True if uvxy_vix_curr_pos*0.75 >= uvxy_vix_pos_ratio else False
            pos_status = 'Closed' if (pos_ratio_075 or is_55_days_pass) else 'Open'     
            pos_gain = curr_pos_vix_value - pos_vix_amount + pos_uvxy_amount - curr_pos_uvxy_value
        else:
            uvxy_vix_pos_ratio = 'NaN'
            uvxy_vix_curr_pos = 'NaN'
            pos_vix_qty = 'NaN'
            pos_uvxy_qty = 'NaN'
            pos_vix_op_price = 'NaN'
            pos_vix_strick = 'NaN'
            pos_vix_exp = 'NaN'
            pos_uvxy_op_price = 'NaN'
            pos_uvxy_strick = 'NaN'
            pos_uvxy_exp = 'NaN'
            pos_vix_amount = 'NaN'
            pos_uvxy_amount = 'NaN'
            curr_vix_op_price = 'NaN'
            curr_uvxy_op_price = 'NaN'
            curr_pos_vix_value = 'NaN'
            curr_pos_uvxy_value = 'NaN'
            days_pass  = 'NaN'
            is_55_days_pass = 'NaN'
            pos_ratio_075 = 'NaN'
            pos_status = 'NaN'
            pos_gain = 'NaN'
            
        res = np.array([open_pos_date.strftime("%d-%m-%Y"),vix_pos_price,uvxy_pos_price,uvxy_vix_pos_ratio,uvxy_vix_curr_pos, pos_vix_qty,pos_vix_op_price,curr_vix_op_price, pos_vix_strick,pos_vix_exp, pos_uvxy_qty,pos_uvxy_op_price,curr_uvxy_op_price,pos_uvxy_qty,pos_uvxy_strick,pos_uvxy_exp,pos_vix_amount,pos_uvxy_amount,curr_pos_vix_value,curr_pos_uvxy_value,days_pass,is_55_days_pass,pos_ratio_075, pos_status, pos_gain])
        np_array_list.append(res)
    print '-------'
    
    comb_np_array = np.vstack(np_array_list)
    big_frame = df.DataFrame(comb_np_array)    
    big_frame.columns = ["open_pos_date","vix_pos_price","uvxy_pos_price","uvxy_vix_pos_ratio","uvxy_vix_curr_pos", "pos_vix_qty","pos_vix_op_price","curr_vix_op_price", "pos_vix_strick","pos_vix_exp", "pos_uvxy_qty","pos_uvxy_op_price","curr_uvxy_op_price","pos_uvxy_qty","pos_uvxy_strick","pos_uvxy_exp","pos_vix_amount","pos_uvxy_amount","curr_pos_vix_value","curr_pos_uvxy_value","days_pass","is_55_days_pass","pos_ratio_075", "pos_status", "pos_gain"]
    #big_frame.set_index(['open_pos_date'])
   # big_frame.to_csv(newFileName, index=False,header=True)
    big_frame.to_csv(newFileName,header=True)

    #df_ = pandas.DataFrame(result_array,index=index, columns=columns)
    #df_ = df_.fillna(0) # with 0s rather than NaNs
    print big_frame
    
main()














