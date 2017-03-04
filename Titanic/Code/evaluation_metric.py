'''
Title: evaluation_metric.py
Created: 14/02/2017
Purpose: Script for generating folds, predictions, and evaluating
Packages used: 
    - sklearn.model_selection
    - sklearn.metrics
Changes needed:
    - produce a graph of roc curve?
    - graph the AUC and accuracy
Changes made:
'''
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, roc_auc_score

def get_folds(train_data, **kwargs):
    '''
    Function to return folds on data previously loaded in with the class format
    '''
    # Defaults
    arguments = {"n_splits" : 2, "shuffle" : False, "random_state" : None}
    for arg in arguments:
        if arg in kwargs.keys():
            arguments[arg] = kwargs[arg]
    
    
    skf = StratifiedKFold(arguments["n_splits"], arguments["shuffle"], arguments["random_state"])
    data_folds = {}
    i = 0
    for train_i, test_i in skf.split(train_data.features, train_data.target):
        i += 1
        name = "fold_" + str(i)
        
        data_folds[name] = {"train" : {"X" : train_data.features.iloc[train_i], "y" : train_data.target.iloc[train_i]},
                            "test" : {"X" : train_data.features.iloc[test_i], "y" : train_data.target.iloc[test_i]}}
                            
        print "folder number:", i
        print "train X dim:", data_folds[name]["train"]["X"].shape, "Y dim", data_folds[name]["train"]["y"].shape
        print "test X dim:", data_folds[name]["test"]["X"].shape, "Y dim", data_folds[name]["test"]["y"].shape
        print "\n"
    return data_folds

# get_folds(data.train)

def evaluate_model(train_data, model, **kwargs):
    '''
    Function to evaluate a model using cross validation
    note that should feed a function that returns predictions
    note that function should take in the training and test sets
    '''
    eval_data = get_folds(train_data)
    eval_metrics = pd.DataFrame()
    for fold in eval_data.keys():
        train_X = eval_data[fold]["train"]["X"]
        train_y = eval_data[fold]["train"]["y"]
        test_X = eval_data[fold]["test"]["X"]
        test_y = eval_data[fold]["test"]["y"]
        
        pred_y = model(train_X, train_y, test_X, kwargs = kwargs)
        
        fold_eval = pd.DataFrame({"fold" : [fold],
                                  "accuracy" : [accuracy_score(test_y, pred_y)], 
                                  "auc" : [roc_auc_score(test_y, pred_y)]})
                                  
        eval_metrics = eval_metrics.append(fold_eval)
    
    for score in eval_metrics.drop("fold", axis = 1).columns:
        print "Average", score, ":", eval_metrics[score].mean()
        print "Standard deviation", score, ":", eval_metrics[score].std()
        print "Mean SD", score, ":", eval_metrics[score].std() / (len(eval_metrics[score])**0.5)
        
    return eval_metrics
    
evaluate_model(data.train, model_random_forest_baseline)


