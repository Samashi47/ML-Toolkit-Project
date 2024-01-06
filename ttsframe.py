import tkinter as tk
import customtkinter as ctk
from sklearn.model_selection import train_test_split
import ppframe as ppf


class TrainTestSplitFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent,fg_color='transparent',corner_radius=20)
        
        # Train Test Split Frame
        self.TrainS_label = ctk.CTkLabel(self,font=('Arial',17), text="Train Size : ")
        self.TrainS_label.place(anchor="center",relx=0.177, rely=0.2)
        self.train_size_entry = ctk.CTkEntry(self,width=190,height=30,placeholder_text="0 < float < 1 default = 0.8")
        self.train_size_entry.place(relx=0.35, rely=0.21, anchor="center")
        
        self.TestS_label = ctk.CTkLabel(self,font=('Arial',17), text="Test Size : ")
        self.TestS_label.place(anchor="center",relx=0.175, rely=0.4)
        self.test_size_entry = ctk.CTkEntry(self,width=190,height=30,placeholder_text="0 < float < 1 default = 0.2")
        self.test_size_entry.place(relx=0.35, rely=0.41, anchor="center")
        
        self.RandS_label = ctk.CTkLabel(self,font=('Arial',17), text="Random State : ")
        self.RandS_label.place(anchor="center",relx=0.189, rely=0.6)
        self.RandS_entry = ctk.CTkEntry(self,width=190,height=30,placeholder_text="int - default = None")
        self.RandS_entry.place(relx=0.35, rely=0.61, anchor="center")
        
        self.Shuffle_label = ctk.CTkLabel(self,font=('Arial',17), text="Shuffle : ")
        self.Shuffle_label.place(anchor="center",relx=0.53, rely=0.31)
        self.Shuffle_optMenu = ctk.CTkOptionMenu(self,width=190,height=30,values=["True", "False"])
        self.Shuffle_optMenu.configure(fg_color="#200E3A")
        self.Shuffle_optMenu.place(relx=0.65, rely=0.31, anchor="center")
        
        self.TargetCol_label = ctk.CTkLabel(self,font=('Arial',17), text="Target : ")
        self.TargetCol_label.place(anchor="center",relx=0.53, rely=0.5)
        self.targetCol_optMenu = ctk.CTkOptionMenu(self,width=190,height=30,values=[],dynamic_resizing=True)
        self.targetCol_optMenu.configure(fg_color="#200E3A")
        self.targetCol_optMenu.place(relx=0.65, rely=0.51, anchor="center")
        
        self.import_file_button = ctk.CTkButton(master=self,text='Import...',width=200,height=45,command=lambda:self.controller.frames[ppf.PrePFrame].getFile())
        self.import_file_button.configure(fg_color="#200E3A")
        self.import_file_button.place(anchor="center",relx=0.92, rely=0.12)
        
        self.showEntireData_button = ctk.CTkButton(master=self,text='load Entire Dataset',width=200,height=45,command=lambda:self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].df))
        self.showEntireData_button.configure(fg_color="#200E3A")
        self.showEntireData_button.place(anchor="center",relx=0.92, rely=0.27)
        
        self.showTrainSplit_button = ctk.CTkButton(master=self,text='load Train Split',width=200,height=45,command=lambda:self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].X_train))
        self.showTrainSplit_button.configure(fg_color="#200E3A")
        self.showTrainSplit_button.place(anchor="center",relx=0.92, rely=0.42)
        
        self.showTestSplit_button = ctk.CTkButton(master=self,text='load Test Split',width=200,height=45,command=lambda:self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].X_test))
        self.showTestSplit_button.configure(fg_color="#200E3A")
        self.showTestSplit_button.place(anchor="center",relx=0.92, rely=0.57)
        
        self.showTargetTrainSplit_button = ctk.CTkButton(master=self,text='load Train Target',width=200,height=45,command=lambda:self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].y_train))
        self.showTargetTrainSplit_button.configure(fg_color="#200E3A")
        self.showTargetTrainSplit_button.place(anchor="center",relx=0.92, rely=0.72)
        
        self.showTargetTestSplit_button = ctk.CTkButton(master=self,text='load Test Traget',width=200,height=45,command=lambda:self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].y_test))
        self.showTargetTestSplit_button.configure(fg_color="#200E3A")
        self.showTargetTestSplit_button.place(anchor="center",relx=0.92, rely=0.87)
        
        self.split_button = ctk.CTkButton(master=self,text='Split Data',font=('Arial',15),width=400,height=40,
                                          command=lambda:self.splitData(str(self.targetCol_optMenu.get()),
                                                                        str(self.test_size_entry.get()),
                                                                        str(self.train_size_entry.get()),
                                                                        str(self.RandS_entry.get()),
                                                                        str(self.Shuffle_optMenu.get())
                                                                        ))
        self.split_button.configure(fg_color="#200E3A")
        self.split_button.place(anchor="center",relx=0.5, rely=0.9)
        
    def splitData(self,target,test_size=0.2,train_size=0.8,random_state=42,shuffle=True):
        if self.controller.frames[ppf.PrePFrame].df is None :
            tk.messagebox.showerror('Python Error', "Please import a file first.")
            return

        if target not in self.controller.frames[ppf.PrePFrame].df.columns:
            tk.messagebox.showerror('Python Error', "Target column not found. Please enter a valid column name.")
            return
        
        X = self.controller.frames[ppf.PrePFrame].df.drop(target,axis=1)
        y = self.controller.frames[ppf.PrePFrame].df[target]

        if test_size == '':
            test_size = 0.2
        if train_size == '':
            train_size = 0.8
        if random_state == '':
            random_state = None

        if isinstance(test_size, str):
            try:
                test_size = float(test_size)
            except:
                tk.messagebox.showerror('Python Error', "test size must be a float.")
                return
        if isinstance(train_size, str):
            try:
                train_size = float(train_size)
            except:
                tk.messagebox.showerror('Python Error', "train size must be a float.")
                return
        if isinstance(random_state, str) and random_state != 'None':
            try:
                random_state = int(random_state)
            except:
                tk.messagebox.showerror('Python Error', "random state must be an int or None.")
                return
        elif random_state == 'None':
            random_state = None
            
        shuffle = bool(shuffle)

        if (test_size <= 0 or test_size >= 1) or (train_size <= 0 or train_size >= 1):
            tk.messagebox.showerror('Python Error', "Invalid test size. Please enter a value between 0 and 1.")
            return
        
        # Split data into training and testing sets
        self.controller.frames[ppf.PrePFrame].X_train, self.controller.frames[ppf.PrePFrame].X_test, self.controller.frames[ppf.PrePFrame].y_train, self.controller.frames[ppf.PrePFrame].y_test = train_test_split(X, y, test_size=test_size, 
                                                                                train_size=train_size,
                                                                                random_state=random_state,
                                                                                shuffle=shuffle)
        tk.messagebox.showinfo('Info', 'Data Split Successfull: \nX_train shape: {} \nX_test shape: {} \ny_train shape: {} \ny_test shape: {}'.format(self.controller.frames[ppf.PrePFrame].X_train.shape,self.controller.frames[ppf.PrePFrame].X_test.shape,self.controller.frames[ppf.PrePFrame].y_train.shape,self.controller.frames[ppf.PrePFrame].y_test.shape))