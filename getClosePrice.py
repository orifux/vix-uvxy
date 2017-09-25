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
g_vixDF = None
g_isVixLoaded = False
g_uvxyDF = None
g_isUvxyLoaded = False
g_vixpath ='./vix/'
g_uvxypath ='./uvxy/'
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
#    print '1: ' , res
#    print '--------------'
    return res

def getStockClosePrice(stock, date):

    global g_isUvxyLoaded
    global g_uvxyDF
    global g_uvxypath
    existFileDate = datetime.datetime.strptime('01-01-1970',"%d-%m-%Y")
    fileName = datetime.datetime.now().strftime("%d-%m-%Y") + '_uvxy.csv'
    
    newlist = []
    for filename in listdir(g_uvxypath):
        if filename.endswith('_uvxy.csv'):
            newlist.append(filename)
            
    try:
        existfile = newlist[0].split('_uvxy.csv',1)[0]
        existFileDate = datetime.datetime.strptime(existfile, "%d-%m-%Y")
    except:
        existFileDate = datetime.datetime.strptime('01-01-1970',"%d-%m-%Y")
        
    if (existFileDate < date and g_isUvxyLoaded == False): # create new file with updated vix data
        
        enddate = datetime.date.today()
        startdate =  (enddate - datetime.timedelta(days=2000)) #date.strftime("%m/%d/%Y")

        rooturl = 'http://www.google.com/finance/historical?q='
        query = stock + '&startdate=' + startdate.strftime("%m/%d/%Y") +'&enddate=' + enddate.strftime("%m/%d/%Y") + '&output=csv'
    
        url = rooturl + query

        response = requests.get(url)   
        g_uvxyDF = df.read_csv(io.StringIO(response.content.decode('utf-8')),index_col=0)
        shutil.rmtree(g_uvxypath,ignore_errors=True, onerror=None)
        os.makedirs(g_uvxypath)
        g_uvxyDF.to_csv(g_uvxypath+fileName)
        
    elif(g_isUvxyLoaded == False):
            g_uvxyDF = df.read_csv(g_uvxypath+existfile + '_uvxy.csv',index_col='Date', header=0)
    g_isUvxyLoaded = True
    
    try:
        return g_uvxyDF.loc[date.strftime("%d-%b-%y"),'Close']
    except:
        g_isUvxyLoaded = True
        return 'NaN';    

def getVIXClosePrice(date):
    global g_isVixLoaded
    global g_vixDF
    global g_vixpath
    existFileDate = datetime.datetime.strptime('01-01-1970',"%d-%m-%Y")
    fileName = datetime.datetime.now().strftime("%d-%m-%Y") + '_vix.csv'
    newlist = []
    for filename in listdir(g_vixpath):
        if filename.endswith('_vix.csv'):
            newlist.append(filename)
    try:
        existfile = newlist[0].split('_vix.csv',1)[0]
        existFileDate = datetime.datetime.strptime(existfile, "%d-%m-%Y")
    except:
        existFileDate = datetime.datetime.strptime('01-01-1970',"%d-%m-%Y")    
    
    if (existFileDate < date and g_isVixLoaded == False): # create new file with updated vix data
        url = 'http://www.cboe.com/publish/scheduledtask/mktdata/datahouse/vixcurrent.csv'
        response = requests.get(url)
        g_vixDF = df.read_csv(io.StringIO(response.content.decode('utf-8')),skiprows=1,index_col=0)
        shutil.rmtree(g_vixpath,ignore_errors=True, onerror=None)
        os.makedirs(g_vixpath)
        g_vixDF.to_csv(g_vixpath+fileName)
        
    elif(g_isVixLoaded == False):
            g_vixDF = df.read_csv(g_vixpath+existfile + '_vix.csv',index_col='Date', header=0)
    g_isVixLoaded = True
    
    try:
        return g_vixDF.loc[date.strftime("%m/%d/%Y"),'VIX Close']
    except:
        g_isVixLoaded = True
        return 'NaN';


def main():
    #print getVixClosePrice('08/22/2017')
    #currDate = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%m/%d/%Y")
    #df_opt = Options('^VIX', 'yahoo')
    #data1 = df_opt.get_all_data()
    #print '1212121:' , data1
    date = (datetime.date.today() - datetime.timedelta(days=200))
    #endDate = (datetime.date.today() - datetime.timedelta(days=1))
    print 'for date:' , date
    #print currDate.strftime("%m/%d/%Y")
    #print getVIXClosePrice(date)
    #print df_vixClosePrice
    #print getStockClosePrice('UVXY', startDate)
    #print getOptClosePrice('UVXY', 'yahoo', '2018-03', 46 ).iloc[0]['Last']
    
      
    todays_date = datetime.datetime.now().date()
    dateArr = df.date_range(todays_date-datetime.timedelta(10), periods=10, freq='D')
    newFileName = './temp/positionFile.csv'
    #print index[1]
    
    #columns = ['pos_num','open_pos_date','vix_pos_price','uvxy_pos_price','uvxy_vix_pos_ratio','uvxy_vix_curr_pos','os_vix_qty','pos_vix_op_price','pos_vix_strick','pos_vix_exp','pos_uvxy_qty','pos_uvxy_op_price','pos_uvxy_strick','pos_uvxy_exp','pos_vix_amount','pos_uvxy_amount','curr_pos_vix_value','curr_pos_uvxy_value','days_pass','is_55_days_pass','pos_ratio*0.75 >=curr_ratio','pos_status','pos_gain']
    columns = ['pos_num','open_pos_date','vix_pos_price','uvxy_pos_price','uvxy_vix_pos_ratio','uvxy_vix_curr_pos','pos_vix_qty','pos_vix_op_price','pos_vix_strick','pos_vix_exp','pos_uvxy_qty','pos_uvxy_op_price','pos_uvxy_strick','pos_uvxy_exp','pos_vix_amount','pos_uvxy_amount','curr_pos_vix_value','curr_pos_uvxy_value','days_pass','is_55_days_pass','pos_ratio*0.75 >=curr_ratio','pos_status','pos_gain']
  
    np_array_list = []
    
    for i in range(len(dateArr)):
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
            curr_vix_op_price = getOptClosePrice('^VIX', 'yahoo', pos_vix_exp, pos_vix_strick ).iloc[0]['Last']
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
    big_frame.to_csv(newFileName,sep= '\t',header=True,index_label='open_pos_date')

    #df_ = pandas.DataFrame(result_array,index=index, columns=columns)
    #df_ = df_.fillna(0) # with 0s rather than NaNs
    print big_frame
    
main()














