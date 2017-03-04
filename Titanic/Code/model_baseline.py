'''
Title: model_baseline.py
Created: 14/02/2017
Purpose: Script for baseline models
Packages used: 
    - 
Changes needed:
    - Should modify variables fed in to "unpack" - literally feed a dictionary
      and then unpack - if don't specify, then will default
    - Need to convert factor variables / drop variables for training
Changes made:
'''

# Packages
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Directory
dir_path = "C:/Users/amathewl/Desktop/kaggle/Titanic/Code" 
os.chdir(dir_path)

# Scripts
import data_prep

def model_all_survive(train_X, train_y, test_X, 
                      seed = 123, **kwargs):
    '''
    Baseline model asigning all 1
    '''
    np.random.seed(seed)
    return [1]*len(test_X)
    
def model_random_survive(train_X, train_y, test_X,
                         seed = 123, other_args = {}):
    '''
    Baseline model asigning randomly - note that p should be 2 long list
    '''
    np.random.seed(seed)
    # Defaults
    arguments = {'p' : None}
    for arg in other_args.keys():
        arguments[arg] = other_args[arg]
            
    return np.random.choice([0,1], len(test_X), p = arguments['p'])
    
def model_random_forest_baseline(train_X, train_y, test_X,
                                 seed = 123, mod_args = {}, other_args = {}):
    '''
    Baseline model asigning randomly - note that weight should be 2d array
    '''
    np.random.seed(seed)
    # Defaults
    arguments = {'threshold' : 0.5}
    for arg in other_args.keys():
        arguments[arg] = other_args[arg]
    
    # Data prep
    to_remove = ['PassengerId', 'Name', 'Ticket', 'Cabin']
    to_numeric = ['Embarked', 'Sex']
    train_X = data_prep.model_prep(train_X, to_remove, to_numeric)
    test_X = data_prep.model_prep(test_X, to_remove, to_numeric)
        
    random_forest = RandomForestClassifier(**mod_args)
                                           
    random_forest.fit(train_X, train_y)
    prob_y = predict_proba(test_X)
    
    return [1 if p > arguments["threshold"] else 0 for p in prob_y]
    
