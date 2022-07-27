#from acquire import *

import pandas as pd
import numpy as np
import os
from env import host, user, password

#function uses info from env.py file to create a connection url to access db

def get_connection(db, user=user, host=host, password=password):
    
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

##reads in telco data from db, writed data to csv in no local file exists, returns a df
def get_telco_data():
    
    if os.path.isfile('telco.csv'):
        #if csv exists read in data
        df = pd.read_csv('telco.csv', index_col=0)
        
    else:
        #read in fresh data from db to df
        df = new_telco_data()
        #cache data
        df.to_csv('telco.csv')
        
    return df

def get_zillow_data():
    """Seeks to read the cached zillow.csv first """
    filename = "zillow.csv"

    if os.path.isfile(filename):
        return pd.read_csv(filename)
    else:
        return get_new_zillow_data()

def get_new_zillow_data():
    """Returns a dataframe of all 2017 properties that are Single Family Residential"""

    sql = """
    select 
    bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, taxvaluedollarcnt, yearbuilt, taxamount, fips
    from properties_2017
    join propertylandusetype using (propertylandusetypeid)
    where propertylandusedesc = "Single Family Residential"
    """
    return pd.read_sql(sql, get_db_url("zillow"))