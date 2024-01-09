import tkinter as tk
import customtkinter as ctk
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import numpy as np
import preprocessing.ppframe as ppf

class OneHotEncFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent,fg_color='transparent',corner_radius=20)
        
        self.onehotenc_label = ctk.CTkLabel(self,font=('Arial',30),text="One Hot Encoder: ")
        self.onehotenc_label.place(anchor="center",relx=0.5, rely=0.07)
        
        self.drop_label = ctk.CTkLabel(self,font=('Arial',17),text="drop: ")
        self.drop_label.place(anchor="center",relx=0.175, rely=0.2)
        self.drop_optMenu = ctk.CTkOptionMenu(self, width=190, height=30,values=['None','first','if_binary'],dynamic_resizing=True)
        self.drop_optMenu.configure(fg_color="#200E3A")
        self.drop_optMenu.place(relx=0.35, rely=0.21, anchor="center")
        
        self.sparse_label = ctk.CTkLabel(self,font=('Arial',17),text="sparse_output: ")
        self.sparse_label.place(anchor="center",relx=0.177, rely=0.4)
        self.sparse_optMenu = ctk.CTkOptionMenu(self, width=190, height=30,values=['True','False'],dynamic_resizing=True)
        self.sparse_optMenu.configure(fg_color="#200E3A")
        self.sparse_optMenu.place(relx=0.35, rely=0.41, anchor="center")
        
        self.dtype_label = ctk.CTkLabel(self,font=('Arial',17),text="dtype: ")
        self.dtype_label.place(anchor="center",relx=0.177, rely=0.6)
        self.dtype_optMenu = ctk.CTkOptionMenu(self, width=190, height=30,values=['np.float64','int','np.uint8'],dynamic_resizing=True)
        self.dtype_optMenu.configure(fg_color="#200E3A")
        self.dtype_optMenu.place(relx=0.35, rely=0.61, anchor="center")
        
        self.handleUnk_label = ctk.CTkLabel(self,font=('Arial',17),text="handle_unknown: ")
        self.handleUnk_label.place(anchor="center",relx=0.51, rely=0.2)
        self.handleUnk_optMenu = ctk.CTkOptionMenu(self, width=190, height=30,values=['error','ignore','infrequent_if_exist'],dynamic_resizing=True)
        self.handleUnk_optMenu.configure(fg_color="#200E3A")
        self.handleUnk_optMenu.place(relx=0.65, rely=0.21, anchor="center")
        
        self.minfreq_label = ctk.CTkLabel(self,font=('Arial',17),text="min_frequency: ")
        self.minfreq_label.place(anchor="center",relx=0.51, rely=0.4)
        self.minfreq_entry = ctk.CTkEntry(self, width=190, height=30, placeholder_text="None")
        self.minfreq_entry.place(relx=0.65, rely=0.41, anchor="center")
        
        self.maxCat_label = ctk.CTkLabel(self,font=('Arial',17),text="max_categories: ")
        self.maxCat_label.place(anchor="center",relx=0.51, rely=0.6)
        self.maxCat_entry = ctk.CTkEntry(self, width=190, height=30, placeholder_text="None")
        self.maxCat_entry.place(relx=0.65, rely=0.61, anchor="center")
        
        self.target_label = ctk.CTkLabel(self,font=('Arial',17),text="Column to encode: ")
        self.target_label.place(anchor="center",relx=0.35, rely=0.75)
        self.target_optMenu = ctk.CTkOptionMenu(self, width=190, height=30,values=[],dynamic_resizing=True)
        self.target_optMenu.configure(fg_color="#200E3A")
        self.target_optMenu.place(relx=0.5, rely=0.76, anchor="center")
        
        self.import_file_button = ctk.CTkButton(master=self,text='Import...',width=200,height=45,command=lambda:self.controller.frames[ppf.PrePFrame].getFile())
        self.import_file_button.configure(fg_color="#200E3A")
        self.import_file_button.place(anchor="center",relx=0.92, rely=0.14)
        
        self.showEntireData_button = ctk.CTkButton(master=self,text='Load Original Dataset',width=200,height=45,command=lambda:self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].df))
        self.showEntireData_button.configure(fg_color="#200E3A")
        self.showEntireData_button.place(anchor="center",relx=0.92, rely=0.3)
        
        self.loadOHEdf_button = ctk.CTkButton(master=self,text='Load OHE Dataframe',width=200,height=45,command=lambda:self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].dfOHE))
        self.loadOHEdf_button.configure(fg_color="#200E3A")
        self.loadOHEdf_button.place(anchor="center",relx=0.92, rely=0.46)
        
        self.rollback_button = ctk.CTkButton(master=self,text='Rollback',width=200,height=45,command=lambda:self.rollback())
        self.rollback_button.configure(fg_color="#200E3A")
        self.rollback_button.place(anchor="center",relx=0.92, rely=0.62)
        
        self.SaveChanges_button = ctk.CTkButton(master=self,text='Save changes to Dataframe',width=200,height=45,command=lambda:self.saveChanges())
        self.SaveChanges_button.configure(fg_color="#200E3A")
        self.SaveChanges_button.place(anchor="center",relx=0.92, rely=0.78)
        
        self.ohe_button = ctk.CTkButton(master=self, text='Apply One-Hot Encoding', font=('Arial', 15), width=400, height=40,
                                          command=lambda:self.applyOHE(str(self.drop_optMenu.get()),
                                                                       str(self.sparse_optMenu.get()),
                                                                       str(self.dtype_optMenu.get()),
                                                                       str(self.handleUnk_optMenu.get()),
                                                                       str(self.minfreq_entry.get()),
                                                                       str(self.maxCat_entry.get()),
                                                                       str(self.target_optMenu.get())
                                                                      ))
        self.ohe_button.configure(fg_color="#200E3A")
        self.ohe_button.place(anchor="center", relx=0.5, rely=0.9)
        
        
    def applyOHE(self,drop,sparse,dtype,handleUnk,minfreq,maxCat,target):
        
        if self.controller.frames[ppf.PrePFrame].dfOHE is None:
            tk.messagebox.showerror('Python Error', "Please import a file first.")
            return
        
        if target == '':
            tk.messagebox.showerror('Python Error', "Please select a target column.")
            return
        
        X = self.controller.frames[ppf.PrePFrame].dfOHE.drop(target, axis=1)
        y = self.controller.frames[ppf.PrePFrame].dfOHE[target]
        
        if minfreq == '':
            minfreq = None
        elif minfreq == 'None':
            minfreq = None
        
        if maxCat == '':
            maxCat = None
        elif maxCat == 'None':
            maxCat = None
        
        if drop == 'None':
            drop = None
        
        if sparse == 'True':
            sparse = True
        else:
            sparse = False
        
        if dtype == 'np.float64':
            dtype = np.float64
        elif dtype == 'int':
            dtype = int
        else:
            dtype = np.uint8
        
        if isinstance(minfreq, str) and minfreq != 'None':
            try:
                minfreq = int(minfreq)
            except:
                tk.messagebox.showerror('Python Error', "min_frequency must be an Int.")
                return
            
        if isinstance(maxCat, str) and maxCat != 'None':
            try:
                maxCat = int(maxCat)
            except:
                tk.messagebox.showerror('Python Error', "max_categories must be an Int.")
                return
        
        OHE = OneHotEncoder(drop=drop,sparse=sparse,dtype=dtype,handle_unknown=handleUnk,min_frequency=minfreq,max_categories=maxCat)
        if sparse == True:
            encoded_values = OHE.fit_transform(np.asarray(y).reshape(-1,1)).toarray()
            encoded_df = pd.DataFrame(encoded_values, columns=OHE.get_feature_names_out([target]))
        else:
            encoded_values = OHE.fit_transform(np.asarray(y).reshape(-1,1))
            encoded_df = pd.DataFrame(encoded_values, columns=OHE.get_feature_names_out([target]))
        
        self.controller.frames[ppf.PrePFrame].dfOHE = X
        self.controller.frames[ppf.PrePFrame].dfOHE = pd.concat([self.controller.frames[ppf.PrePFrame].dfOHE, encoded_df], axis=1)
        
        self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].dfOHE)
        
    def saveChanges(self):
        if self.controller.frames[ppf.PrePFrame].dfOHE is not None:
            self.controller.frames[ppf.PrePFrame].df = self.controller.frames[ppf.PrePFrame].dfOHE
            tk.messagebox.showinfo('Info', 'Changes saved to Dataframe, rollback not available.')
            
    def rollback(self):
        if self.controller.frames[ppf.PrePFrame].dfOHE is not None and self.controller.frames[ppf.PrePFrame].df is not None:
            self.controller.frames[ppf.PrePFrame].dfOHE = self.controller.frames[ppf.PrePFrame].df
            self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].dfOHE)
            tk.messagebox.showinfo('Info', 'Rollback successful')