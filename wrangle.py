## IMPORTS ##
##-------------------------------------------------------------------##
#tabular data imports :
import pandas as pd
import numpy as np
import env
from env import user, password, host
from pydataset import data

# visualization imports:
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn.preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LassoLars, TweedieRegressor
from sklearn.feature_selection import SelectKBest, RFE, f_regression, SequentialFeatureSelector
# success metrics from earlier in the week: mean squared error and r^2 explained variance
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.preprocessing import PolynomialFeatures

from scipy.stats import pearsonr, spearmanr
from scipy.stats import shapiro

import warnings
warnings.filterwarnings("ignore")
import wrangle as w
import os
directory = os.getcwd()

## FUNCTIONS ##
##-------------------------------------------------------------------##
def get_db_url(database_name):
    """
    this function will:
    - take in a string database_name 
    - return a string connection url to be used with sqlalchemy later.
    """
    return f'mysql+pymysql://{user}:{password}@{host}/{database_name}'

def new_zillow_data():
    """
    This function will:
    - take in a SQL_query
    - create a connection_url to mySQL
    - return a df of the given query from the zillow
    """
    sql_query = """
      WITH RankedProperties AS (
    SELECT 
        p.id, 
        p.bedroomcnt, 
        p.bathroomcnt,
        p.calculatedfinishedsquarefeet, 
        p.yearbuilt,
        p.lotsizesquarefeet,
        p.fips,
        p.latitude,
        p.longitude,
        pr.transactiondate,
        plt.propertylandusedesc,
        p.taxvaluedollarcnt,
        PERCENT_RANK() OVER (ORDER BY p.calculatedfinishedsquarefeet) AS percentile_rank
    FROM properties_2017 AS p
    JOIN predictions_2017 AS pr ON p.id = pr.id
    JOIN propertylandusetype AS plt ON p.propertylandusetypeid = plt.propertylandusetypeid
    WHERE p.propertylandusetypeid IN (246, 247, 260, 261, 262, 263, 264, 265, 266, 275, 279)
      AND YEAR(pr.transactiondate) = 2017
      AND p.id IS NOT NULL
      AND p.bedroomcnt IS NOT NULL
      AND p.bathroomcnt IS NOT NULL
      AND p.calculatedfinishedsquarefeet IS NOT NULL
      AND p.yearbuilt IS NOT NULL
      AND p.lotsizesquarefeet IS NOT NULL
      AND p.fips IS NOT NULL
      AND pr.transactiondate IS NOT NULL
      AND plt.propertylandusedesc IS NOT NULL
      AND p.bathroomcnt > 0
)

SELECT * FROM RankedProperties
WHERE percentile_rank > 0.01 AND percentile_rank < 0.99;"""
    
    url = get_db_url('zillow')
    
    df = pd.read_sql(sql_query, url)
    
    return df


def get_zillow_data():
    """
    This function will:
    - Check local directory for csv file
        - return if exists
    - if csv doesn't exist:
        - creates df of sql query
        - writes df to csv
    - outputs zillow df
    """
    filename = 'zillow_2017.csv'
    
    if os.path.isfile(filename): 
        df = pd.read_csv(filename, index_col=0)
        return df
    else:
        df = new_zillow_data()

        df.to_csv(filename)
    return df

def prep_zillow(df):
    '''
    This function takes in a dataframe
    renames the columns and drops nulls values
    Additionally it changes datatypes for appropriate columns
    and renames fips to actual county names.
    Then returns a cleaned dataframe
    '''
    df = df.rename(columns = 
                   {'bedroomcnt':'bedrooms',
                    'bathroomcnt':'bathrooms',
                    'lotsizesquarefeet':'lot_sqft',
                    'propertylandusedesc':'property_class',
                    'calculatedfinishedsquarefeet':'sqft',
                    'taxvaluedollarcnt':'taxvalue',
                    'transactiondate':'transaction_date',
                    'fips':'county'})
    
    df = df.dropna()
    
    make_ints = ['bedrooms','sqft','taxvalue','yearbuilt','lot_sqft']

    for col in make_ints:
        df[col] = df[col].astype(int)
        
    df.county = df.county.map({6037:'LA',6059:'Orange',6111:'Ventura'})
    
    return df


def split_data(df):
    '''
    take in a DataFrame and return train, validate, and test DataFrames.
    return train, validate, test DataFrames.
    '''
    
    # Create train_validate and test datasets
    train, validate_test = train_test_split(df, train_size=0.60, random_state=123)
    
    # Create train and validate datsets
    validate, test = train_test_split(validate_test, test_size=0.5, random_state=123)

    # Take a look at your split datasets

    print(f"""
    train -> {train.shape}
    validate -> {validate.shape}
    test -> {test.shape}""")
    
    return train, validate, test