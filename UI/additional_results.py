from tkinter import Label, LabelFrame,Toplevel
import json,codecs
import numpy as np

def showresults():
    with open('results.json','r') as f:
        results = json.load(f)
    with open('settings.json') as f:
        settings = json.load(f)
    results_window = Toplevel()
    results_window.grab_set()

    summaryframe = LabelFrame(results_window,text="Parameters of Classification",pady=10,width=250)
    
    Label(summaryframe,text="Classifier used:    ").grid(row=0,column=0,pady=10)
    Label(summaryframe,text=settings["User selected settings"]["Classifier"]).grid(row=0,column=1,pady=10)
    if(settings["User selected settings"]["Classifier"] == "Auto"):
        Label(summaryframe,text=results["selected classifier"]).grid(row=0,column=2,pady=10)
      
    try:
        i=2
        Label(summaryframe,text="Classifier settings:    ").grid(row=1,column=0)
        for key,value in settings["Classifier settings"].items():
            Label(summaryframe,text=key).grid(row=i,column=0,pady=5)
            Label(summaryframe,text=value).grid(row=i,column=1,pady=5)
            i = i+1
    except Exception:
        #print("Exception raised")
        #print(e)
        pass
    
    summaryframe.pack(padx=10,pady=10)
    
    obj_text = codecs.open('/conf.json', 'r', encoding='utf-8').read()
    b_new = json.loads(obj_text)
    conf = np.array(b_new)
    
    resultsframe = LabelFrame(results_window,text="Results of Classification",pady=10,width=250)
    Label(summaryframe,text="Classification results:    ").grid(row=1,column=0)
    Label(summaryframe,text='Confusion Matrix').grid(row=2,column=0,pady=5)
    Label(summaryframe,text= conf).grid(row=2,column=1,pady=5)
    
    i = 3
    for key,value in results.items():
        if(key == "selected classifier"):
            pass
        Label(summaryframe,text=key).grid(row=i,column=0,pady=5)
        Label(summaryframe,text=value).grid(row=i,column=1,pady=5)
        i = i+1
    
    resultsframe.pack(pady=10,padx=10)      


