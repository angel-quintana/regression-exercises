import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import env

   
def get_zillow_data():
    '''
    loads zillow data from sql query as df
    '''
    url = env.get_db_url('zillow')
    query = '''
    select bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, taxvaluedollarcnt, yearbuilt, taxamount, fips
    from propertylandusetype
        join properties_2017
            using (propertylandusetypeid)
        WHERE propertylandusedesc = ("Single Family Residential")
    '''

    df = pd.read_sql(query, url)
    return df    
    
#functionize/wrangle - acquisition and preparation
def wrangle_zillow():
    '''
    returns clean df from get_zillow_data()
    '''
    zillow_df= get_zillow_data()

#blank space and nulls
    zillow_df = zillow_df.dropna()
    
#change datatypes to ints
    zillow_df.yearbuilt = zillow_df.yearbuilt.astype(int)
    zillow_df.bedroomcnt = zillow_df.bedroomcnt.astype(int)
    zillow_df.fips = zillow_df.fips.astype(int)
    zillow_df.taxvaluedollarcnt = zillow_df.taxvaluedollarcnt.astype(int)
    zillow_df.calculatedfinishedsquarefeet = zillow_df.calculatedfinishedsquarefeet.astype(int)
    
    return zillow_df

def splitting_data(df, col):
    '''
    input dataframe and target variable to stratify on
    returns 3 dataframes serving as train, validate, and test samples
    '''

    #first split
    train, validate_test = train_test_split(df,
                     train_size=0.6,
                     random_state=123,
                     stratify=df[col]
                    )
    
    #second split
    validate, test = train_test_split(validate_test,
                                     train_size=0.5,
                                      random_state=123,
                                      stratify=validate_test[col]
                        
                                     )
    return train, validate, test

