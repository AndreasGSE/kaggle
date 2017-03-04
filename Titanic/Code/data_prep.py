'''
Title: data_prep.py
Created: 14/02/2017
Purpose: Script for preparing data - removing columns and featurising
Packages used: 
    - 
Changes needed:
    - must be a better way to encode factors
    - treat nulls - I THINK SHOULD FEED IN BOTH TRAIN AND TEST - test if right
    - standardisation / mean removal
    - encoding into vectors (features)
    - polynomial (features)
Changes made:

Ideas
    - Note that we should keep this outside of all other functions
      because varied model creation could depend on prep etc.
'''

# Packages
import pandas as pd
from sklearn.preprocessing import Imputer

def model_prep(data, remove_feature, factor_feature):
    '''
    Function to remove columns as well as make factors numerics
    This is NOT a feature creation wrapper - nor a normaliser -
    nor does it create "one hots" as can see those as additional features
    Note that DATA should be fed in - not just the train
    '''
    data.features.drop(remove_feature, axis = 1, inplace = True)
    
    for feature in factor_feature:
        unique_factors = set(data.features[feature])
        repl_dic = {factor : code for code, factor in enumerate(unique_factors)}
        data.features[feature] = data.features[feature].replace(repl_dic)
        
    return data
        
def treat_nulls(data_train, data_test, strategy = {}):
    for feature in strategy.keys():
        imp = Imputer(missing_values = 'NaN', axis = 0)
        if strategy[feature] == 'average':
            imp.set_params(strategy = 'strategy__mean')
            
        if strategy[feature] == 'median':
            imp.set_params(strategy = 'strategy__median')
            
        if strategy[feature] == 'mode':
            imp.set_params(strategy = 'strategy__most_frequent')
            
        if strategy[feature] == 'remove':
            data_train.features.dropna(subset = [feature], inplace = True)
            data_test.features.dropna(subset = [feature], inplace = True)
        
        else: # if not remove
            imp.fit(data_train.features[feature])
            data_train.features[feature] = imp.transform(data_train.features[feature])
            data_test.features[feature] = imp.transform(data_test.features[feature])
            
        
    return imp.transform(data_train), imp.transform(data_test)
