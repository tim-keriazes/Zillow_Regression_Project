from sklearn.model_selection import train_test_split
import pandas as pd
import os
from sklearn.preprocessing import MinMaxScaler
import sklearn.preprocessing
from env import user, password, host

def get_db_url(database):
    return f'mysql+pymysql://{user}:{password}@{host}/{database}'

"""
USAGE: 
Use `from wrangle import wrangle_zillow` at the top of your notebook.
This 
"""
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


def handle_nulls(df):    
    # We keep 99.41% of the data after dropping nulls
    # round(df.dropna().shape[0] / df.shape[0], 4) returned .9941
    df = df.dropna()
    return df


def optimize_types(df):
    # Convert some columns to integers
    # fips, yearbuilt, and bedrooms can be integers
    df["fips"] = df["fips"].astype(str)
    df["yearbuilt"] = df["yearbuilt"].astype(int)
    df["bedroomcnt"] = df["bedroomcnt"].astype(int)    
    df["taxvaluedollarcnt"] = df["taxvaluedollarcnt"].astype(int)
    df["calculatedfinishedsquarefeet"] = df["calculatedfinishedsquarefeet"].astype(int)
    return df


def handle_outliers(df):
    """Manually handle outliers that do not represent properties likely for 99% of buyers and zillow visitors"""
    df = df[df.bathroomcnt <= 6]
    
    df = df[df.bedroomcnt <= 6]

    df = df[df.taxvaluedollarcnt < 1_500_000]

    df.drop(df.loc[df.calculatedfinishedsquarefeet >25000].index, inplace=True)

    df.drop(df.loc[df['bedroomcnt']==0].index, inplace=True)
    
    df.drop(df.loc[df['bathroomcnt']==0].index, inplace=True)

    return df


def wrangle_zillow():
    """
    Acquires Zillow data
    Handles nulls
    optimizes or fixes data types
    handles outliers w/ manual logic
    returns a clean dataframe
    """
    df = get_zillow_data()

    df = handle_nulls(df)

    df = optimize_types(df)

    df = handle_outliers(df)

    #new column total bill divided by size
    df['cost_per_sqft'] = (df['taxvaluedollarcnt']/df['calculatedfinishedsquarefeet']).round(2)

    #avg sqft per number of rooms (bedroom+bathroom)
    df['sqft_room_ratio'] = (df['calculatedfinishedsquarefeet']/(df['bedroomcnt']+df['bathroomcnt'])).round(2)

    #dummy encode fips
    fipsdummies = pd.get_dummies(df.fips)
    df = pd.concat([df,dummies],axis=1)

   # df.to_csv("zillow.csv", index=False)
   #rename columns for ease of use
    df=df.rename(columns={"bedroomcnt": "bedrooms", "bathroomcnt": "bathrooms", "calculatedfinishedsquarefeet": "sqft","taxvaluedollarcnt": "home_value"})

    return df

def split(df, stratify_by=None):
    """
    Crude train, validate, test split
    To stratify, send in a column name for the stratify_by argument
    """

    if stratify_by == None:
        train, test = train_test_split(df, test_size=.2, random_state=123)
        train, validate = train_test_split(train, test_size=.3, random_state=123)
    else:
        train, test = train_test_split(df, test_size=.2, random_state=123, stratify=df[stratify_by])
        train, validate = train_test_split(train, test_size=.3, random_state=123, stratify=train[stratify_by])

    return train, validate, test

def scale_zillow(train, validate, test):
    '''
    scale_zillow will 
    - fits a min-max scaler to the train split
    - transforms all three spits using that scaler. 
    returns: 3 dataframes with the same column names and scaled values. 
    '''
    
    scaler = sklearn.preprocessing.MinMaxScaler()
    
    # Note that we only call .fit with the TRAINING data,
    scaler.fit(train)
    
    # but we use .transform to apply the scaling to all the data splits.    
    train_scaled = scaler.transform(train)
    validate_scaled = scaler.transform(validate)
    test_scaled = scaler.transform(test)
    
    # convert to arrays to pandas DFs
    train_scaled = pd.DataFrame(train_scaled, columns=train.columns)
    validate_scaled = pd.DataFrame(validate_scaled, columns=train.columns)
    test_scaled = pd.DataFrame(test_scaled, columns=train.columns)
    
    return train_scaled, validate_scaled, test_scaled






## TODO Encode categorical variables (and FIPS is a category so Fips to string to one-hot-encoding
## TODO Scale numeric columns
## TODO Add train/validate/test split in here
## TODO How to handle 0 bedroom, 0 bathroom homes? Drop them? How many? They're probably clerical nulls

# #new column total bill divided by size
# df['cost_per_sqft'] = (df['taxvaluedollarcnt']/df['calculatedfinishedsquarefeet']).round(2)

# #avg sqft per number of rooms (bedroom+bathroom)
# df['sqft_room_ratio'] = (df['calculatedfinishedsquarefeet']/(df['bedroomcnt']+df['bathroomcnt'])).round(2)


# (df.bedroomcnt == 0).value_counts()
# (df.bathroomcnt == 0).value_counts()
# (df['bedroomcnt']==0)&(df['bathroomcnt']==0)

# #at this point after digging into whether or not i can or should impute the 
# # values of the averages based on squarefootage or just drop them

# df.drop(df.loc[df['bedroomcnt']==0].index, inplace=True)
# df.drop(df.loc[df['bathroomcnt']==0].index, inplace=True)

# def select_kbest(X_train, y_train, k):
#     # parameters: f_regression stats test, give me 2 features
#     f_selector = SelectKBest(f_regression, k=k)
# # find the top 8 X's correlated with y
#     f_selector.fit(X_train, y_train)
# # boolean mask of whether the column was selected or not. 
#     feature_mask = f_selector.get_support()
# # get list of top K features. 
#     f_feature = X_train.iloc[:,feature_mask].columns.tolist()
#     return f_feature

# def rfe (X_train, y_train, k):
#     # initialize the ML algorithm
#     lm = LinearRegression()
# # create the rfe object, indicating the ML object (lm) and the number of features I want to end up with. 
#     rfe = RFE(lm, n_features_to_select=k)
# # fit the data using RFE
#     rfe.fit(X_train,y_train)  
# # get the mask of the columns selected
#     feature_mask = rfe.support_
# # get list of the column names. 
#     rfe_feature = X_train.iloc[:,feature_mask].columns.tolist()
#     return rfe_feature
