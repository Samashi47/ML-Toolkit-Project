import tkinter as tk
import customtkinter as ctk
import pandas as pd
from imblearn.under_sampling import CondensedNearestNeighbour
import ppframe as ppf


class CnnFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent, fg_color='transparent', corner_radius=20)


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




        self.import_file_button = ctk.CTkButton(master=self, text='Import...', width=230, height=40,command=lambda:self.controller.frames[ppf.PrePFrame].getFile())
        self.import_file_button.configure(fg_color="#200E3A")
        self.import_file_button.place(anchor="center", relx=0.9, rely=0.12)

        self.showEntireData_button = ctk.CTkButton(master=self, text='load Entire Dataset',width=230, height=40,command=lambda:self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].df))
        self.showEntireData_button.configure(fg_color="#200E3A")
        self.showEntireData_button.place(anchor="center", relx=0.9, rely=0.27)

        self.showTrainSplit_button = ctk.CTkButton(master=self, text='load Train Split',width=230, height=40,command=lambda:self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].X_train))
        self.showTrainSplit_button.configure(fg_color="#200E3A")
        self.showTrainSplit_button.place(anchor="center", relx=0.9, rely=0.42)

        self.showTrainSplitU_button = ctk.CTkButton(master=self, text='load Train_undersimpled Split', width=230, height=40,command=lambda:self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].X_trainU))
        self.showTrainSplitU_button.configure(fg_color="#200E3A")
        self.showTrainSplitU_button.place(anchor="center", relx=0.9, rely=0.57)

        self.showTargetTrainSplit_button = ctk.CTkButton(master=self, text='load Train Target', width=230, height=40,command=lambda:self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].y_train))
        self.showTargetTrainSplit_button.configure(fg_color="#200E3A")
        self.showTargetTrainSplit_button.place(anchor="center", relx=0.9, rely=0.72)

        self.showTargetTestSplitU_button = ctk.CTkButton(master=self, text='load Train_undersimpled Traget', width=230, height=40,command=lambda:self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].y_trainU))
        self.showTargetTestSplitU_button.configure(fg_color="#200E3A")
        self.showTargetTestSplitU_button.place(anchor="center", relx=0.9, rely=0.87)





        self.split_button = ctk.CTkButton(master=self, text='Submit', font=('Arial', 15), width=300, height=40,
                                          command=lambda:self.applyCNN(str(self.Shuffle_optMenu.get()),
                                                                str(self.random_state_entry.get()),
                                                                str(self.n_neighbors_entry.get()),
                                                                str(self.n_seeds_S_entry.get())
                                                                ))
        self.split_button.configure(fg_color="#200E3A")
        self.split_button.place(anchor="center", relx=0.45, rely=0.86)


    def applyCNN(self,sampling_s='auto',random_s=None,n_n=None,n_s=1):

        X = self.controller.frames[ppf.PrePFrame].X_train
        y = self.controller.frames[ppf.PrePFrame].y_train

        if self.controller.frames[ppf.PrePFrame].df is None :
            tk.messagebox.showerror('Python Error', "Please import a file first.")
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
        self.controller.frames[ppf.PrePFrame].X_trainU, self.controller.frames[ppf.PrePFrame].y_trainU=CNN.fit_resample(X,y)

        tk.messagebox.showinfo('Info', 'Data Split Successfull: \nX_train shape: {} \nX_train_Undersempled shape: {} \ny_train shape: {} \ny_train_Undersempled shape: {}'.format(self.controller.frames[ppf.PrePFrame].X_train.shape,self.controller.frames[ppf.PrePFrame].X_trainU.shape,self.controller.frames[ppf.PrePFrame].y_train.shape,self.controller.frames[ppf.PrePFrame].y_trainU.shape))