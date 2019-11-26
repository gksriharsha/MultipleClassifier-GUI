import pandas as pd
import numpy as np

def get_number_of_cols(path):
    file = pd.read_csv(path,nrows=1)
    return len(file)

def get_number_of_rows(path):
    file = pd.read_csv(path)
    return (file.shape)[1]

def get_number_of_classes(path):
    cols = get_number_of_cols(path)
    file = pd.read_csv(path)   
    classes = len(np.unique(file.iloc[:,cols-1]))
    return classes

""" def search_classes(path):
    cols = get_number_of_cols(path)
    file = pd.read_csv(path)
    unique_list = [0] * cols
    for ind in reversed(range(cols)):
        column = file.iloc[:,ind]
        unique_list[ind] = len(np.unique(column)) 
    temp_list = unique_list
    temp_list.sort()
    return unique_list.index(temp_list[0:5]) """