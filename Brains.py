import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
import json
import os

raw_file = []
data_test = []
data_train = []
label_test = []
label_train = []
labels = []
classifier_results = {}
rows = 0
cols = 0
classes = 0
def get_number_of_cols(path):
    global cols
    file = pd.read_csv(path,nrows=1)
    cols = len(file)
    return cols

def get_number_of_rows(path):
    global rows
    file = pd.read_csv(path)
    rows = file.shape[1]
    return rows

def get_number_of_classes(path):
    cols = get_number_of_cols(path)
    global classes
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
def big_data_classify():
    print("File size too large - Module under implementation")

def classify(paths,user_settings,classifier_settings):
    from sklearn.model_selection import train_test_split 
    global raw_file,label_test,label_train,data_test,data_train,cols,labels  
    cols = get_number_of_cols(paths[0])
    file_size = os.stat(paths[0]).st_size/(1024*1024)
    if(file_size<1):
        if(user_settings["Headers"] == "Yes"):
            raw_file = pd.read_csv(paths[0],skiprows=1)
            if(user_settings['Number of files'] == "One file"):            
                dfs = np.split(raw_file,[cols-2],axis=1)
                data = dfs[0]
                labels = dfs[1]            
            else:
                labels = pd.read_csv(paths[1],skiprows=1)
        else:
            raw_file = pd.read_csv(paths[0])
            if(user_settings['Number of files'] == "One file"):            
                dfs = np.split(raw_file,[cols-2],axis=1)
                data = dfs[0]
                labels = dfs[1]
            else:
                labels = pd.read_csv(paths[1])    
    else:
        big_data_classify()        
    
    data_train, data_test, label_train, label_test = train_test_split(data, labels, test_size=0.33, random_state=42)
    if(user_settings['Classifier'] == "KNN"):
        classify_KNN(classifier_settings)
    elif(user_settings['Classifier'] == "SVM"):
        classify_SVM(classifier_settings)
    elif(user_settings['Classifier'] == "MLP"):
        classify_MLP(classifier_settings)
    else:
        auto_classify(paths)
    print("End of classification")
    write_results()

def classify_KNN(classifier_settings):
    global classifier_results,data_test,data_train,label_test,label_train
    from sklearn.neighbors import KNeighborsClassifier    
    if(bool(classifier_settings)):
        clf_KNN = KNeighborsClassifier(n_neighbors=classifier_settings['K'], weights=classifier_settings['weights'])
    else:
        clf_KNN = KNeighborsClassifier(n_neighbors=3)
    clf_KNN.fit(data_train,label_train)
    pred = clf_KNN.predict(data_test)    
    acc = accuracy_score(label_test,pred)*100
    classifier_results["Accuracy"] = acc
    print(acc)
    #return classifier_results

def classify_SVM(classifier_settings):
    global classifier_results,data_test,data_train,label_test,label_train
    from sklearn.svm import SVC    
    if(bool(classifier_settings)):
        clf_SVM = SVC(degree=int(classifier_settings["Degree"]),tol=float(classifier_settings["tol"]))
    else:
        clf_SVM = SVC()
    clf_SVM.fit(data_train,label_train)
    pred = clf_SVM.predict(data_test)
    acc = accuracy_score(label_test,pred)*100
    classifier_results["Accuracy"] = acc
    print(acc)
    #return classifier_results

def classify_MLP(classifier_settings):
    global classifier_results,data_test,data_train,label_test,label_train    
    from sklearn.neural_network import MLPClassifier
    if(bool(classifier_settings)):
        clf_MLP =  MLPClassifier(solver='lbfgs',hidden_layer_sizes=(5, 2),
                activation=classifier_settings['Activation Func.'],max_iter=int(classifier_settings['Iterations']),tol=float(classifier_settings['Tolerance']))
    else:
        clf_MLP =  MLPClassifier()
    clf_MLP.fit(data_train,label_train)
    pred = clf_MLP.predict(data_test)
    acc = accuracy_score(label_test,pred)*100
    classifier_results["Accuracy"] = acc
    print(acc)
    #return classifier_results

def auto_classify(paths):
    global classes,cols,rows,classifier_results
    classifier_settings = {}
    if(classes == 0):
        classes = len(np.unique(labels))
    if(cols == 0):
        cols = get_number_of_cols(paths[1] if len(paths[1])>5 else paths[0])
    if(rows == 0):
        rows = len(labels)
    
    NGI = rows/(classes*cols)

    if(NGI<1):
        classify_MLP(classifier_settings)
        classifier_results["selected classifier"] = "MLP"
    elif(NGI>1 and NGI <10):
        classify_SVM(classifier_settings)
        classifier_results["selected classifier"] = "SVM"
    else:
        classify_KNN(classifier_settings)
        classifier_results["selected classifier"] = "KNN"

def write_results():
    f=open("results.json","w+")
    f.write(json.dumps(classifier_results,indent=4))
    f.close()
