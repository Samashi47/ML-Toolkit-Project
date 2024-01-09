import tkinter as tk
import customtkinter as ctk
from sklearn.preprocessing import Normalizer, StandardScaler, minmax_scale, maxabs_scale
import pandas as pd
import preprocessing.ppframe as ppf
import re

class NormSCFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent,fg_color='transparent',corner_radius=20)
        
        self.seph = tk.ttk.Separator(self, orient='horizontal', style='TSeparator')
        self.seph.place(relx=0.01, rely=0.55, width=1260, bordermode="outside")
        self.sepv = tk.ttk.Separator(self, orient='vertical', style='TSeparator')
        self.sepv.place(relx=0.42, rely=0.01, height=720, bordermode="outside")
        
        self.norm_label = ctk.CTkLabel(self,font=('Arial',20),text="Normalizer: ")
        self.norm_label.place(anchor="center",relx=0.22, rely=0.08)
        
        self.Norm_label = ctk.CTkLabel(self,font=('Arial',17),text="Norm: ")
        self.Norm_label.place(anchor="center",relx=0.02, rely=0.3)
        self.norm_optMenu = ctk.CTkOptionMenu(self,width=190,height=30,values=["l1","l2","max"])
        self.norm_optMenu.configure(fg_color="#200E3A")
        self.norm_optMenu.place(relx=0.12, rely=0.31, anchor="center")
        self.nCols_label = ctk.CTkLabel(self,font=('Arial',17),text="Target: ")
        self.nCols_label.place(anchor="center",relx=0.23, rely=0.3)
        self.nCols_optMenu = ctk.CTkOptionMenu(self, width=190, height=30,values=[],dynamic_resizing=True)
        self.nCols_optMenu.configure(fg_color="#200E3A")
        self.nCols_optMenu.place(relx=0.335, rely=0.31, anchor="center")
        self.norm_button = ctk.CTkButton(master=self,text='Normalize',font=('Arial',15),width=190,height=30,command=lambda:self.applyNorm(str(self.norm_optMenu.get()),str(self.nCols_optMenu.get())))
        self.norm_button.configure(fg_color="#200E3A")
        self.norm_button.place(anchor="center",relx=0.22, rely=0.48)
        
        self.sc_label = ctk.CTkLabel(self,font=('Arial',20),text="Standard Scaler: ")
        self.sc_label.place(anchor="center",relx=0.22, rely=0.6)
        self.withMean_label = ctk.CTkLabel(self,font=('Arial',17),text="with_mean: ")
        self.withMean_label.place(anchor="center",relx=0.06, rely=0.71)
        self.sc_optMenu = ctk.CTkOptionMenu(self,width=120,height=30,values=["True","False"])
        self.sc_optMenu.configure(fg_color="#200E3A")
        self.sc_optMenu.place(relx=0.15, rely=0.72, anchor="center")
        self.withStd_label = ctk.CTkLabel(self,font=('Arial',17),text="with_std: ")
        self.withStd_label.place(anchor="center",relx=0.24, rely=0.71)
        self.withStd_optMenu = ctk.CTkOptionMenu(self,width=120,height=30,values=["True","False"])
        self.withStd_optMenu.configure(fg_color="#200E3A")
        self.withStd_optMenu.place(relx=0.33, rely=0.72, anchor="center")
        self.scCols_label = ctk.CTkLabel(self,font=('Arial',17),text="Target: ")
        self.scCols_label.place(anchor="center",relx=0.11, rely=0.815)
        self.scCols_optMenu = ctk.CTkOptionMenu(self, width=190, height=30,values=[],dynamic_resizing=True)
        self.scCols_optMenu.configure(fg_color="#200E3A")
        self.scCols_optMenu.place(relx=0.22, rely=0.825, anchor="center")
        self.sc_button = ctk.CTkButton(master=self,text='Standardize',font=('Arial',15),width=190,height=30,command=lambda:self.applySC(str(self.sc_optMenu.get()),str(self.withStd_optMenu.get()),str(self.scCols_optMenu.get())))
        self.sc_button.configure(fg_color="#200E3A")
        self.sc_button.place(anchor="center",relx=0.22, rely=0.955)
        
        self.minmax_label = ctk.CTkLabel(self,font=('Arial',20),text="MinMax Scaler: ")
        self.minmax_label.place(anchor="center",relx=0.62, rely=0.08)
        self.feature_range_label = ctk.CTkLabel(self,font=('Arial',17),text="feature_range: ")
        self.feature_range_label.place(anchor="center",relx=0.48, rely=0.23)
        self.feature_range_entry = ctk.CTkEntry(self,width=120,height=30,placeholder_text="tuple - default (0,1)")
        self.feature_range_entry.place(relx=0.58, rely=0.24, anchor="center")
        self.axis_label = ctk.CTkLabel(self,font=('Arial',17),text="axis: ")
        self.axis_label.place(anchor="center",relx=0.68, rely=0.23)
        self.axis_OptMenu = ctk.CTkOptionMenu(self,width=120,height=30,values=["0","1"])
        self.axis_OptMenu.configure(fg_color="#200E3A")
        self.axis_OptMenu.place(relx=0.75, rely=0.24, anchor="center")
        self.mmCols_label = ctk.CTkLabel(self,font=('Arial',17),text="Target: ")
        self.mmCols_label.place(anchor="center",relx=0.52, rely=0.35)
        self.mmCols_optMenu = ctk.CTkOptionMenu(self, width=190, height=30,values=[],dynamic_resizing=True)
        self.mmCols_optMenu.configure(fg_color="#200E3A")
        self.mmCols_optMenu.place(relx=0.62, rely=0.36, anchor="center")
        self.minmax_button = ctk.CTkButton(master=self,text='MinMax',font=('Arial',15),width=190,height=30,command=lambda:self.applyMinMax(str(self.feature_range_entry.get()),str(self.axis_OptMenu.get()),str(self.mmCols_optMenu.get())))
        self.minmax_button.configure(fg_color="#200E3A")
        self.minmax_button.place(anchor="center",relx=0.62, rely=0.48)
        
        self.maxabs_label = ctk.CTkLabel(self,font=('Arial',20),text="MaxAbs Scaler: ")
        self.maxabs_label.place(anchor="center",relx=0.62, rely=0.6)
        self.maxabsAxis_label = ctk.CTkLabel(self,font=('Arial',17),text="axis: ")
        self.maxabsAxis_label.place(anchor="center",relx=0.45, rely=0.75)
        self.maxabsAxis_OptMenu = ctk.CTkOptionMenu(self,width=190,height=30,values=["0","1"])
        self.maxabsAxis_OptMenu.configure(fg_color="#200E3A")
        self.maxabsAxis_OptMenu.place(relx=0.55, rely=0.76, anchor="center")
        self.mabsCols_label = ctk.CTkLabel(self,font=('Arial',17),text="Target: ")
        self.mabsCols_label.place(anchor="center",relx=0.65, rely=0.75)
        self.mabsCols_optMenu = ctk.CTkOptionMenu(self, width=190, height=30,values=[],dynamic_resizing=True)
        self.mabsCols_optMenu.configure(fg_color="#200E3A")
        self.mabsCols_optMenu.place(relx=0.75, rely=0.76, anchor="center")
        self.maxabs_button = ctk.CTkButton(master=self,text='MaxAbs',font=('Arial',15),width=190,height=30,command=lambda:self.applyMaxAbs(str(self.maxabsAxis_OptMenu.get()),str(self.mabsCols_optMenu.get())))
        self.maxabs_button.configure(fg_color="#200E3A")
        self.maxabs_button.place(anchor="center",relx=0.62, rely=0.955)
        
        self.import_file_button = ctk.CTkButton(master=self,text='Import...',width=200,height=45,command=lambda:self.controller.frames[ppf.PrePFrame].getFile())
        self.import_file_button.configure(fg_color="#200E3A")
        self.import_file_button.place(anchor="center",relx=0.92, rely=0.14)
        
        self.showEntireData_button = ctk.CTkButton(master=self,text='Load Original Dataset',width=200,height=45,command=lambda:self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].df))
        self.showEntireData_button.configure(fg_color="#200E3A")
        self.showEntireData_button.place(anchor="center",relx=0.92, rely=0.3)
        
        self.loadNSCDF_button = ctk.CTkButton(master=self,text='Load N&SC Dataframe',width=200,height=45,command=lambda:self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].dfNSC))
        self.loadNSCDF_button.configure(fg_color="#200E3A")
        self.loadNSCDF_button.place(anchor="center",relx=0.92, rely=0.46)
        
        self.rollback_button = ctk.CTkButton(master=self,text='Rollback',width=200,height=45,command=lambda:self.rollback())
        self.rollback_button.configure(fg_color="#200E3A")
        self.rollback_button.place(anchor="center",relx=0.92, rely=0.62)
        
        self.SaveChanges_button = ctk.CTkButton(master=self,text='Save changes to Dataframe',width=200,height=45,command=lambda:self.saveChanges())
        self.SaveChanges_button.configure(fg_color="#200E3A")
        self.SaveChanges_button.place(anchor="center",relx=0.92, rely=0.78)
        
    def applyNorm(self,norm,target):
        if self.controller.frames[ppf.PrePFrame].dfNSC is None:
            tk.messagebox.showerror('Python Error', "Please import a file first.")
            return
        
        if any(self.controller.frames[ppf.PrePFrame].dfNSC.dtypes == object):
            tk.messagebox.showerror('Python Error', "Categorical columns represented as strings are not supported. Please convert them to numerical values.")
            return
        
        X = self.controller.frames[ppf.PrePFrame].dfNSC.drop(target, axis=1)
        y = self.controller.frames[ppf.PrePFrame].dfNSC[target]
        
        N = Normalizer(norm=norm)
        self.controller.frames[ppf.PrePFrame].dfNSC = pd.DataFrame(N.fit_transform(X,y))
        self.controller.frames[ppf.PrePFrame].dfNSC[target] = y
            
        self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].dfNSC)
    
    def applySC(self,with_mean,with_std,target):
        if self.controller.frames[ppf.PrePFrame].dfNSC is None:
            tk.messagebox.showerror('Python Error', "Please import a file first.")
            return
        
        if any(self.controller.frames[ppf.PrePFrame].dfNSC.dtypes == object):
            tk.messagebox.showerror('Python Error', "Categorical columns represented as strings are not supported. Please convert them to numerical values.")
            return
        
        X = self.controller.frames[ppf.PrePFrame].dfNSC.drop(target, axis=1)
        y = self.controller.frames[ppf.PrePFrame].dfNSC[target]
        
        if with_mean == 'True':
            with_mean = True
        else:
            with_mean = False
            
        if with_std == 'True':
            with_std = True
        else:
            with_std = False
        
        SC = StandardScaler(with_mean=with_mean,with_std=with_std)
        self.controller.frames[ppf.PrePFrame].dfNSC = pd.DataFrame(SC.fit_transform(X))
        self.controller.frames[ppf.PrePFrame].dfNSC[target] = y
        
        self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].dfNSC)
        
    def applyMinMax(self, feature_range, axis,target):
        if self.controller.frames[ppf.PrePFrame].dfNSC is None:
            tk.messagebox.showerror('Python Error', "Please import a file first.")
            return

        if any(self.controller.frames[ppf.PrePFrame].dfNSC.dtypes == object):
            tk.messagebox.showerror('Python Error', "Categorical columns represented as strings are not supported. Please convert them to numerical values.")
            return

        X = self.controller.frames[ppf.PrePFrame].dfNSC.drop(target, axis=1)
        y = self.controller.frames[ppf.PrePFrame].dfNSC[target]
        
        if feature_range == '':
            feature_range = (0, 1)
        else:
            if not re.match(r'\(\s*\d+\s*,\s*\d+\s*\)', feature_range):
                tk.messagebox.showerror('Python Error', "feature_range must be a tuple.")
                return

            range_values = re.findall(r'\d+', feature_range)
            if int(range_values[0]) >= int(range_values[1]):
                tk.messagebox.showerror('Python Error', "The first number in feature_range must be smaller than the second number.")
                return

            feature_range = tuple(map(int, range_values))
        
        self.controller.frames[ppf.PrePFrame].dfNSC = pd.DataFrame(minmax_scale(X,feature_range=feature_range, axis=int(axis)))
        self.controller.frames[ppf.PrePFrame].dfNSC[target] = y

        self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].dfNSC)
        
    def applyMaxAbs(self,axis,target):
        if self.controller.frames[ppf.PrePFrame].dfNSC is None:
            tk.messagebox.showerror('Python Error', "Please import a file first.")
            return
        
        if any(self.controller.frames[ppf.PrePFrame].dfNSC.dtypes == object):
            tk.messagebox.showerror('Python Error', "Categorical columns represented as strings are not supported. Please convert them to numerical values.")
            return
        
        X = self.controller.frames[ppf.PrePFrame].dfNSC.drop(target, axis=1)
        y = self.controller.frames[ppf.PrePFrame].dfNSC[target]
        
        
        self.controller.frames[ppf.PrePFrame].dfNSC = pd.DataFrame(maxabs_scale(X,axis=int(axis)))
        self.controller.frames[ppf.PrePFrame].dfNSC[target] = y
        
        self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].dfNSC)
        
    def saveChanges(self):
        if self.controller.frames[ppf.PrePFrame].dfNSC is not None:
            self.controller.frames[ppf.PrePFrame].df = self.controller.frames[ppf.PrePFrame].dfNSC
            tk.messagebox.showinfo('Info', 'Changes saved to Dataframe, rollback not available.')
            
    def rollback(self):
        if self.controller.frames[ppf.PrePFrame].dfNSC is not None and self.controller.frames[ppf.PrePFrame].df is not None:
            self.controller.frames[ppf.PrePFrame].dfNSC = self.controller.frames[ppf.PrePFrame].df
            self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].dfNSC)
            tk.messagebox.showinfo('Info', 'Rollback successful')