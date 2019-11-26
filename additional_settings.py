from tkinter import *
def isint(number):
    try:               
        return float(number).is_integer() 
    except:
        return False

def isfloat(number):
    try:
        float(number)
        return True
    except:
        return False

        

def additional_settings(value):
        settings_window = Toplevel()
        settings_window.grab_set()
        #settings_window.geometry("250x150")
        #settings_window.minsize(150,150)
        settings_window.title('Classifier Settings')
        reg = settings_window.register(isint)
        reg2 = settings_window.register(isfloat)        
        if(value == "SVM"):
            degree_SVM = IntVar()
            degree_SVM.set(3)
            tol_SVM = DoubleVar()
            tol_SVM.set(0.001)
            def SVM_close():
                classifier_settings["Degree "] = degree_SVM.get()
                classifier_settings["tol"] = tol_SVM.get()
                settings_window.destroy()
            Label(settings_window,text="Degree:    ").grid(row=0,column=0)
            Entry(settings_window,textvariable=degree_SVM,validate="key",vcmd=(reg,'%P')).grid(row=0,column=1,pady=10)
            Label(settings_window,text="Tolerance:    ").grid(row=1,column=0)
            Entry(settings_window,textvariable=tol_SVM,validate="key",vcmd=(reg2,'%P')).grid(row=1,column=1,pady=10)
            Button(settings_window,text="Save and close",command=SVM_close).grid(row=2,column=0,columnspan=2,pady=10)
        elif(value == "KNN"):
            K_KNN = IntVar()
            def KNN_close():
                classifier_settings["K"] = K_KNN.get()
                settings_window.destroy()
            Label(settings_window,text="N neighbors:    ").grid(row=0,column=0)
            Entry(settings_window,textvariable=K_KNN,validate="key",vcmd=(reg,'%P')).grid(row=0,column=1,pady=10)
            Button(settings_window,text="Save and close",command=KNN_close).grid(row=1,column=0,columnspan=2,pady=10)
        elif(value == "MLP"):
            fn = StringVar()
            Iter = IntVar()
            tol_MLP = DoubleVar()
            def MLP_close():
                classifier_settings["fn"] = fn.get()
                classifier_settings["Iterations"] = Iter.get()
                classifier_settings["Tolerance"] = tol_MLP.get()
                settings_window.destroy()
            Label(settings_window,text="Activation func. :    ").grid(row=0,column=0)
            activation =  [
                            "Relu", 
                            "Tanh", 
                            "Logistic", 
                            "Identity"                           
                        ]            
            fn.set(activation[0])
            OptionMenu(settings_window, fn, *activation).grid(row=0,column=1,pady=10)
            Label(settings_window,text="Max Iterations:    ").grid(row=1,column=0,pady=10)
            Entry(settings_window,textvariable=Iter,validate="key",vcmd=(reg,'%P')).grid(row=1,column=1,pady=10)
            Label(settings_window,text="Tolerance:    ").grid(row=2,column=0,pady=10)
            Entry(settings_window,textvariable=tol_MLP,validate="key",vcmd=(reg2,'%P')).grid(row=2,column=1,pady=10)
            Button(settings_window,text="Save and close",command=MLP_close).grid(row=3,column=0,columnspan=2,pady=10)
        else:
            pass
    