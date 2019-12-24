from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import themed_tk as tk
import json
import Brains
import DatasetInsights as insights
import additional_settings as Settings
import additional_results as results
root = Tk()
root.title("Classification Selection Tool")
root.geometry("350x725")
#root.resizable(False,False)
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
user_settings = {}

accuracy = StringVar()
classifier = StringVar()
classifier1 = StringVar()

def classifier_selection():
    global selectedclassifier 
    classifierframe = LabelFrame(root,text="Choose the classifier",pady=10)
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
        Radiobutton(classifierframe,text=classifier, variable=selectedclassifier,value=value,command=radio_settings).pack(anchor=W)
    
    def settings_clicked():
        f = open("settings.json",'w+')
        print(json.dumps(settings,indent=4)) 
        f.write(json.dumps(settings,indent=4))
        f.close()
        Settings.additional_settings(selectedclassifier.get()) 
    Settings_button = Button(classifierframe,text="Additional Settings",
                     command=settings_clicked,state=DISABLED)
    Settings_button.pack(anchor=E,padx=10)

    

    classifierframe.pack_propagate(0)
    classifierframe.pack(pady=10)


def file_selection(): 

    fileframe = LabelFrame(root,text="Classifier Data Setup",pady=10)
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
    data_path = Entry(fileframe,state='readonly',relief=SUNKEN,width=80,textvariable=file_path_data)
    label_path = Entry(fileframe,state='readonly',relief=SUNKEN,width=80,textvariable=file_path_labels)

    def data_openfile():
        global paths
        root.filename = filedialog.askopenfilename(initialdir="/", title="Select Data for Classification", filetypes=(("csv files", "*.csv"),("all files", "*.*")))   
        paths[0] = root.filename        
        if(paths):            
            data_path.delete(0,END)
            data_path.insert(0,str(paths[0]))
            file_path_data.set(paths[0])
            
        

    def label_openfile():
        global paths
        root.filename = filedialog.askopenfilename(initialdir="/", title="Select Labels for Classification", filetypes=(("csv files", "*.csv"),("all files", "*.*")))   
        paths[1] = root.filename
        if(paths):
            label_path.delete(0,END)
            label_path.insert(0,str(paths[1]))
            file_path_labels.set(paths[1])
            
    Radiobutton(fileframe,text="Data and Labels in single file",variable=fileoptn,value="One file",command=lambda :file_number_choose(fileoptn)).pack(anchor=W)
    Radiobutton(fileframe,text="Data and Labels as seperate files",variable = fileoptn,value="Two files",command=lambda :file_number_choose(fileoptn)).pack(anchor=W)

    data_button = Button(fileframe,text="Open Data file",command=data_openfile)
    label_button = Button(fileframe,text="Open Labels file",command=label_openfile)
    Insights_button = Button(fileframe,text="Dataset Properties",command=lambda: insights.getInsights(paths[0]))
    data_button.pack(padx=5,pady=10,anchor=W)
    data_path.pack(padx=5,pady=10,anchor=W)
    label_button.pack(padx=5,pady=10,anchor=W)
    label_path.pack(padx=5,pady=10,anchor=W)
    Insights_button.pack(padx=5,anchor=S)

    fileframe.pack_propagate(0)
    fileframe.pack()

def mini_results():
    global accuracy
    
    resultsFrame = LabelFrame(root,text="Results",pady=10)
    #resultsFrame.config(width=250)
    
   
    with open('settings.json') as f:
        settings = json.load(f)    
        
    Label(resultsFrame,text="Classifier used:    ").grid(row=0,column=0,pady=10)
    Entry(resultsFrame,textvariable=classifier,relief=FLAT,state='readonly').grid(row=0,column=1,pady=10)
    if(settings["User selected settings"]["Classifier"] == "Auto"):
        Entry(resultsFrame,textvariable=classifier1,relief=FLAT,state='readonly').grid(row=0,column=2,pady=10)
    Label(resultsFrame,text="Accuracy:    ").grid(row=1,column=0)
    Entry(resultsFrame,textvariable=accuracy,relief=FLAT,state='readonly').grid(row=1,column=1,pady=10)
    
    resultsFrame.pack_propagate(0)
    resultsFrame.pack()      
def click_button():
    def classify():
        write_settings()
        finalize()

      
    myButton = Button(root, text="Classify", state=DISABLED,command=classify)
    
    def button_check(self):
        if((len(paths[1]) >= 2 and fileoptn.get() == "Two files") or (len(paths[0]) >= 2 and fileoptn.get() == "One file")):
            myButton.config(state=NORMAL)
        else:
            myButton.config(state=DISABLED)
    root.bind("<Enter>",button_check)    
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
    f = open("settings.json",'w+')
    print(json.dumps(settings,indent=4)) 
    f.write(json.dumps(settings,indent=4))
    f.close() 

def finalize():
    Brains.classify(paths,user_settings,Settings.classifier_settings)
    
    with open('results.json','r') as f:
       results = json.load(f)
       
    global accuracy,classifier
    accuracy.set(str("%0.3f" % results['Accuracy'])+' %')
    classifier.set(settings["User selected settings"]["Classifier"])
    classifier1.set(results["selected classifier"])
    #results.showresults()    

    
    
classifier_selection()
file_selection()
click_button()
mini_results()


root.mainloop()