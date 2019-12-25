import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import multilabel_confusion_matrix
import json,codecs
import pickle
import FileChecks as checks

raw_file = []
data_test = []
data_train = []
label_test = []
label_train = []
labels = []
pred= []
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

def classify(paths):
    from sklearn.model_selection import train_test_split 
    global raw_file,label_test,label_train,data_test,data_train,cols,labels  
    cols = get_number_of_cols(paths[0])    
    
    with open('settings.json') as f:
        settings = json.load(f)
    user_settings = settings['User selected settings']
    classifier_settings = settings['Classifier settings']
    Encoder_settings = settings['Encoder']
    if(Encoder_settings != "Null"):
        raw_file = pd.read_csv(paths[0])
        if(Encoder_settings == "OHE"):
            raw_file = checks.text2numberOHE(paths[0])
        elif(Encoder_settings == "LE"):
            raw_file = checks.text2number(paths[0])
        elif(Encoder_settings == "OHE/LE"):
            raw_file1 = checks.text2numberOHE(paths[0],columns=list(settings["Encoder_OHE"]))
            raw_file = checks.text2number(data=raw_file1,columns=list(settings["Encoder_LE"]))
        else:
            pass
        raw_file.to_csv('data.csv',index_label=0)        
    if(user_settings['Number of files'] == "One file"):            
        dfs = np.split(raw_file,[cols-2],axis=1)
        data = dfs[0]
        labels = dfs[1]            
    else:
        labels = pd.read_csv(paths[1]).to_frame()
        if(labels.apply(np.isreal).sum != len(labels)):
            labels = checks.text2number(data=labels)
    
    data_train, data_test, label_train, label_test = train_test_split(data, labels, test_size=0.33, random_state=42)
    if(user_settings['Classifier'] == "KNN"):
        classify_KNN(classifier_settings)
    elif(user_settings['Classifier'] == "SVM"):
        classify_SVM(classifier_settings)
    elif(user_settings['Classifier'] == "MLP"):
        classify_MLP(classifier_settings)
    else:
        auto_classify(user_settings,paths)
        
    acc = accuracy_score(label_test,pred)*100
    classifier_results["Accuracy"] = acc
    fscore = f1_score(label_test,pred)*100
    classifier_results["F1 Score"] = fscore
    pscore = precision_score(label_test,pred)*100 
    classifier_results["Precision"] = pscore
    rscore = recall_score(label_test,pred)*100
    classifier_results["Recall"] = rscore
    conf_matrix = multilabel_confusion_matrix(label_test,pred)
    json.dump(conf_matrix.tolist(),codecs.open('/conf.json','w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
    write_results()
    print("End of classification")

def classify_KNN(classifier_settings):
    global classifier_results,data_test,data_train,label_test,label_train,pred
    from sklearn.neighbors import KNeighborsClassifier    
    if(bool(classifier_settings)):
        clf_KNN = KNeighborsClassifier(n_neighbors=classifier_settings['K'], weights=classifier_settings['weights'])
    else:
        clf_KNN = KNeighborsClassifier(n_neighbors=3)
    clf_KNN.fit(data_train,label_train)
    pickle.dump(clf_KNN,open('Model.mdl','wb'))
    pred = clf_KNN.predict(data_test)    
    

def classify_SVM(classifier_settings):
    global classifier_results,data_test,data_train,label_test,label_train,pred
    from sklearn.svm import SVC    
    if(bool(classifier_settings)):
        clf_SVM = SVC(degree=int(classifier_settings["Degree"]),tol=float(classifier_settings["tol"]))
    else:
        clf_SVM = SVC()
    clf_SVM.fit(data_train,label_train)
    pred = clf_SVM.predict(data_test)
    pickle.dump(clf_SVM,open('Model.mdl','wb'))


def classify_MLP(classifier_settings):
    global classifier_results,data_test,data_train,label_test,label_train,pred    
    from sklearn.neural_network import MLPClassifier
    if(bool(classifier_settings)):
        clf_MLP =  MLPClassifier(solver='lbfgs',hidden_layer_sizes=(5, 2),
                activation=classifier_settings['Activation Func.'],max_iter=int(classifier_settings['Iterations']),tol=float(classifier_settings['Tolerance']))
    else:
        clf_MLP =  MLPClassifier()
    clf_MLP.fit(data_train,label_train)
    pred = clf_MLP.predict(data_test)
    pickle.dump(clf_MLP,open('Model.mdl','wb'))
    
   
def auto_classify(user_settings,paths):
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
        classifier_settings = {}
        classifier_settings["Activation Func."] = "tanh"
        classifier_settings["Iterations"] = 200000
        classifier_settings["Tolerance"] = 0.00005
        classify_MLP(classifier_settings)
        classifier_results["selected classifier"] = "MLP"
    elif(NGI>1 and NGI <10):
        classifier_settings = {}
        classifier_settings["Degree"] = 11
        classifier_settings["tol"] = 0.0001
        classify_SVM(classifier_settings)
        classifier_results["selected classifier"] = "SVM"
    else:
        classifier_settings = {}
        classifier_settings["K"] = 27
        classifier_settings["weights"] = "distance"
        classify_KNN(classifier_settings)
        classifier_results["selected classifier"] = "KNN"
    settings = {}
    settings['Classifier settings'] = classifier_settings
    settings['User selected settings'] = user_settings
    write_settings(settings)  
def write_settings(settings):
    f = open("settings.json",'w+') 
    f.write(json.dumps(settings,indent=4))
    f.close() 
def write_results():
    f=open("results.json","w+")
    f.write(json.dumps(classifier_results,indent=4))
    f.close()
