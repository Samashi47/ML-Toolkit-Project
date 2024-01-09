import tkinter as tk
import customtkinter as ctk
from imblearn.under_sampling import CondensedNearestNeighbour
import preprocessing.ppframe as ppf


class CNNFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent, fg_color='transparent', corner_radius=20)

        self.cnn_label = ctk.CTkLabel(self,font=('Arial',30), text="Condensed Nearest Neighbour: ")
        self.cnn_label.place(anchor="center",relx=0.5, rely=0.07)
        
        self.RandomS_label = ctk.CTkLabel(self, font=('Arial', 17), text="random_state: ")
        self.RandomS_label.place(anchor="center", relx=0.175, rely=0.3)
        self.random_state_entry = ctk.CTkEntry(self, width=190, height=30, placeholder_text="None")
        self.random_state_entry.place(relx=0.35, rely=0.31, anchor="center")

        self.Shuffle_label = ctk.CTkLabel(self, font=('Arial', 17), text="sampling_strategy: ")
        self.Shuffle_label.place(anchor="center", relx=0.177, rely=0.5)
        self.Shuffle_optMenu = ctk.CTkOptionMenu(self, width=190, height=30, values=["auto","majority","not minority","not majority","all"])
        self.Shuffle_optMenu.configure(fg_color="#200E3A")
        self.Shuffle_optMenu.place(relx=0.35, rely=0.51, anchor="center")

        self.Neighbors_label = ctk.CTkLabel(self, font=('Arial', 17), text="n_neighbors : ")
        self.Neighbors_label.place(anchor="center", relx=0.53, rely=0.3)
        self.n_neighbors_entry = ctk.CTkEntry(self, width=190, height=30, placeholder_text="None")
        self.n_neighbors_entry.place(relx=0.65, rely=0.31, anchor="center")

        self.Seeds_label = ctk.CTkLabel(self, font=('Arial', 17), text="n_seeds_S : ")
        self.Seeds_label.place(anchor="center", relx=0.53, rely=0.5)
        self.n_seeds_S_entry = ctk.CTkEntry(self, width=190, height=30, placeholder_text="1")
        self.n_seeds_S_entry.place(relx=0.65, rely=0.51, anchor="center")

        self.import_file_button = ctk.CTkButton(master=self, text='Import...', width=200, height=35,command=lambda:self.controller.frames[ppf.PrePFrame].getFile())
        self.import_file_button.configure(fg_color="#200E3A")
        self.import_file_button.place(anchor="center", relx=0.92, rely=0.08)

        self.showEntireData_button = ctk.CTkButton(master=self, text='load Entire Dataset',width=200, height=35,command=lambda:self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].df))
        self.showEntireData_button.configure(fg_color="#200E3A")
        self.showEntireData_button.place(anchor="center", relx=0.92, rely=0.2)

        self.showTrainSplit_button = ctk.CTkButton(master=self, text='load Train Split',width=200, height=35,command=lambda:self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].X_train))
        self.showTrainSplit_button.configure(fg_color="#200E3A")
        self.showTrainSplit_button.place(anchor="center", relx=0.92, rely=0.32)

        self.showTrainSplitU_button = ctk.CTkButton(master=self, text='load Resampled Train Data', width=200, height=35,command=lambda:self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].X_train_resampled))
        self.showTrainSplitU_button.configure(fg_color="#200E3A")
        self.showTrainSplitU_button.place(anchor="center", relx=0.92, rely=0.44)

        self.showTargetTrainSplit_button = ctk.CTkButton(master=self, text='load Train Target', width=200, height=35,command=lambda:self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].y_train))
        self.showTargetTrainSplit_button.configure(fg_color="#200E3A")
        self.showTargetTrainSplit_button.place(anchor="center", relx=0.92, rely=0.56)

        self.showTargetTestSplitU_button = ctk.CTkButton(master=self, text='load Resampled Train Target', width=200, height=35,command=lambda:self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].y_train_resampled))
        self.showTargetTestSplitU_button.configure(fg_color="#200E3A")
        self.showTargetTestSplitU_button.place(anchor="center", relx=0.92, rely=0.68)
        
        self.rollback_button = ctk.CTkButton(master=self,text='Rollback',width=200,height=35,command=lambda:self.rollback())
        self.rollback_button.configure(fg_color="#200E3A")
        self.rollback_button.place(anchor="center",relx=0.92, rely=0.8)
        
        self.SaveChanges_button = ctk.CTkButton(master=self,text='Save changes to Dataframe',width=200,height=35,command=lambda:self.saveChanges())
        self.SaveChanges_button.configure(fg_color="#200E3A")
        self.SaveChanges_button.place(anchor="center",relx=0.92, rely=0.92)

        self.split_button = ctk.CTkButton(master=self, text='Apply CNN', font=('Arial', 15), width=400, height=40,
                                          command=lambda:self.applyCNN(str(self.Shuffle_optMenu.get()),
                                                                str(self.random_state_entry.get()),
                                                                str(self.n_neighbors_entry.get()),
                                                                str(self.n_seeds_S_entry.get())
                                                                ))
        self.split_button.configure(fg_color="#200E3A")
        self.split_button.place(anchor="center", relx=0.5, rely=0.9)

    def saveChanges(self):
        
        if self.controller.frames[ppf.PrePFrame].X_train is None or self.controller.frames[ppf.PrePFrame].y_train is None:
            tk.messagebox.showerror('Python Error', "Please split the data first.")
            return
        
        if self.controller.frames[ppf.PrePFrame].X_train is not None:
            self.controller.frames[ppf.PrePFrame].X_train = self.controller.frames[ppf.PrePFrame].X_train_resampled
            self.controller.frames[ppf.PrePFrame].y_train = self.controller.frames[ppf.PrePFrame].y_train_resampled
            tk.messagebox.showinfo('Info', 'Changes saved to Dataframe, rollback not available.')
            
    def rollback(self):
        
        if self.controller.frames[ppf.PrePFrame].X_train is None or self.controller.frames[ppf.PrePFrame].y_train is None:
            tk.messagebox.showerror('Python Error', "Please split the data first.")
            return
        
        if self.controller.frames[ppf.PrePFrame].X_train_resampled is not None and self.controller.frames[ppf.PrePFrame].X_train is not None:
            self.controller.frames[ppf.PrePFrame].X_train_resampled = self.controller.frames[ppf.PrePFrame].X_train
            self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].X_train_resampled)
            tk.messagebox.showinfo('Info', 'Rollback successful')
            
    def applyCNN(self,sampling_s='auto',random_s=None,n_n=None,n_s=1):

        if self.controller.frames[ppf.PrePFrame].df is None :
            tk.messagebox.showerror('Python Error', "Please import a file first.")
            return
        
        if self.controller.frames[ppf.PrePFrame].X_train is None or self.controller.frames[ppf.PrePFrame].y_train is None:
            tk.messagebox.showerror('Python Error', "Please split the data first.")
            return
        
        X = self.controller.frames[ppf.PrePFrame].X_train
        y = self.controller.frames[ppf.PrePFrame].y_train
        
        if any(X.dtypes == object):
            tk.messagebox.showerror('Python Error', "Categorical columns represented as strings are not supported. Please convert them to numerical values.")
            return

        if sampling_s == '':
            sampling_s ='auto'
        if n_n == '':
            n_n = None
        if random_s == '':
            random_s = None
        if n_s == '':
            n_s = 1

        if isinstance(n_s, str):
            try:
                n_s = int(n_s)
            except:
                tk.messagebox.showerror('Python Error', "n_seeds_S_entry size must be a Int.")
                return
        if isinstance(n_n, str) and n_n != 'None':
            try:
                n_n = int(n_n)
            except:
                tk.messagebox.showerror('Python Error', "n_neighbors must be an int or None.")
                return
        if isinstance(random_s, str) and random_s != 'None':
            try:
                random_s = int(random_s)
            except:
                tk.messagebox.showerror('Python Error', "random state must be an int or None.")
                return

        CNN = CondensedNearestNeighbour(sampling_strategy=sampling_s, random_state=random_s,n_neighbors=n_n,n_seeds_S=n_s)
        self.controller.frames[ppf.PrePFrame].X_train_resampled, self.controller.frames[ppf.PrePFrame].y_train_resampled=CNN.fit_resample(X,y)

        tk.messagebox.showinfo('Info', 'CNN applied Successfully: \nX_train shape: {} \nX_train_resampled shape: {} \ny_train shape: {} \ny_train_resampled shape: {}'.format(self.controller.frames[ppf.PrePFrame].X_train.shape,self.controller.frames[ppf.PrePFrame].X_train_resampled.shape,self.controller.frames[ppf.PrePFrame].y_train.shape,self.controller.frames[ppf.PrePFrame].y_train_resampled.shape))