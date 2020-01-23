import matplotlib as m
import pandas as pd
import numpy as np
from tkinter import ttk
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
    scaled = (dataset.max().max() <= 3)
    
    BasicFrame = ttk.LabelFrame(Insights_window,text = "Basic Insights of Dataset")
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
    
    PropertiesFrame = ttk.LabelFrame(Insights_window,text="Descriptive Statistics of data")
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
    ttk.OptionMenu(PropertiesFrame, Selected_column, *Columns,command= columnproperties).grid(row=0,column=1,pady=10)
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
    ttk.Button(PropertiesFrame,text="Plot",command=lambda:plotcolumn()).grid(columnspan=2,row=10)
        
    PropertiesFrame.pack()
