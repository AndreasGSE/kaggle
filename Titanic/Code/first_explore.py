'''
Title: first_explore.py
Created: 13/02/2017
Purpose: Take a first look at the data
Packages used: 
    - os
    - matplotlib
    - numpy
    - collections
Changes needed:
    - display number of entries, number of nulls
Changes made:
'''
# Packages
import os
import matplotlib.pyplot as plt
import numpy as np
import collections
from __future__ import division

# Directory
dir_path = "C:/Users/amathewl/Desktop/kaggle/Titanic/Code" 
os.chdir(dir_path)

# Scripts
import class_def

# Constants
train_loc = "../Data/train.csv"
test_loc = "../Data/test.csv"
target_col = "Survived"
out_file = "../Statistics/feature_stats.csv"

# Load data
data = class_def.data_load(train_loc, test_loc, target_col)

# Get distribution of each
variable_stats = [["Feature", "Num null", "Prct null", "Num unique", "Prct unique", "Mode",
                  "Num mode", "Prct mode", "Mean", "SD"]]
for feature in data.train.features:
    file_name = "../Figures/" + feature + "_dist.png"
    print "Printing distribution for", feature,"to\n", file_name
    
    # Graph text
    num_null = sum(data.train.features[feature].isnull())
    total_regs = len(data.train.features[feature].dropna())
    num_unique = len(set(data.train.features[feature]))
    
    fig = plt.figure(figsize=(16, 12))
    if data.train.features[feature].dtype == 'O' or num_unique / total_regs < 0.1:
        x = collections.Counter(data.train.features[feature].dropna())
        l = range(len(x.keys()))
        plt.bar(l, x.values(), align = 'center')
        plt.xticks(l, x.keys(), rotation = 'vertical')
    else:
        plt.hist(data.train.features[feature].dropna())
        
    
    text_string = "$Number of NaN: " + str(num_null) + "$\n$Number of unique: " + str(num_unique) + "$\n$Numer of non-null: " + str(total_regs) + "$"
    plt.annotate(text_string, xy = (1,1.12), xycoords = "axes fraction",
                 horizontalalignment = "right", verticalalignment = "top", size = 16)
    plt.title(feature)
    plt.savefig(file_name)
    plt.close(fig)
    
    # Create Excel that generalises the variables
    print "Getting stats for", feature
    if data.train.features[feature].dtype != 'O' and num_unique / total_regs > 0.1:
        x = collections.Counter(data.train.features[feature].dropna())
        average = data.train.features[feature].dropna().mean()
        stan_d = data.train.features[feature].dropna().std()
    else:
        average = "TEXT"
        stan_d = "TEXT"
    
    val_mode = x.most_common(1)[0][0]
    num_mode = x.most_common(1)[0][1]
    total = len(data.train.features[feature])
    
    variable_stats.append([feature, num_null, 100*num_null / total, num_unique, 100*num_unique / total,
                           val_mode, num_mode, 100*num_mode / total, average, stan_d])
                           
    print "\n\n"

pd.DataFrame(variable_stats[1:], columns = variable_stats[0]).to_csv(out_file, index = False)
    


    


























