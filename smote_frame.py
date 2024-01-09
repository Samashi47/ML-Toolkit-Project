import tkinter as tk
import customtkinter as ctk
import pandas as pd
from imblearn.over_sampling import SMOTE
import ppframe as ppf

class SmoteFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent,fg_color='transparent',corner_radius=20)
        
        self.test = ctk.CTkLabel(self,font=('Arial',30), text="Khay smotix : ")
        self.test.place(anchor="center",relx=0.5, rely=0.5)
    
    
    def applySMOTE(self):
        if self.X_train is None or self.y_train is None:
            print("Please import and split data first.")
            return

        # Apply SMOTE to balance the classes
        smote = SMOTE(sampling_strategy=0.5,random_state=42)
        X_train_resampled, y_train_resampled = smote.fit_resample(self.X_train, self.y_train)

        # Update X_train and y_train with resampled data
        self.X_train = pd.DataFrame(X_train_resampled, columns=self.X_train.columns)
        self.y_train = pd.Series(y_train_resampled, name=self.y_train.name)
        print("Shape of X_train after SMOTE is :", self.X_train.shape)
        print("Shape of y_train after SMOTE is :", self.y_train.shape)
        print("SMOTE applied successfully.")