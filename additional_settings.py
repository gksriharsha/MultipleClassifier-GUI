from tkinter import *
import json
try:
    classifier_settings
except:
    classifier_settings = {} 
def isint(number):
    try:
        if(number is None or number is ""):
            return True               
        return float(number).is_integer() 
    except:
        return False

def isfloat(number):
    try:
        if(number is None or number is ""):
            return True   
        float(number)
        return True
    except:
        return False

def SVM(settings_window):
    degree_SVM = IntVar()
    degree_SVM.set(3)
    tol_SVM = DoubleVar()
    tol_SVM.set(0.0001)
    reg = settings_window.register(isint)
    reg2 = settings_window.register(isfloat)    
    def SVM_close():
        global classifier_settings
        classifier_settings = {}
        classifier_settings["Degree"] = degree_SVM.get()        
        classifier_settings["tol"] = tol_SVM.get()
        print(json.dumps(classifier_settings,indent=4))
        settings_window.destroy()
    Label(settings_window,text="Degree:    ").grid(row=0,column=0)
    Entry(settings_window,textvariable=degree_SVM,validate="key",vcmd=(reg,'%P')).grid(row=0,column=1,pady=10)
    Label(settings_window,text="Tolerance:    ").grid(row=1,column=0)
    Entry(settings_window,textvariable=tol_SVM,validate="key",vcmd=(reg2,'%P')).grid(row=1,column=1,pady=10)
    Button(settings_window,text="Save and close",command=SVM_close).grid(row=2,column=0,columnspan=2,pady=10)

def KNN(settings_window):
    K_KNN = IntVar()
    K_KNN.set(classifier_settings['K'])
    fn = StringVar()
    reg = settings_window.register(isint)
    reg2 = settings_window.register(isfloat)    
    def KNN_close():
        global classifier_settings
        classifier_settings = {}
        classifier_settings['K'] = K_KNN.get()
        classifier_settings['weights'] = fn.get()
        print(json.dumps(classifier_settings,indent=4))
        settings_window.destroy()
    Label(settings_window,text="N neighbors:    ").grid(row=0,column=0)
    Entry(settings_window,textvariable=K_KNN,validate="key",vcmd=(reg,'%P')).grid(row=0,column=1,pady=10)
    Label(settings_window,text="Weights :    ").grid(row=1,column=0)
    weights =  [
                    "uniform", 
                    "distance"                                           
                ]            
    fn.set(weights[0])
    OptionMenu(settings_window, fn, *weights).grid(row=1,column=1,pady=10)
    Button(settings_window,text="Save and close",command=KNN_close).grid(row=2,column=0,columnspan=2,pady=10)

def MLP(settings_window):
    fn = StringVar()
    Iter = IntVar()
    Iter.set(int(classifier_settings["Iterations"]))
    tol_MLP = DoubleVar()
    tol_MLP.set(float(classifier_settings["Tolerance"]))
    reg = settings_window.register(isint)
    reg2 = settings_window.register(isfloat)    
    def MLP_close():
        global classifier_settings
        classifier_settings = {}
        classifier_settings["Activation Func."] = fn.get()
        classifier_settings["Iterations"] = Iter.get()
        classifier_settings["Tolerance"] = tol_MLP.get()
        print(json.dumps(classifier_settings,indent=4))
        settings_window.destroy()
    Label(settings_window,text="Activation func. :    ").grid(row=0,column=0)
    activation =  [
                    "relu", 
                    "tanh", 
                    "logistic", 
                    "identity"                           
                ]            
    fn.set(classifier_settings['Activation Func.'])
    OptionMenu(settings_window, fn, *activation).grid(row=0,column=1,pady=10)
    Label(settings_window,text="Max Iterations:    ").grid(row=1,column=0,pady=10)
    Entry(settings_window,textvariable=Iter,validate="key",vcmd=(reg,'%P')).grid(row=1,column=1,pady=10)
    Label(settings_window,text="Tolerance:    ").grid(row=2,column=0,pady=10)
    Entry(settings_window,textvariable=tol_MLP,validate="key",vcmd=(reg2,'%P')).grid(row=2,column=1,pady=10)
    Button(settings_window,text="Save and close",command=MLP_close).grid(row=3,column=0,columnspan=2,pady=10)

def additional_settings(value):
    global classifier_settings
    with open('settings.json') as f:
        classifier_settings = json.load(f)
    settings_window = Toplevel(padx=10,pady=10)
    settings_window.grab_set()
    settings_window.resizable(False,False)       
    settings_window.title('Classifier Settings')
        
    if(value == "SVM"):
        SVM(settings_window)
    elif(value == "KNN"):
        KNN(settings_window)
    elif(value == "MLP"):
        MLP(settings_window)
    else:
        pass
        
    
