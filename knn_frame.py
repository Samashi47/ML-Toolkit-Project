import tkinter as tk
import customtkinter as ctk
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import numpy as np
import ppframe as ppf

class KNNFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent,fg_color='transparent',corner_radius=20)
        
        self.onehotenc_label = ctk.CTkLabel(self,font=('Arial',20),text="One Hot Encoder: ")
        self.onehotenc_label.place(anchor="center",relx=0.5, rely=0.08)
        
        self.drop_label = ctk.CTkLabel(self,font=('Arial',17),text="drop: ")
        self.drop_label.place(anchor="center",relx=0.175, rely=0.2)
        self.drop_optMenu = ctk.CTkOptionMenu(self, width=190, height=30,values=['None','first','if_binary'],dynamic_resizing=True)
        self.drop_optMenu.configure(fg_color="#200E3A")
        self.drop_optMenu.place(relx=0.35, rely=0.21, anchor="center")
        