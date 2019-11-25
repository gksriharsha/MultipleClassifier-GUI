from tkinter import *
from tkinter import filedialog

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
paths = []

def classifier_selection():
    classifierframe = LabelFrame(root)
    classifierframe.config(height=height_widget,width=width_widget)
    classifierframe.pack_propagate(0)

    classificationlabel = Label(classifierframe,text="Choose the classifier required")
    classificationlabel.pack()

    classifiers = [
        ("SVM Classifier","SVM"),
        ("KNN Classifier","KNN"),
        ("MLP Classifier","MLP"),
        ("Auto Select", "Auto")]

    for classifier,value in classifiers:
        Radiobutton(classifierframe,text=classifier, variable=selectedclassifier,value=value).pack(anchor=W)

    classifierframe.pack(pady=10)

   

def data_openfile():
    root.filename = filedialog.askopenfilename(initialdir="/", title="Select Data for Classification", filetypes=(("csv files", "*.csv"),("all files", "*.*")))   
    paths.append(root.filename)
    Label(root, text=root.filename).pack()

def label_openfile():
    root.filename = filedialog.askopenfilename(initialdir="/", title="Select Labels for Classification", filetypes=(("csv files", "*.csv"),("all files", "*.*")))   
    paths.append(root.filename)
    Label(root, text=root.filename).pack()

        
def file_selection(): 

    def file_number_choose(fileoptn):   
        if(fileoptn.get() == "One file"):
            data_button.config(text="Open Data + Labels file")        
            label_button.config(state="disabled")
            paths.clear()   
        else:
            data_button.config(text="Open Data file")
            label_button.config(state="normal")
            paths.clear()        

    fileframe = LabelFrame(root)
    fileframe.config(height=height_widget,width=width_widget)
    
    Radiobutton(fileframe,text="Data and Labels in single file",variable=fileoptn,value="One file",command=lambda :file_number_choose(fileoptn)).pack(anchor=W)
    Radiobutton(fileframe,text="Data and Labels as seperate files",variable = fileoptn,value="Two files",command=lambda :file_number_choose(fileoptn)).pack(anchor=W)
    data_button = Button(fileframe,text="Open Data file",command=data_openfile)
    label_button = Button(fileframe,text="Open Labels file",command=label_openfile)
    data_button.pack(padx=5,pady=10,anchor=W)
    label_button.pack(padx=5,pady=10,anchor=W)

    fileframe.pack_propagate(0)
    fileframe.pack()



def click_button():
    def clicked(value1,value2):
        myLabel = Label(root, text=value1+" "+value2)
        myLabel.pack()	

    myButton = Button(root, text="Click Me!", command=lambda: clicked(selectedclassifier.get(),fileoptn.get()))
    myButton.pack(pady=10)

classifier_selection()
file_selection()
click_button()
root.mainloop()
