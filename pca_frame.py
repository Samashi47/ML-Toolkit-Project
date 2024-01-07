import tkinter as tk
import customtkinter as ctk
from sklearn.decomposition import PCA
import pandas as pd
import ppframe as ppf


class PCAFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent, fg_color='transparent', corner_radius=20)

        self.components_label = ctk.CTkLabel(self, font=('Arial', 17), text="n_components: ")
        self.components_label.place(anchor="center", relx=0.175, rely=0.2)
        self.components_entry = ctk.CTkEntry(self, width=190, height=30, placeholder_text="None")
        self.components_entry.place(relx=0.35, rely=0.21, anchor="center")

        self.copy_label = ctk.CTkLabel(self, font=('Arial', 17), text="copy: ")
        self.copy_label.place(anchor="center", relx=0.177, rely=0.4)
        self.copy_optMenu = ctk.CTkOptionMenu(self, width=190, height=30, values=["True","False"])
        self.copy_optMenu.configure(fg_color="#200E3A")
        self.copy_optMenu.place(relx=0.35, rely=0.41, anchor="center")

        self.Target_label = ctk.CTkLabel(self, font=('Arial', 17), text="Target : ")
        self.Target_label.place(anchor="center", relx=0.177, rely=0.6)
        self.Target_optMenu = ctk.CTkOptionMenu(self, width=190, height=30, values=[], dynamic_resizing=True)
        self.Target_optMenu.configure(fg_color="#200E3A")
        self.Target_optMenu.place(relx=0.35, rely=0.61, anchor="center")

        self.whiten_label = ctk.CTkLabel(self, font=('Arial', 17), text="whiten: ")
        self.whiten_label.place(anchor="center", relx=0.53, rely=0.2)
        self.whiten_optMenu = ctk.CTkOptionMenu(self, width=190, height=30, values=["True", "False"])
        self.whiten_optMenu.configure(fg_color="#200E3A")
        self.whiten_optMenu.place(relx=0.65, rely=0.21, anchor="center")

        self.svd_solver_label = ctk.CTkLabel(self, font=('Arial', 17), text="svd_solver: ")
        self.svd_solver_label.place(anchor="center", relx=0.53, rely=0.4)
        self.svd_solver_optMenu = ctk.CTkOptionMenu(self, width=190, height=30, values=["auto", "full","arpack","randomized"])
        self.svd_solver_optMenu.configure(fg_color="#200E3A")
        self.svd_solver_optMenu.place(relx=0.65, rely=0.41, anchor="center")

        self.samples_label = ctk.CTkLabel(self, font=('Arial', 17), text="random_state : ")
        self.samples_label.place(anchor="center", relx=0.53, rely=0.6)
        self.samples_entry = ctk.CTkEntry(self, width=190, height=30, placeholder_text="None")
        self.samples_entry.place(relx=0.65, rely=0.61, anchor="center")

        self.import_file_button = ctk.CTkButton(master=self, text='Import...', width=230, height=40,command=lambda:self.controller.frames[ppf.PrePFrame].getFile())
        self.import_file_button.configure(fg_color="#200E3A")
        self.import_file_button.place(anchor="center", relx=0.9, rely=0.27)

        self.showEntireData_button = ctk.CTkButton(master=self, text='load original Dataset',width=230, height=40,command=lambda:self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].df))
        self.showEntireData_button.configure(fg_color="#200E3A")
        self.showEntireData_button.place(anchor="center", relx=0.9, rely=0.42)

        self.before_pca_button = ctk.CTkButton(master=self, text='load PCA Dataframe ',width=230, height=40,command=lambda:self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].dfPCA))
        self.before_pca_button.configure(fg_color="#200E3A")
        self.before_pca_button.place(anchor="center", relx=0.9, rely=0.57)

        self.after_pca_button = ctk.CTkButton(master=self, text='Save changes to Dataframe', width=230, height=40,command=lambda:self.saveChanges())
        self.after_pca_button.configure(fg_color="#200E3A")
        self.after_pca_button.place(anchor="center", relx=0.9, rely=0.72)

        self.pca_button = ctk.CTkButton(master=self, text='Submit', font=('Arial', 15), width=300, height=40,
                                          command=lambda:self.applyPCA(str(self.components_entry.get()),
                                                                       str(self.Target_optMenu.get()),
                                                                       str(self.copy_optMenu.get()),
                                                                       str(self.whiten_optMenu.get()),
                                                                       str(self.svd_solver_optMenu.get()),
                                                                       str(self.samples_entry.get())
                                                                      ))

        self.pca_button.configure(fg_color="#200E3A")
        self.pca_button.place(anchor="center", relx=0.45, rely=0.86)


    def applyPCA(self,comp=None,Target=None,cop="True",wh="False",svd="auto",over="10"):

        if self.controller.frames[ppf.PrePFrame].df is None:
            tk.messagebox.showerror('Python Error', "Please import a file first.")
            return

        if Target not in self.controller.frames[ppf.PrePFrame].df.columns:
            tk.messagebox.showerror('Python Error', "Target column not found. Please enter a valid column name.")
            return

        X = self.controller.frames[ppf.PrePFrame].df.drop(Target, axis=1)
        y = self.controller.frames[ppf.PrePFrame].df[Target]
        
        if any(X.dtypes == object):
            tk.messagebox.showerror('Python Error', "Categorical columns represented as strings are not supported. Please convert them to numerical values.")
            return

        if comp== '':
            comp = None
        if over== '':
            over = None

        if isinstance(comp, str) and comp != 'None':
            try:
                comp = int(comp)
            except:
                tk.messagebox.showerror('Python Error', "n_components must be an int or None.")
                return
        elif comp == 'None':
            comp = None
        if isinstance(over, str) and over != 'None':
            try:
                over = int(over)
            except:
                tk.messagebox.showerror('Python Error', "random_state must be an Int.")
                return
        elif over == 'None':
            over = 0
            # Convert 'cop' to boolean
        cop = True if cop.lower() == 'true' else False
        wh = True if wh.lower() == 'true' else False


        pca = PCA(n_components=comp,copy=cop,whiten=wh,svd_solver=svd,random_state=over)
        
        self.controller.frames[ppf.PrePFrame].dfPCA = pd.DataFrame(pca.fit_transform(X))
        self.controller.frames[ppf.PrePFrame].dfPCA[Target] = y

        tk.messagebox.showinfo('Info', 'PCA applied Successfully: \nDF shape without PCA : {} \nDF shape with PCA: {} '.format(self.controller.frames[ppf.PrePFrame].df.shape,self.controller.frames[ppf.PrePFrame].dfPCA.shape))
        
    def saveChanges(self):
        if self.controller.frames[ppf.PrePFrame].dfPCA is not None:
            self.controller.frames[ppf.PrePFrame].df = self.controller.frames[ppf.PrePFrame].dfPCA
            tk.messagebox.showinfo('Info', 'Changes saved to Dataframe')