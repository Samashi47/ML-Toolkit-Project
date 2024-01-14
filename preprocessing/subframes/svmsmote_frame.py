import tkinter as tk
import customtkinter as ctk
import preprocessing.ppframe as ppf
from imblearn.over_sampling import SVMSMOTE

class SVMSmoteFrame(ctk.CTkFrame):
    """
    A class representing the SVMSmoteFrame, which is a custom frame for applying SVMSMOTE algorithm.

    Args:
        parent: The parent widget.
        controller: The controller object.

    Attributes:
        controller: The controller object.
        svmsmote: The label for SVMSMOTE.
        Strat_label: The label for sampling strategy.
        Strat_optMenu: The option menu for sampling strategy.
        RandS_label: The label for random state.
        RandS_entry: The entry field for random state.
        kNei_label: The label for k-neighbors.
        kNei_entry: The entry field for k-neighbors.
        mNeigh_label: The label for m-neighbors.
        mNeigh_entry: The entry field for m-neighbors.
        outStep_label: The label for out step.
        outStep_entry: The entry field for out step.
        import_file_button: The button for importing a file.
        showEntireData_button: The button for loading the entire dataset.
        showTrainSplit_button: The button for loading the original train data.
        showTestSplit_button: The button for loading the resampled train data.
        showTargetTrainSplit_button: The button for loading the original train target.
        showTargetTestSplit_button: The button for loading the resampled train target.
        rollback_button: The button for rolling back changes.
        SaveChanges_button: The button for saving changes to the dataframe.
        svmsmote_button: The button for applying SVMSMOTE.

    Methods:
        saveChanges: Saves changes to the dataframe.
        rollback: Rolls back changes to the dataframe.
        applySVMSMOTE: Applies SVMSMOTE algorithm to balance the classes.
    """
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent,fg_color='transparent',corner_radius=20)
        
        self.svmsmote = ctk.CTkLabel(self,font=('Arial',30), text="SVMSMOTE: ")
        self.svmsmote.place(anchor="center",relx=0.5, rely=0.07)

        # SVMSMOTE Frame
        
        self.Strat_label = ctk.CTkLabel(self,font=('Arial',17), text="Sampling strategy : ")
        self.Strat_label.place(anchor="center",relx=0.177, rely=0.25)
        self.Strat_optMenu = ctk.CTkOptionMenu(self,width=190,height=30,values=["auto","minority","not minority","not majority","all"])
        self.Strat_optMenu.configure(fg_color="#200E3A")
        self.Strat_optMenu.place(relx=0.35, rely=0.26, anchor="center")
        
        self.RandS_label = ctk.CTkLabel(self,font=('Arial',17), text="Random state : ")
        self.RandS_label.place(anchor="center",relx=0.175, rely=0.45)
        self.RandS_entry = ctk.CTkEntry(self,width=190,height=30,placeholder_text="int - default = None")
        self.RandS_entry.place(relx=0.35, rely=0.46, anchor="center")

        self.kNei_label = ctk.CTkLabel(self,font=('Arial',17), text="K-Neighbors : ")
        self.kNei_label.place(anchor="center",relx=0.175, rely=0.65)
        self.kNei_entry = ctk.CTkEntry(self,width=190,height=30,placeholder_text="int - default = 5")
        self.kNei_entry.place(relx=0.35, rely=0.66, anchor="center")
        
        self.mNeigh_label = ctk.CTkLabel(self,font=('Arial',17), text="m-Neighbors : ")
        self.mNeigh_label.place(anchor="center",relx=0.53, rely=0.36)
        self.mNeigh_entry = ctk.CTkEntry(self,width=190,height=30,placeholder_text="int - default = 10")
        self.mNeigh_entry.place(relx=0.65, rely=0.37, anchor="center")
        
        self.outStep_label = ctk.CTkLabel(self,font=('Arial',17), text="Out Step : ")
        self.outStep_label.place(anchor="center",relx=0.53, rely=0.56)
        self.outStep_entry = ctk.CTkEntry(self,width=190,height=30,placeholder_text="float - default = 0.5")
        self.outStep_entry.place(relx=0.65, rely=0.57, anchor="center")
        
        self.import_file_button = ctk.CTkButton(master=self,text='Import...',width=200,height=35,command=lambda:self.controller.frames[ppf.PrePFrame].getFile())
        self.import_file_button.configure(fg_color="#200E3A")
        self.import_file_button.place(anchor="center",relx=0.92, rely=0.08)
        
        self.showEntireData_button = ctk.CTkButton(master=self,text='Load Entire Dataset',width=200,height=35,command=lambda:self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].df))
        self.showEntireData_button.configure(fg_color="#200E3A")
        self.showEntireData_button.place(anchor="center",relx=0.92, rely=0.2)
        
        self.showTrainSplit_button = ctk.CTkButton(master=self,text='Load Original Train Data',width=200,height=35,command=lambda:self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].X_train))
        self.showTrainSplit_button.configure(fg_color="#200E3A")
        self.showTrainSplit_button.place(anchor="center",relx=0.92, rely=0.32)
        
        self.showTestSplit_button = ctk.CTkButton(master=self,text='Load Resampled Train Data',width=200,height=35,command=lambda:self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].X_train_resampled))
        self.showTestSplit_button.configure(fg_color="#200E3A")
        self.showTestSplit_button.place(anchor="center",relx=0.92, rely=0.44)
        
        self.showTargetTrainSplit_button = ctk.CTkButton(master=self,text='Load Original Train Target',width=200,height=35,command=lambda:self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].y_train))
        self.showTargetTrainSplit_button.configure(fg_color="#200E3A")
        self.showTargetTrainSplit_button.place(anchor="center",relx=0.92, rely=0.56)
        
        self.showTargetTestSplit_button = ctk.CTkButton(master=self,text='Load Resampled Train Traget',width=200,height=35,command=lambda:self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].y_train_resampled))
        self.showTargetTestSplit_button.configure(fg_color="#200E3A")
        self.showTargetTestSplit_button.place(anchor="center",relx=0.92, rely=0.68)
        
        self.rollback_button = ctk.CTkButton(master=self,text='Rollback',width=200,height=35,command=lambda:self.rollback())
        self.rollback_button.configure(fg_color="#200E3A")
        self.rollback_button.place(anchor="center",relx=0.92, rely=0.8)
        
        self.SaveChanges_button = ctk.CTkButton(master=self,text='Save changes to Dataframe',width=200,height=35,command=lambda:self.saveChanges())
        self.SaveChanges_button.configure(fg_color="#200E3A")
        self.SaveChanges_button.place(anchor="center",relx=0.92, rely=0.92)
        
        self.svmsmote_button = ctk.CTkButton(master=self,text='Apply SVMSMOTE',font=('Arial',15),width=400,height=40,
                                          command=lambda:self.applySVMSMOTE(str(self.Strat_optMenu.get()),
                                                                        str(self.RandS_entry.get()),
                                                                        str(self.kNei_entry.get()),
                                                                        str(self.mNeigh_entry.get()),
                                                                        str(self.outStep_entry.get())
                                                                        ))
        self.svmsmote_button.configure(fg_color="#200E3A")
        self.svmsmote_button.place(anchor="center",relx=0.5, rely=0.9)
    
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
    
    def applySVMSMOTE(self,sampling_strategy="auto",random_state=None,k_neighbors=5,m_neighbors=10, out_step=0.5):
        """
        Apply SVMSMOTE algorithm to balance the classes in the training data.

        Parameters:
        - sampling_strategy (str or float or dict, optional): The desired ratio of the number of samples in the minority class over the number of samples in the majority class after resampling. Default is "auto".
        - random_state (int or None, optional): Seed used by the random number generator. Default is None.
        - k_neighbors (int, optional): Number of nearest neighbors to be considered in the majority class. Default is 5.
        - m_neighbors (int, optional): Number of nearest neighbors to be considered in the minority class. Default is 10.
        - out_step (float, optional): Step size for the outlier detection. Default is 0.5.

        Returns:
        - None

        Raises:
        - Python Error: If the data file is not imported or if the data is not split.
        - Python Error: If categorical columns represented as strings are found in the data.
        - Python Error: If k_neighbors, random_state, m_neighbors, or out_step are not of the expected type.

        """
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
        
        if k_neighbors == '':
            k_neighbors = 5
        if random_state == '':
            random_state = None
        if m_neighbors == '':
            m_neighbors = 10
        if out_step == '':
            out_step = 0.5
            
        if isinstance(k_neighbors, str):
            try:
                k_neighbors = int(k_neighbors)
            except:
                tk.messagebox.showerror('Python Error', "k-neighbors must be an int.")
                return
        if isinstance(random_state, str) and random_state != 'None':
            try:
                random_state = int(random_state)
            except:
                tk.messagebox.showerror('Python Error', "random state must be an int or None.")
                return
        if isinstance(m_neighbors, str):
            try:
                m_neighbors = int(m_neighbors)
            except:
                tk.messagebox.showerror('Python Error', "m_neighbors must be an int.")
                return
        if isinstance(out_step, str):
            try:
                out_step = float(out_step)
            except:
                tk.messagebox.showerror('Python Error', "out_step must be an int.")
                return
            
        # Apply SMOTE to balance the classes
        svmsmote = SVMSMOTE(sampling_strategy=sampling_strategy,random_state=random_state,k_neighbors=k_neighbors,m_neighbors=m_neighbors, out_step=out_step)
        try:
            self.controller.frames[ppf.PrePFrame].X_train_resampled, self.controller.frames[ppf.PrePFrame].y_train_resampled = svmsmote.fit_resample(X, y)
        except ValueError as e:
            tk.messagebox.showerror('Python Error', e)
            return

        tk.messagebox.showinfo('Info', 'Shape of X_train after SMOTE is : {} \nShape of y_train after SMOTE is : {}\n SMOTE applied successfully.'.format(self.controller.frames[ppf.PrePFrame].X_train_resampled.shape,self.controller.frames[ppf.PrePFrame].y_train_resampled.shape))