from tkinter import *
from tkinter import filedialog
import json
import Brains

root = Tk()
root.title("Classification Selection Tool")
root.minsize(350,250)
root.geometry("350x550")
height_widget = 150
width_widget = 250

global selectedclassifier 
selectedclassifier = StringVar()
selectedclassifier.set("Auto")

global fileoptn
fileoptn = StringVar() 
fileoptn.set("Two files")

global paths
paths = [' ']*2

global settings
global auto_generated_settings
global user_settings

settings = {}
user_settings = {}
auto_generated_settings = {}


def classifier_selection():
    classifierframe = LabelFrame(root,text="Choose the classifier",pady=10)
    classifierframe.config(height=height_widget,width=width_widget)
    

    classifiers = [
        ("SVM Classifier","SVM"),
        ("KNN Classifier","KNN"),
        ("MLP Classifier","MLP"),
        ("Auto Select", "Auto")]

    for classifier,value in classifiers:
        Radiobutton(classifierframe,text=classifier, variable=selectedclassifier,value=value).pack(anchor=W)

    classifierframe.pack_propagate(0)
    classifierframe.pack(pady=10)

   


        
def file_selection(): 

    fileframe = LabelFrame(root,text="Classifier Data Setup",pady=10)
    fileframe.config(height=300,width=width_widget)

    def file_number_choose(fileoptn):   
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
        root.filename = filedialog.askopenfilename(initialdir="/", title="Select Data for Classification", filetypes=(("csv files", "*.csv"),("all files", "*.*")))   
        paths[0] = root.filename        
        if(paths):            
            data_path.delete(0,END)
            data_path.insert(0,str(paths[0]))
            file_path_data.set(paths[0])
            
        Label(root, text=root.filename).pack()

    def label_openfile():
        root.filename = filedialog.askopenfilename(initialdir="/", title="Select Labels for Classification", filetypes=(("csv files", "*.csv"),("all files", "*.*")))   
        paths[1] = root.filename
        if(paths):
            label_path.delete(0,END)
            label_path.insert(0,str(paths[1]))
            file_path_labels.set(paths[1])
            
        Label(root, text=root.filename).pack()

    Radiobutton(fileframe,text="Data and Labels in single file",variable=fileoptn,value="One file",command=lambda :file_number_choose(fileoptn)).pack(anchor=W)
    Radiobutton(fileframe,text="Data and Labels as seperate files",variable = fileoptn,value="Two files",command=lambda :file_number_choose(fileoptn)).pack(anchor=W)

    data_button = Button(fileframe,text="Open Data file",command=data_openfile)
    label_button = Button(fileframe,text="Open Labels file",command=label_openfile)
    data_button.pack(padx=5,pady=10,anchor=W)
    data_path.pack(padx=5,pady=10,anchor=W)
    label_button.pack(padx=5,pady=10,anchor=W)
    label_path.pack(padx=5,pady=10,anchor=W)

   

    fileframe.pack_propagate(0)
    fileframe.pack()



def click_button():
    def clicked(value1,value2):
        myLabel = Label(root, text=value1+" "+value2)
        myLabel.pack()
        finalize()	
    myButton = Button(root, text="Classify", state=DISABLED,command=lambda: clicked(selectedclassifier.get(),fileoptn.get()))
    
    if((len(paths[1]) >= 10 and fileoptn.get() == "Two files") or (len(paths[0]) >= 10 and fileoptn.get() == "One file")):
        myButton.config(state=NORMAL)    
    myButton.pack(pady=10)

def write_settings():    
    user_settings['Number of files'] = fileoptn.get()
    user_settings['Classifier'] = selectedclassifier.get()
    auto_generated_settings['Features'] = Brains.get_number_of_cols(paths[0])
    settings['User selected settings'] = user_settings
def finalize():
    
    f = open("settings.json",'w+')
    print(json.dumps(settings,indent=4)) 
    f.write(json.dumps(settings,indent=4))
    f.close()
    write_settings()


classifier_selection()
file_selection()
click_button()


root.mainloop()
