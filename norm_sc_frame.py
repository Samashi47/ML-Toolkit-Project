import tkinter as tk
import customtkinter as ctk
from sklearn.preprocessing import Normalizer, StandardScaler, MinMaxScaler, MaxAbsScaler
import ppframe as ppf

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
        self.Norm_label.place(anchor="center",relx=0.11, rely=0.3)
        self.norm_optMenu = ctk.CTkOptionMenu(self,width=190,height=30,values=["l1","l2","max"])
        self.norm_optMenu.configure(fg_color="#200E3A")
        self.norm_optMenu.place(relx=0.22, rely=0.31, anchor="center")
        self.norm_button = ctk.CTkButton(master=self,text='Normalize',font=('Arial',15),width=190,height=30,command=lambda:self.applyNorm(str(self.norm_optMenu.get())))
        self.norm_button.configure(fg_color="#200E3A")
        self.norm_button.place(anchor="center",relx=0.22, rely=0.48)
        
        self.sc_label = ctk.CTkLabel(self,font=('Arial',20),text="Standard Scaler: ")
        self.sc_label.place(anchor="center",relx=0.22, rely=0.6)
        self.withMean_label = ctk.CTkLabel(self,font=('Arial',17),text="with_mean: ")
        self.withMean_label.place(anchor="center",relx=0.06, rely=0.75)
        self.sc_optMenu = ctk.CTkOptionMenu(self,width=120,height=30,values=["True","False"])
        self.sc_optMenu.configure(fg_color="#200E3A")
        self.sc_optMenu.place(relx=0.15, rely=0.76, anchor="center")
        self.withStd_label = ctk.CTkLabel(self,font=('Arial',17),text="with_std: ")
        self.withStd_label.place(anchor="center",relx=0.24, rely=0.75)
        self.withStd_optMenu = ctk.CTkOptionMenu(self,width=120,height=30,values=["True","False"])
        self.withStd_optMenu.configure(fg_color="#200E3A")
        self.withStd_optMenu.place(relx=0.33, rely=0.76, anchor="center")
        self.sc_button = ctk.CTkButton(master=self,text='Standardize',font=('Arial',15),width=190,height=30,command=lambda:self.applySC(str(self.sc_optMenu.get()),str(self.withStd_optMenu.get())))
        self.sc_button.configure(fg_color="#200E3A")
        self.sc_button.place(anchor="center",relx=0.22, rely=0.93)
        
        self.minmax_label = ctk.CTkLabel(self,font=('Arial',20),text="MinMax Scaler: ")
        self.minmax_label.place(anchor="center",relx=0.62, rely=0.08)
        self.feature_range_label = ctk.CTkLabel(self,font=('Arial',17),text="feature_range: ")
        self.feature_range_label.place(anchor="center",relx=0.48, rely=0.3)
        self.feature_range_entry = ctk.CTkEntry(self,width=120,height=30,placeholder_text="(0,1)")
        self.feature_range_entry.place(relx=0.58, rely=0.31, anchor="center")
        self.axis_label = ctk.CTkLabel(self,font=('Arial',17),text="axis: ")
        self.axis_label.place(anchor="center",relx=0.68, rely=0.3)
        self.axis_OptMenu = ctk.CTkOptionMenu(self,width=120,height=30,values=["0","1"])
        self.axis_OptMenu.configure(fg_color="#200E3A")
        self.axis_OptMenu.place(relx=0.75, rely=0.31, anchor="center")
        self.minmax_button = ctk.CTkButton(master=self,text='MinMax',font=('Arial',15),width=190,height=30,command=lambda:self.applyMinMax(str(self.feature_range_entry.get()),str(self.axis_OptMenu.get())))
        self.minmax_button.configure(fg_color="#200E3A")
        self.minmax_button.place(anchor="center",relx=0.62, rely=0.48)
        
        self.maxabs_label = ctk.CTkLabel(self,font=('Arial',20),text="MaxAbs Scaler: ")
        self.maxabs_label.place(anchor="center",relx=0.62, rely=0.6)
        self.maxabsAxis_label = ctk.CTkLabel(self,font=('Arial',17),text="axis: ")
        self.maxabsAxis_label.place(anchor="center",relx=0.47, rely=0.75)
        self.maxabsAxis_OptMenu = ctk.CTkOptionMenu(self,width=190,height=30,values=["0","1"])
        self.maxabsAxis_OptMenu.configure(fg_color="#200E3A")
        self.maxabsAxis_OptMenu.place(relx=0.62, rely=0.76, anchor="center")
        self.maxabs_button = ctk.CTkButton(master=self,text='MaxAbs',font=('Arial',15),width=190,height=30,command=lambda:self.applyMaxAbs(str(self.maxabsAxis_OptMenu.get())))
        self.maxabs_button.configure(fg_color="#200E3A")
        self.maxabs_button.place(anchor="center",relx=0.62, rely=0.93)
        
        self.import_file_button = ctk.CTkButton(master=self,text='Import...',width=200,height=45,command=lambda:self.controller.frames[ppf.PrePFrame].getFile())
        self.import_file_button.configure(fg_color="#200E3A")
        self.import_file_button.place(anchor="center",relx=0.92, rely=0.27)
        
        self.showEntireData_button = ctk.CTkButton(master=self,text='Load Original Dataset',width=200,height=45,command=lambda:self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].df))
        self.showEntireData_button.configure(fg_color="#200E3A")
        self.showEntireData_button.place(anchor="center",relx=0.92, rely=0.42)
        
        self.loadMissValsDF_button = ctk.CTkButton(master=self,text='Load N&SC Dataframe',width=200,height=45,command=lambda:self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].df_msv))
        self.loadMissValsDF_button.configure(fg_color="#200E3A")
        self.loadMissValsDF_button.place(anchor="center",relx=0.92, rely=0.57)
        
        self.SaveChanges_button = ctk.CTkButton(master=self,text='Save changes to Dataframe',width=200,height=45,command=lambda:self.saveChanges())
        self.SaveChanges_button.configure(fg_color="#200E3A")
        self.SaveChanges_button.place(anchor="center",relx=0.92, rely=0.72)