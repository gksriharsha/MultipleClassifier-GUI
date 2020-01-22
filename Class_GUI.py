import sys,os
sys.path.append(os.path.join(sys.path[0],'UI'))
sys.path.append(os.path.join(sys.path[0],'Classification'))
sys.path.append(os.path.join(sys.path[0],'Checks'))

from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import numpy as np
from ttkthemes import themed_tk as tk
import json
import Brains
import DatasetInsights as insights
import additional_settings as Settings
import additional_results as results
import FileChecks as checks
root = tk.ThemedTk()
root.set_theme('plastik')
root.title("Classification Selection Tool")
root.geometry("350x700")
root.resizable(False,False)
height_widget = 175
width_widget = 250

classifier_settings = {}
selectedclassifier = StringVar()
selectedclassifier.set("Auto")

global fileoptn
fileoptn = StringVar() 
fileoptn.set("Two files")


paths = [' ']*2

global settings
global user_settings

settings = {}
settings["Encoder"] = "Null"
user_settings = {}

accuracy = StringVar()
classifier = StringVar()
classifier1 = StringVar()

Encoderoptn = StringVar()
Encoderoptn.set("OHE")   
Encoderoptn_select = StringVar()
Encoderoptn_select.set(None)
def classifier_selection():
    global selectedclassifier 
    classifierframe = ttk.LabelFrame(root,text="Choose the classifier")
    classifierframe.config(height=height_widget,width=width_widget)
    

    classifiers = [
        ("SVM Classifier","SVM"),
        ("KNN Classifier","KNN"),
        ("MLP Classifier","MLP"),
        ("Auto Select", "Auto")]

    
    
    def radio_settings():
        global classifier_settings
        if(selectedclassifier.get() == "MLP"):
            Settings_button.config(state=NORMAL)
            classifier_settings = {}
            classifier_settings["Activation Func."] = "tanh"
            classifier_settings["Iterations"] = 100000
            classifier_settings["Tolerance"] = 0.0001
        elif(selectedclassifier.get() == "SVM"):
            Settings_button.config(state=NORMAL)
            classifier_settings = {}
            classifier_settings["Degree"] = 3
            classifier_settings["tol"] = 0.0001
        elif(selectedclassifier.get() == "KNN"):
            Settings_button.config(state=NORMAL)
            classifier_settings = {}
            classifier_settings["K"] = 3
            classifier_settings["weights"] = "uniform"
        else:           
            Settings_button.config(state=DISABLED)           
        
        settings["Classifier settings"] = classifier_settings

    for classifier,value in classifiers:
        ttk.Radiobutton(classifierframe,text=classifier, variable=selectedclassifier,value=value,command=radio_settings).pack(pady=5,anchor=W)
    
    def settings_clicked():
        f = open("settings.json",'w+')
        f.write(json.dumps(settings,indent=4))
        f.close()
        Settings.additional_settings(selectedclassifier.get()) 
    Settings_button = ttk.Button(classifierframe,text="Additional Settings",
                     command=settings_clicked,state=DISABLED)
    Settings_button.pack(anchor=E,padx=10)

    classifierframe.pack_propagate(0)
    classifierframe.pack(pady=10)


def file_selection(): 

    fileframe = ttk.LabelFrame(root,text="Classifier Data Setup")
    fileframe.config(height=300,width=width_widget)

    def file_number_choose(fileoptn):  
        global paths 
        if(fileoptn.get() == "One file"):
            data_button.config(text="Open Data + Labels file")        
            label_button.config(state="disabled")
            file_path_labels.set("")
            file_path_data.set("")
            paths = [' ']*2               
        else:
            data_button.config(text="Open Data file")
            label_button.config(state="normal")
            file_path_labels.set("")
            file_path_data.set("")
            paths = [' ']*2                   
    file_path_data = StringVar()
    file_path_labels = StringVar()
    data_path = ttk.Entry(fileframe,state='readonly',width=80,textvariable=file_path_data)
    label_path = ttk.Entry(fileframe,state='readonly',width=80,textvariable=file_path_labels)

    def data_openfile():
        global paths
        root.filename = filedialog.askopenfilename(initialdir="/", title="Select Data for Classification", filetypes=(("csv files", "*.csv"),("all files", "*.*")))   
        paths[0] = root.filename        
        if(paths):            
            data_path.delete(0,END)
            data_path.insert(0,str(paths[0]))
            file_path_data.set(paths[0])
        if(not (paths[0] == '')):
            checks.ensure_header(paths[0])
        file_check()
            
    def file_check():
        columnVar = StringVar()                        
        global paths
        if(not (paths[0] == '')):
            checks.ensure_no_nans(paths[0])
            if((checks.contains_text_check(paths[0])) and (checks.getTextcols(paths[0]) == [])):
                    data = checks.ensure_numeric_labels(paths[0])
            if(( checks.contains_text_check(paths[0])) and (checks.getTextcols(paths[0]) != [])):                   
                ErrorWindow = Toplevel(pady=10,padx=5)
                ErrorWindow.grab_set()
                ErrorWindow.title("Encoder Window")     
                OHE_cols = []
                LE_cols = []           
                Colselect = Entry(ErrorWindow,textvariable=columnVar,state='readonly')
                columns = checks.getTextcols(paths[0]) 
                def encselect():
                    if(Encoderoptn.get() == "OHE"):
                        settings["Encoder"] = "OHE"
                        R1.config(state=DISABLED)
                        R2.config(state=DISABLED)
                        B.config(state = DISABLED)
                        Close.config(state=NORMAL) 
                    elif(Encoderoptn.get() == "LE"):
                        settings["Encoder"] = "LE"
                        R1.config(state=DISABLED)
                        R2.config(state=DISABLED) 
                        B.config(state = DISABLED)
                        Close.config(state=NORMAL) 
                    elif(Encoderoptn.get() == "OHE/LE"):
                        settings["Encoder"] = "OHE/LE"
                        columnVar.set(columns[0])
                        R1.config(state=NORMAL)
                        R2.config(state=NORMAL)
                        B.config(state = NORMAL)
                        Close.config(state = DISABLED)
                    else:
                        pass
                
                def encselect2(columns):                    
                    choice = Encoderoptn_select.get() 
                    if(choice == "OHE"):
                        OHE_cols.append(int(columnVar.get()))
                    elif(choice == "LE"):
                        LE_cols.append(int(columnVar.get()))
                    else:
                        pass 
                    columns = np.setdiff1d(np.setdiff1d(columns,OHE_cols),LE_cols)                                
                    if(columns.size == 0):
                        columnVar.set(None) 
                        settings["Encoder_OHE"] = OHE_cols
                        settings["Encoder_LE"] = LE_cols 
                        B.config(state=DISABLED)
                        Close.config(state = NORMAL)                      
                    else:                        
                        columnVar.set(columns[0])                    
                    Encoderoptn_select.set(None)
                B = ttk.Button(ErrorWindow,text="Submit",command=lambda:encselect2(columns),state=DISABLED)
                R1 = ttk.Radiobutton(ErrorWindow,text="Text labels do not have a relationship",variable=Encoderoptn_select,value="OHE",state=DISABLED)
                R2 = ttk.Radiobutton(ErrorWindow,text="Text labels do have a relationship",variable = Encoderoptn_select,value="LE",state=DISABLED)                                                                
                Close = ttk.Button(ErrorWindow,text="Close Window",command=ErrorWindow.destroy)
                ttk.Radiobutton(ErrorWindow,text="Text labels do not have a relationship",variable=Encoderoptn,value="OHE",command=encselect).pack(anchor=W)
                ttk.Radiobutton(ErrorWindow,text="Text labels do have a relationship",variable = Encoderoptn,value="LE",command=encselect).pack(anchor=W)
                if(len(columns) > 20):
                    ttk.Radiobutton(ErrorWindow,text="Choose for each column seperately",variable = Encoderoptn,value="OHE/LE",state=DISABLED).pack(anchor=W)
                else:
                    ttk.Radiobutton(ErrorWindow,text="Choose for each column seperately",variable = Encoderoptn,value="OHE/LE",state=NORMAL,command=encselect).pack(anchor=W)
                ttk.Label(ErrorWindow,text="Column").pack(anchor=W,pady=10)                
                Colselect.pack(anchor=W,pady=5)
                R1.pack(anchor=W)
                R2.pack(anchor=W)
                B.pack(anchor=S,pady=5)
                Close.pack(anchor=S,pady=10)
      
    def label_openfile():
        global paths
        root.filename = filedialog.askopenfilename(initialdir="/", title="Select Labels for Classification", filetypes=(("csv files", "*.csv"),("all files", "*.*")))   
        paths[1] = root.filename
        if(paths):
            label_path.delete(0,END)
            label_path.insert(0,str(paths[1]))
            file_path_labels.set(paths[1])
        if(not (paths[0] == '')):
            checks.ensure_header(paths[1])
        file_check()
            
    ttk.Radiobutton(fileframe,text="Data and Labels in single file",variable=fileoptn,value="One file",command=lambda :file_number_choose(fileoptn)).pack(anchor=W)
    ttk.Radiobutton(fileframe,text="Data and Labels as seperate files",variable = fileoptn,value="Two files",command=lambda :file_number_choose(fileoptn)).pack(anchor=W)

    data_button = ttk.Button(fileframe,text="Open Data file",command=data_openfile)
    label_button = ttk.Button(fileframe,text="Open Labels file",command=label_openfile)
    Insights_button = ttk.Button(fileframe,text="Dataset Properties",command=lambda: insights.getInsights(paths[0]),state=DISABLED)
    data_button.pack(padx=5,pady=10,anchor=W)
    data_path.pack(padx=5,pady=10,anchor=W)
    label_button.pack(padx=5,pady=10,anchor=W)
    label_path.pack(padx=5,pady=10,anchor=W)
    Insights_button.pack(padx=5,anchor=S)
    
    def insight_check(self):
        if((len(paths[1]) >= 2 and fileoptn.get() == "Two files") or
            (len(paths[0]) >= 2 and fileoptn.get() == "One file")):
            Insights_button.config(state=NORMAL)
        else:
            Insights_button.config(state=DISABLED)
    root.bind("<Enter>",insight_check,add=True)
    fileframe.pack_propagate(0)
    fileframe.pack()

def mini_results():
    global accuracy
    
    miniresultsFrame = ttk.LabelFrame(root,text="Results")  
    miniresultsFrame.config(height=100,width=width_widget)
            
    ttk.Label(miniresultsFrame,text="Classifier used:    ").grid(row=0,column=0,pady=10)
    Entry(miniresultsFrame,textvariable=classifier,state='readonly',width=10,relief=FLAT).grid(row=0,column=1,pady=10)
    Entry(miniresultsFrame,textvariable=classifier1,state='readonly',width=10,relief=FLAT).grid(row=0,column=2,pady=10)
    ttk.Label(miniresultsFrame,text="Accuracy:    ").grid(row=1,column=0)
    Entry(miniresultsFrame,textvariable=accuracy,relief=FLAT,state='readonly').grid(row=1,column=1,pady=10,columnspan=2)
    
    resultsbutton = ttk.Button(miniresultsFrame,text="Detailed Results",command=lambda:results.showresults(),state=DISABLED)
    resultsbutton.grid(row=2,column=0,columnspan=3)
       
    def results_check(self):
        resultsbutton.config(state=NORMAL)
    root.bind('<<Activate Results>>',results_check)
    miniresultsFrame.pack_propagate(0)
    #miniresultsFrame.grid_propagate(False)
    miniresultsFrame.pack()      
def click_button():
    def classify():
        write_settings()
        finalize()
    
    myButton = ttk.Button(root, text="Classify", state=DISABLED,command=classify)
    
    def button_check(self):
        if((len(paths[1]) >= 2 and fileoptn.get() == "Two files") or
            (len(paths[0]) >= 2 and fileoptn.get() == "One file")):
            myButton.config(state=NORMAL)
        else:
            myButton.config(state=DISABLED)
    root.bind("<Enter>",button_check,add=True)    
    myButton.pack(pady=10)

def write_settings():
    global selectedclassifier     
    user_settings['Number of files'] = fileoptn.get()
    user_settings['Classifier'] = selectedclassifier.get()
    settings['User selected settings'] = user_settings
    if(Settings.classifier_settings == {}):
        pass
    else:
        settings['Classifier settings'] = Settings.classifier_settings
    try:
        classifier_settings = settings['Classifier settings']
    except:
        settings['Classifier settings'] = {}
    f = open("settings.json",'w+')
    f.write(json.dumps(settings,indent=4))
    f.close() 

def finalize():
   
    Brains.classify(paths)
    root.event_generate('<<Activate Results>>',when='tail')
    with open('results.json','r') as f:
       results = json.load(f)
       
    global accuracy,classifier
    accuracy.set(str("%0.3f" % results['Accuracy'])+' %')
    classifier.set(settings["User selected settings"]["Classifier"])
    if(settings["User selected settings"]["Classifier"] == "Auto"):
        classifier1.set(results["selected classifier"])   
    else:
        classifier1.set("") 

    
    
classifier_selection()
file_selection()
click_button()
mini_results()


root.mainloop()