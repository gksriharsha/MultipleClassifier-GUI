import matplotlib as m
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from tkinter import *
import matplotlib
matplotlib.use("TkAgg")

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def getInsights(path):
    Insights_window = Toplevel(pady=10,padx=5)
    Insights_window.grab_set()
    
    dataset = pd.read_csv(path)
    NAs = dataset.isnull().sum().sum()
    Total_elts = dataset.shape[0]*dataset.shape[1]
    scaled = (dataset.max().max() <= 1)
    
    BasicFrame = LabelFrame(Insights_window,text = "Basic Insights of Dataset",padx=10,pady=10)
    Label(BasicFrame,text="Rows:    ").grid(row=0,column=0,pady=10)
    Label(BasicFrame,text=str(dataset.shape[0])).grid(row=0,column=1,pady=10)
    Label(BasicFrame,text="Columns:    ").grid(row=1,column=0,pady=10)
    Label(BasicFrame,text=str(dataset.shape[1])).grid(row=1,column=1,pady=10)
    Label(BasicFrame,text="Total Elements:    ").grid(row=2,column=0,pady=10)
    Label(BasicFrame,text=str(Total_elts)).grid(row=2,column=1,pady=10)
    Label(BasicFrame,text="NAN Elements:    ").grid(row=3,column=0,pady=10)
    Label(BasicFrame,text=(str(NAs)+' elements ('+str(NAs*100.0/Total_elts)+" % of the dataset)")).grid(row=3,column=1,pady=10)
    Label(BasicFrame,text="Text Elements:    ").grid(row=4,column=0,pady=10)
    Label(BasicFrame,text=str(Total_elts - dataset.applymap(np.isreal).sum().sum())).grid(row=4,column=1,pady=10)    
    Label(BasicFrame,text="Scaled Data:    ").grid(row=4,column=0,pady=10)
    Label(BasicFrame,text=scaled).grid(row=4,column=1,pady=10)    
    BasicFrame.pack()
    
    PropertiesFrame = LabelFrame(Insights_window,text="Descriptive Statistics of data",padx=10,pady=10)
    Columns = list(dataset.columns)
    Selected_column = StringVar()
    Mean = StringVar()
    Std = StringVar()
    Median = StringVar()
    Quartile1 = StringVar()
    Quartile3 = StringVar()
    Nunique = IntVar()
    
    def columnproperties(self):
        col = dataset[Selected_column.get()]        
        Mean.set(str("%.3f" % col.mean()))
        Std.set(str("%.4f" % col.std()))
        Quartile1.set(str("%.4f" % col.quantile(0.25)))
        Median.set(str("%.4f" % col.median()))
        Quartile3.set(str("%.4f" % col.quantile(0.75)))
        Nunique.set(col.nunique())
        
    def plotcolumn():
        col = dataset[Selected_column.get()]
        graph_window = Toplevel()
        graph_window.resizable(False,False)
        graph_window.grab_set()
        figure = Figure(figsize=(5, 4), dpi=100)
        plot = figure.add_subplot(1, 1, 1)
        plot.plot(list(range(len(col))), list(col.values), color="red", marker="o", linestyle="")
        canvas = FigureCanvasTkAgg(figure, graph_window)
        canvas.get_tk_widget().grid(row=0, column=0)
        #dataset.plot(y=Selected_column.get()) 
           
    Label(PropertiesFrame,text="Select Column for analysis:    ").grid(row=0,column=0,pady=10)
    OptionMenu(PropertiesFrame, Selected_column, *Columns,command= columnproperties).grid(row=0,column=1,pady=10)
    Label(PropertiesFrame,text="Mean:    ").grid(row=1,column=0,pady=10)
    Entry(PropertiesFrame,textvariable=Mean,relief=FLAT,state='readonly').grid(row=1,column=1,pady=10)
    Label(PropertiesFrame,text="Standard Deviation:    ").grid(row=2,column=0,pady=10)
    Entry(PropertiesFrame,textvariable=Std,relief=FLAT,state='readonly').grid(row=2,column=1,pady=10)
    Label(PropertiesFrame,text="1st Quartile:    ").grid(row=3,column=0,pady=10)
    Entry(PropertiesFrame,textvariable=Quartile1,relief=FLAT,state='readonly').grid(row=3,column=1,pady=10)
    Label(PropertiesFrame,text="Median:    ").grid(row=4,column=0,pady=10)
    Entry(PropertiesFrame,textvariable=Median,relief=FLAT,state='readonly').grid(row=4,column=1,pady=10)
    Label(PropertiesFrame,text="3rd Quartile:    ").grid(row=5,column=0,pady=10)
    Entry(PropertiesFrame,textvariable=Median,relief=FLAT,state='readonly').grid(row=4,column=1,pady=10)
    Label(PropertiesFrame,text="Unique Values:    ").grid(row=5,column=0,pady=10)
    Entry(PropertiesFrame,textvariable=Nunique,relief=FLAT,state='readonly').grid(row=5,column=1,pady=10)
    Button(PropertiesFrame,text="Plot",command=lambda:plotcolumn()).grid(columnspan=2,row=10)
        
    PropertiesFrame.pack()

def text2number(path,columns = None):
    dataset = pd.read_csv(path)
    column_names = list(dataset.columns)
    if(columns == None):        
        textcolumns = dataset.applymap(np.isreal)        
        for i in range(dataset.shape[1]):
            isNum = textcolumns.iloc[:,i]
            if(all(isNum)):
                pass
            else:
                col = dataset[dataset.iloc[:,i].name]
                uniq = col.nunique()
                if(uniq==2):
                    le = LabelEncoder()
                    transformed_column = le.fit_transform(dataset.iloc[:,i])
                    dataset.iloc[:,i] = transformed_column                            
    else:
        for column in columns:
            le = LabelEncoder()
            transformed_column = le.fit_transform(dataset.iloc[:,column])
            dataset.iloc[:,column] = transformed_column         
    return dataset

def text2numberOHE(path,columns = None):
    dataset = pd.read_csv(path)
    column_names = list(dataset.columns)
    to_be_removed = []  
    if(columns == None):    
        textcolumns = dataset.applymap(np.isreal)         
        for i in range(dataset.shape[1]-1):
            isNum = textcolumns.iloc[:,i]
            if(all(isNum)):
                pass
            else:
                ohe_data = pd.get_dummies(dataset[column_names[i]],prefix=column_names[i])
                dataset = pd.concat([dataset,ohe_data],axis=1)
                to_be_removed.append(column_names[i])
                
        dataset.drop(columns=to_be_removed,axis=1, inplace=True)            
    else:
        for column in columns:
            ohe_data = pd.get_dummies(dataset[column_names[column]],prefix=column_names[column])
            dataset = pd.concat([dataset,ohe_data],axis=1)
            to_be_removed.append(column_names[column])                
        dataset.drop(columns=to_be_removed,axis=1, inplace=True)          
    return dataset
