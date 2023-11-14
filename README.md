# Zillow House Value Investigation

### **Project Description**
An ML Regression model that predicts property tax assessed values  of Single Family Properties using attributes of the properties.

### **Project Goal**
To find a regression model that can predict the value of a single family property with a much higher accuracy than the baseline prediction. 

### **Initial Hypotheses** 
1. There is a relationship between square footage and taxvalue.
2. There is a relationship between the number of bedrooms and taxvalue.
3. There is a relationship between the number of bathrooms and taxvalue.

### **Project Plan**
#### 1. Acquire

- get the data into pandas
- look at it
    - describe, info, head, shape
- understand what your data means
    - know what each column is
    - know what your target variable is
#### 2. Wrangle
- clean the data
    - handle nulls
    - handle outliers
    - correct datatypes
- univariate analysis (looking at only one variable)
- encode variables -- Preprocessing
- split into train, validate/, test
- scale data (after train/validate/test split) -- Preprocessing
- document how you're changing the data
#### 3. Explore
- use train data
    - use unscaled data
- establish relationships using multivariate analysis
    - hypothesize
    - visualize
    - statistize
    - summarize
- feature engineering
    - use scaled data
#### 4. Model

- use scaled/encoded data
- split into X_variables and y_variables
    - X_train, y_train, X_validate, y_validate, X_test, y_test
- build models
    - make
    - fit (on train)
    - use
- evaluate models on train and validate
- pick the best model and evaluate it on test
#### 5. Test
- present results of the best model

### **Data Dictionary**
# Data Dictionary


| Feature | Definition |
|:--------|:-----------|
| id | Unique identifier for a property record |
| bedroomcnt, bedrooms | The number of bedrooms in the property |
| bathroomcnt, bathrooms | The number of bathrooms in the property, including partial bathrooms |
| calculatedfinishedsquarefeet, sqft | The total square footage of the property as calculated from public records |
| yearbuilt | The year the property was originally constructed |
| fips, county | Federal Information Processing Standards code representing the county in which the property is located |
| latitude | The latitude coordinate of the property |
| longitude | The longitude coordinate of the property |
| transactiondate, transaction_date | The date the property transaction was recorded |
| propertylandusedesc, property_class | The type or use of land the property is classified under |
| taxvaluedollarcnt, **taxvalue** | The total tax assessed value of the property |
| percentile_rank  | The percentile rank of the property based on the house square feet |


### **Steps to Reproduce**
1. Download this notebook and Wrgangle.py
2. Obtain the required 2017 zillow data needed from Zillow or CodeUP
3. Run it

### Takeaways
There is a correlation between square footage and taxvalue
Gradient Boosting Regressor performed the best with my data set
### Conclusion and Next Steps
Overall my regression model performs good. Its predictions beat the baseline model by 16%
In the future, I would consider the Lasso Lars Regressor model.
To imporove prediction results I would recommend to pull more features from the database and see if home remodeling can be a factor to drive taxvalue.
Also I would focus on making a model that is more stable than the current.