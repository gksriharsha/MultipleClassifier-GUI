import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

def text2number(path=None,columns = None,data = None,le_data = False):
    
    if(data.__sizeof__ == 0):
        dataset = pd.read_csv(path)       
    else:
        dataset = data
    
    #column_names = list(dataset.columns)
    if(columns == None):        
        textcolumns = dataset.applymap(np.isreal)        
        for i in range(dataset.shape[1]):
            isNum = textcolumns.iloc[:,i]
            if(all(isNum)):
                pass
            else:
                le = LabelEncoder()
                transformed_column = le.fit_transform(dataset.iloc[:,i])
                dataset.iloc[:,i] = transformed_column                            
    
    else:
        for column in columns:
            le = LabelEncoder()
            transformed_column = le.fit_transform(dataset.iloc[:,column])
            dataset.iloc[:,column] = transformed_column    
    if(le_data == True):
        return (dataset,le)
    else:
        return dataset

def text2numberOHE(path,columns = None,classes=True):
    dataset = pd.read_csv(path)
    labels = []
    if(classes):
        labels = dataset.iloc[:,-1].to_frame()
        dataset = dataset.iloc[:,:-1]
        if(labels.apply(np.isreal).sum != len(labels)):
            labels = text2number(data=labels)
        
    column_names = list(dataset.columns)
    to_be_removed = []  
    if(columns == None):    
        textcolumns = dataset.applymap(np.isreal)         
        for i in range(dataset.shape[1]):
            isNum = textcolumns.iloc[:,i]
            if(all(isNum)):
                pass
            else:
                ohe_data = pd.get_dummies(dataset[column_names[i]],prefix=column_names[i])
                dataset = pd.concat([dataset,ohe_data],axis=1)
                to_be_removed.append(column_names[i])
                
        dataset.drop(columns=to_be_removed,axis=1, inplace=True)
        if(classes):
            pd.concat([dataset,labels],axis=1)            
    else:
        for column in columns:
            ohe_data = pd.get_dummies(dataset[column_names[column]],prefix=column_names[column])
            dataset = pd.concat([dataset,ohe_data],axis=1)
            to_be_removed.append(column_names[column])                
        dataset.drop(columns=to_be_removed,axis=1, inplace=True)          
    return dataset

def contains_text_check(path):
    dataset = pd.read_csv(path)
    textcolumns = dataset.applymap(np.isreal)    
    if(textcolumns.sum().sum() == textcolumns.shape[0]*textcolumns.shape[1]):
        return False
    else:
        return True
    
def getTextcols(path):
    dataset = pd.read_csv(path)
    textcolumns = []
    istextcolumns = dataset.applymap(np.isreal).sum()
    for i in range(len(istextcolumns)-1):
        if(istextcolumns[i] != dataset.shape[0]):
           textcolumns.append(i)           
    return textcolumns

def ensure_header(path=None,Data=None):
    dataset = pd.read_csv(path)
    #header_names = list(dataset.columns)
    try:
        #test = float(header_names[3])
        Column_headers = []
        for i in range(dataset.shape[1]):
            Column_headers.append('Column '+str(i))
        dataset.columns = Column_headers
    except Exception:
        pass
    dataset.to_csv(path,index=False)
    #return dataset
    
def ensure_numeric_labels(path):
    dataset = pd.read_csv(path,index_col=False)
    labels = dataset.iloc[:,-1].to_frame()
    dataset = dataset.iloc[:,:-1]
    if(labels.apply(np.isreal).sum != len(labels)):
        (labels,le) = text2number(data=labels,le_data=True)
    
    pd.DataFrame(le.classes_).to_csv('Label_metadata.csv')
    dataset = pd.concat([dataset,labels],axis=1)
    dataset.to_csv(path,index=False)   
    

def ensure_no_nans(path):
    dataset = pd.read_csv(path)
    dataset.fillna(dataset.mean())
    dataset.to_csv(path,index=False) 

def isfileOK_classify(path):
    if(not contains_text_check(path)):
        if(True):
            pass
