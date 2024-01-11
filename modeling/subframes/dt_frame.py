import tkinter as tk
import customtkinter as ctk
from sklearn.tree import DecisionTreeClassifier
import pickle
import modeling.models_frame as mf
import preprocessing.ppframe as ppf


class DTFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent,corner_radius=20,fg_color='transparent')
        
        self.DT_label = ctk.CTkLabel(self,font=('Arial',30),text="Decision Trees: ")
        self.DT_label.place(anchor="center",relx=0.5, rely=0.08)
        
        self.criterion_label = ctk.CTkLabel(self,font=('Arial',17),text="criterion: ")
        self.criterion_label.place(anchor="center",relx=0.035, rely=0.2)
        self.criterion_optMenu = ctk.CTkOptionMenu(self, width=190, height=30,values=['gini', 'entropy', 'log_loss'],dynamic_resizing=True)
        self.criterion_optMenu.configure(fg_color="#200E3A")
        self.criterion_optMenu.place(relx=0.18, rely=0.21, anchor="center")
        
        self.splitter_label = ctk.CTkLabel(self,font=('Arial',17),text="splitter: ")
        self.splitter_label.place(anchor="center",relx=0.037, rely=0.4)
        self.splitter_optMenu = ctk.CTkOptionMenu(self, width=190, height=30,values=['best', 'random'],dynamic_resizing=True)
        self.splitter_optMenu.configure(fg_color="#200E3A")
        self.splitter_optMenu.place(relx=0.18, rely=0.41, anchor="center")
        
        self.maxdepth_label = ctk.CTkLabel(self,font=('Arial',17),text="max_depth: ")
        self.maxdepth_label.place(anchor="center",relx=0.037, rely=0.6)
        self.maxdepth_entry = ctk.CTkEntry(self, width=190, height=30, placeholder_text="None")
        self.maxdepth_entry.place(relx=0.18, rely=0.61, anchor="center")
        
        self.randomstate_label = ctk.CTkLabel(self,font=('Arial',17),text="random_state: ")
        self.randomstate_label.place(anchor="center",relx=0.047, rely=0.8)
        self.randomstate_entry = ctk.CTkEntry(self, width=190, height=30, placeholder_text="None")
        self.randomstate_entry.place(relx=0.18, rely=0.81, anchor="center")
        
        self.minsamples_label = ctk.CTkLabel(self,font=('Arial',17),text="min_samples_split: ")
        self.minsamples_label.place(anchor="center",relx=0.32, rely=0.2)
        self.minsamples_entry = ctk.CTkEntry(self, width=190, height=30, placeholder_text="2")
        self.minsamples_entry.place(relx=0.51, rely=0.21, anchor="center")
        
        self.minleaf_label = ctk.CTkLabel(self,font=('Arial',17),text="min_samples_leaf: ")
        self.minleaf_label.place(anchor="center",relx=0.32, rely=0.4)
        self.minleaf_entry = ctk.CTkEntry(self, width=190, height=30, placeholder_text="1")
        self.minleaf_entry.place(relx=0.51, rely=0.41, anchor="center")
        
        self.minsamplesleaf_label = ctk.CTkLabel(self,font=('Arial',17),text="min_weight_fraction_leaf: ")
        self.minsamplesleaf_label.place(anchor="center",relx=0.34, rely=0.6)
        self.minsamplesleaf_entry = ctk.CTkEntry(self, width=190, height=30, placeholder_text="0.0")
        self.minsamplesleaf_entry.place(relx=0.51, rely=0.61, anchor="center")
        
        self.minimpurity_label = ctk.CTkLabel(self,font=('Arial',17),text="min_impurity_decrease: ")
        self.minimpurity_label.place(anchor="center",relx=0.335, rely=0.8)
        self.minimpurity_entry = ctk.CTkEntry(self, width=190, height=30, placeholder_text="0.0")
        self.minimpurity_entry.place(relx=0.51, rely=0.81, anchor="center")
        
        self.maxfeatures_label = ctk.CTkLabel(self,font=('Arial',17),text="max_features: ")
        self.maxfeatures_label.place(anchor="center",relx=0.635, rely=0.3)
        self.maxfeatures_optMenu = ctk.CTkOptionMenu(self, width=190, height=30,values=['None','auto', 'sqrt','log2'],dynamic_resizing=True)
        self.maxfeatures_optMenu.configure(fg_color="#200E3A")
        self.maxfeatures_optMenu.place(relx=0.78, rely=0.31, anchor="center")
        
        self.maxleafnodes_label = ctk.CTkLabel(self,font=('Arial',17),text="max_leaf_nodes: ")
        self.maxleafnodes_label.place(anchor="center",relx=0.645, rely=0.5)
        self.maxleafnodes_entry = ctk.CTkEntry(self, width=190, height=30, placeholder_text="None")
        self.maxleafnodes_entry.place(relx=0.78, rely=0.51, anchor="center")
        
        self.ccpalpha_label = ctk.CTkLabel(self,font=('Arial',17),text="ccp_alpha: ")
        self.ccpalpha_label.place(anchor="center",relx=0.625, rely=0.7)
        self.ccpalpha_entry = ctk.CTkEntry(self, width=190, height=30, placeholder_text="0.0")
        self.ccpalpha_entry.place(relx=0.78, rely=0.71, anchor="center")
        
        self.import_file_button = ctk.CTkButton(master=self, text='Import...', width=170, height=45,command=lambda:self.controller.frames[ppf.PrePFrame].getFile())
        self.import_file_button.configure(fg_color="#200E3A")
        self.import_file_button.place(anchor="center", relx=0.93, rely=0.42)
        
        self.evaluateModel_button = ctk.CTkButton(master=self,text='Evaluate Model',width=170,height=45,command=lambda:self.controller.frames[mf.ModelsFrame].evaluateModel())
        self.evaluateModel_button.configure(fg_color="#200E3A")
        self.evaluateModel_button.place(anchor="center",relx=0.93, rely=0.57)
        
        self.SaveChanges_button = ctk.CTkButton(master=self,text='Save Model',width=170,height=45,command=lambda:self.saveModel())
        self.SaveChanges_button.configure(fg_color="#200E3A")
        self.SaveChanges_button.place(anchor="center",relx=0.93, rely=0.72)
        
        self.train_button = ctk.CTkButton(master=self, text='Train', font=('Arial', 15), width=300, height=35,
                                          command=lambda:self.trainDT(str(self.criterion_optMenu.get()),
                                                                      str(self.splitter_optMenu.get()),
                                                                      str(self.maxdepth_entry.get()),
                                                                      str(self.randomstate_entry.get()),
                                                                      str(self.minsamples_entry.get()),
                                                                      str(self.minleaf_entry.get()),
                                                                      str(self.minsamplesleaf_entry.get()),
                                                                      str(self.minimpurity_entry.get()),
                                                                      str(self.maxfeatures_optMenu.get()),
                                                                      str(self.maxleafnodes_entry.get()),
                                                                      str(self.ccpalpha_entry.get())
                                                                      ))
        self.train_button.configure(fg_color="#200E3A")
        self.train_button.place(anchor="center", relx=0.5, rely=0.94)
        
    def trainDT(self,criterion,splitter,maxdepth,randomstate,minsamples,minleaf,minsamplesleaf,minimpurity,maxfeatures,maxleafnodes,ccpalpha):
        if self.controller.frames[ppf.PrePFrame].df is None:
            tk.messagebox.showerror('Python Error', "Please import a file first.")
            return
        
        if self.controller.frames[ppf.PrePFrame].X_train is None or self.controller.frames[ppf.PrePFrame].y_train is None:
            tk.messagebox.showerror('Python Error', "Please run train test split first.")
            return
        
        if any(self.controller.frames[ppf.PrePFrame].X_test.dtypes == object):
            tk.messagebox.showerror('Python Error', "Categorical columns represented as strings are not supported. Please convert them to numerical values.")
            return
        
        if maxdepth == '':
            maxdepth = None
        
        if randomstate == '':
            randomstate = None
            
        if minsamples == '':
            minsamples = 2
            
        if minleaf == '':
            minleaf = 1
            
        if minsamplesleaf == '':
            minsamplesleaf = 0.0
        if minimpurity == '':
            minimpurity = 0.0
            
        if maxfeatures == 'None':
            maxfeatures = None
            
        if maxleafnodes == '':
            maxleafnodes = None
        if ccpalpha == '':
            ccpalpha = 0.0
        
        if isinstance(maxdepth, str):
            try:
                maxdepth = int(maxdepth)
            except:
                tk.messagebox.showerror('Python Error', "max_depth must be an integer.")
                return
            
        if isinstance(randomstate, str) and randomstate != 'None':
            try:
                randomstate = int(randomstate)
            except:
                tk.messagebox.showerror('Python Error', "random state must be an int or None.")
                return
        elif randomstate == 'None':
            randomstate = None
            
        if isinstance(minsamples, str):
            try:
                minsamples = int(minsamples)
            except:
                tk.messagebox.showerror('Python Error', "min_samples_split must be an integer.")
                return
            
        if isinstance(minleaf, str):
            try:
                minleaf = int(minleaf)
            except:
                tk.messagebox.showerror('Python Error', "min_samples_leaf must be an integer.")
                return
            
        if isinstance(minsamplesleaf, str):
            try:
                minsamplesleaf = float(minsamplesleaf)
            except:
                tk.messagebox.showerror('Python Error', "min_weight_fraction_leaf must be a float.")
                return
        if isinstance(minimpurity, str):
            try:
                minimpurity = float(minimpurity)
            except:
                tk.messagebox.showerror('Python Error', "min_impurity_decrease must be a float.")
                return
        
        if isinstance(maxleafnodes, str) and maxleafnodes != 'None':
            try:
                maxleafnodes = int(maxleafnodes)
            except:
                tk.messagebox.showerror('Python Error', "max_leaf_nodes must be an int or None.")
                return
        elif maxleafnodes == 'None':
            maxleafnodes = None
        
        if isinstance(ccpalpha, str):
            try:
                ccpalpha = float(ccpalpha)
            except:
                tk.messagebox.showerror('Python Error', "ccp_alpha must be a float.")
                return
        if maxdepth is not None and maxdepth < 0:
            tk.messagebox.showerror('Python Error', "max_depth must be positive.")
            return
        if minsamples < 0:
            tk.messagebox.showerror('Python Error', "min_samples_split must be positive.")
            return
        if minleaf < 0:
            tk.messagebox.showerror('Python Error', "min_samples_leaf must be positive.")
            return
        if minsamplesleaf < 0:
            tk.messagebox.showerror('Python Error', "min_weight_fraction_leaf must be positive.")
            return
        if minimpurity < 0:
            tk.messagebox.showerror('Python Error', "min_impurity_decrease must be positive.")
            return
        if maxleafnodes is not None and maxleafnodes < 0:
            tk.messagebox.showerror('Python Error', "max_leaf_nodes must be positive.")
            return
        if ccpalpha < 0:
            tk.messagebox.showerror('Python Error', "ccp_alpha must be positive.")
            return
        
        self.controller.frames[mf.ModelsFrame].model = DecisionTreeClassifier(criterion=criterion, splitter=splitter, max_depth=maxdepth, random_state=randomstate, min_samples_split=minsamples, min_samples_leaf=minleaf, min_weight_fraction_leaf=minsamplesleaf, min_impurity_decrease=minimpurity, max_features=maxfeatures, max_leaf_nodes=maxleafnodes, ccp_alpha=ccpalpha)
        try:
            self.controller.frames[mf.ModelsFrame].model.fit(self.controller.frames[ppf.PrePFrame].X_train, self.controller.frames[ppf.PrePFrame].y_train)
            tk.messagebox.showinfo('Info', 'Training successful')
            return
        except ValueError as e:
            tk.messagebox.showerror('Python Error', str(e))
            return
        
    def saveModel(self):
        if self.controller.frames[mf.ModelsFrame].model is None:
            tk.messagebox.showerror('Python Error', "Please train a model first.")
            return
        filename = tk.filedialog.asksaveasfilename(initialdir="/", title="Select file", filetypes=(("model files", "*.sav"), ("all files", "*.*")))
        if filename == '':
            return
        pickle.dump(self.controller.frames[mf.ModelsFrame].model, open(filename+'.sav', 'wb'))
        tk.messagebox.showinfo('Info', 'Model saved successfully')