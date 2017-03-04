'''
Title: class_def.py
Created: 13/02/2017
Purpose: Class for import of data
Packages used: 
    - Pandas
Changes needed:
Changes made:
'''
# Packages
import pandas as pd

# Classes
class data_load(object):
    '''
    Class for loading the data so that we can access in a way like
    data.train.features, data.train.target
    By default will not load test
    By default will choose the last column as the target
    '''
    
    def __init__(self, train_loc, test_loc = None, target_col = None):
        class data_train(object): # so call this later for the init of parent
            def __init__(self, train_loc, target_col):
                
                print "Loading train data"
                data = pd.read_csv(train_loc)
                print "Loaded", len(data), "rows"
                
                if not target_col:
                    target_col = data.columns[-1]
                    print "Defaulting target_col to", target_col
                    
                self.features = data.drop(target_col, axis = 1)
                self.target = data[target_col]
                self.target_name = target_col
            
        class data_test(object):
            def __init__(self, test_loc, target_col):
                print "Loading test data"
                data = pd.read_csv(test_loc)
                print "Loaded", len(data), "rows"
                
                if target_col in data:
                    print "Target provided"
                    self.features = data.drop(target_col, axis = 1)
                    self.target = data[target_col]
                else:
                    print "Target not provided"
                    self.features = data
        
                
        self.train = data_train(train_loc, target_col)
        
        if test_loc:
            self.test = data_test(test_loc, self.train.target_name)



