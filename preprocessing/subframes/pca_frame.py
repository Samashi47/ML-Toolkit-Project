import tkinter as tk
import customtkinter as ctk
from sklearn.decomposition import PCA
import pandas as pd
import preprocessing.ppframe as ppf
import visualization.vizualization_frame as vsf


class PCAFrame(ctk.CTkFrame):
    """
    A custom frame for performing Principal Component Analysis (PCA) on a dataset.

    Args:
        parent: The parent widget.
        controller: The controller object.

    Attributes:
        pca_label: The label for displaying "PCA:".
        components_label: The label for displaying "n_components:".
        components_entry: The entry field for specifying the number of components.
        copy_label: The label for displaying "copy:".
        copy_optMenu: The option menu for selecting the copy option.
        Target_label: The label for displaying "Target:".
        Target_optMenu: The option menu for selecting the target column.
        whiten_label: The label for displaying "whiten:".
        whiten_optMenu: The option menu for selecting the whiten option.
        svd_solver_label: The label for displaying "svd_solver:".
        svd_solver_optMenu: The option menu for selecting the svd_solver option.
        rand_state_label: The label for displaying "random_state:".
        rand_state_entry: The entry field for specifying the random state.
        import_file_button: The button for importing a file.
        showEntireData_button: The button for loading the original dataset.
        before_pca_button: The button for loading the PCA dataframe.
        rollback_button: The button for rolling back changes.
        saveChanges_button: The button for saving changes to the dataframe.
        pca_button: The button for applying PCA.

    Methods:
        applyPCA: Applies PCA to the dataset.
        saveChanges: Saves the changes made to the dataframe.
        rollback: Rolls back the changes made to the dataframe.
        updateCols: Updates the columns in the dataframe.
    """
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent, fg_color='transparent', corner_radius=20)

        self.pca_label = ctk.CTkLabel(self,font=('Arial',30), text="PCA: ")
        self.pca_label.place(anchor="center",relx=0.5, rely=0.07)
        
        self.components_label = ctk.CTkLabel(self, font=('Arial', 17), text="n_components: ")
        self.components_label.place(anchor="center", relx=0.175, rely=0.2)
        self.components_entry = ctk.CTkEntry(self, width=190, height=30, placeholder_text="None")
        self.components_entry.place(relx=0.35, rely=0.21, anchor="center")

        self.copy_label = ctk.CTkLabel(self, font=('Arial', 17), text="copy: ")
        self.copy_label.place(anchor="center", relx=0.151, rely=0.4)
        self.copy_optMenu = ctk.CTkOptionMenu(self, width=190, height=30, values=["True","False"])
        self.copy_optMenu.configure(fg_color="#200E3A")
        self.copy_optMenu.place(relx=0.35, rely=0.41, anchor="center")

        self.Target_label = ctk.CTkLabel(self, font=('Arial', 17), text="Target : ")
        self.Target_label.place(anchor="center", relx=0.154, rely=0.6)
        self.Target_optMenu = ctk.CTkOptionMenu(self, width=190, height=30, values=[], dynamic_resizing=True)
        self.Target_optMenu.configure(fg_color="#200E3A")
        self.Target_optMenu.place(relx=0.35, rely=0.61, anchor="center")

        self.whiten_label = ctk.CTkLabel(self, font=('Arial', 17), text="whiten: ")
        self.whiten_label.place(anchor="center", relx=0.47, rely=0.2)
        self.whiten_optMenu = ctk.CTkOptionMenu(self, width=190, height=30, values=["True", "False"])
        self.whiten_optMenu.configure(fg_color="#200E3A")
        self.whiten_optMenu.place(relx=0.65, rely=0.21, anchor="center")

        self.svd_solver_label = ctk.CTkLabel(self, font=('Arial', 17), text="svd_solver: ")
        self.svd_solver_label.place(anchor="center", relx=0.482, rely=0.4)
        self.svd_solver_optMenu = ctk.CTkOptionMenu(self, width=190, height=30, values=["auto", "full","arpack","randomized"])
        self.svd_solver_optMenu.configure(fg_color="#200E3A")
        self.svd_solver_optMenu.place(relx=0.65, rely=0.41, anchor="center")

        self.rand_state_label = ctk.CTkLabel(self, font=('Arial', 17), text="random_state : ")
        self.rand_state_label.place(anchor="center", relx=0.49, rely=0.6)
        self.rand_state_entry = ctk.CTkEntry(self, width=190, height=30, placeholder_text="None")
        self.rand_state_entry.place(relx=0.65, rely=0.61, anchor="center")

        self.import_file_button = ctk.CTkButton(master=self, text='Import...', width=200, height=45,command=lambda:self.controller.frames[ppf.PrePFrame].getFile())
        self.import_file_button.configure(fg_color="#200E3A")
        self.import_file_button.place(anchor="center", relx=0.92, rely=0.14)

        self.showEntireData_button = ctk.CTkButton(master=self, text='load original Dataset',width=200, height=45,command=lambda:self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].df))
        self.showEntireData_button.configure(fg_color="#200E3A")
        self.showEntireData_button.place(anchor="center", relx=0.92, rely=0.3)

        self.before_pca_button = ctk.CTkButton(master=self, text='load PCA Dataframe ',width=200, height=45,command=lambda:self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].dfPCA))
        self.before_pca_button.configure(fg_color="#200E3A")
        self.before_pca_button.place(anchor="center", relx=0.92, rely=0.46)

        self.rollback_button = ctk.CTkButton(master=self,text='Rollback',width=200,height=45,command=lambda:self.rollback())
        self.rollback_button.configure(fg_color="#200E3A")
        self.rollback_button.place(anchor="center",relx=0.92, rely=0.62)
        
        self.saveChanges_button = ctk.CTkButton(master=self, text='Save changes to Dataframe', width=200, height=45,command=lambda:self.saveChanges())
        self.saveChanges_button.configure(fg_color="#200E3A")
        self.saveChanges_button.place(anchor="center", relx=0.92, rely=0.78)

        self.pca_button = ctk.CTkButton(master=self, text='Apply PCA', font=('Arial', 15), width=400, height=40,
                                          command=lambda:self.applyPCA(str(self.components_entry.get()),
                                                                       str(self.Target_optMenu.get()),
                                                                       str(self.copy_optMenu.get()),
                                                                       str(self.whiten_optMenu.get()),
                                                                       str(self.svd_solver_optMenu.get()),
                                                                       str(self.rand_state_entry.get())
                                                                      ))

        self.pca_button.configure(fg_color="#200E3A")
        self.pca_button.place(anchor="center", relx=0.5, rely=0.9)


    def applyPCA(self,comp=None,Target=None,cop="True",wh="False",svd="auto",over="10"):
        """
        Apply Principal Component Analysis (PCA) to the data.

        Args:
            comp (int or None): Number of components to keep. If None, all components are kept.
            Target (str): Name of the target column.
            cop (str): Whether to make a copy of the input data. Default is "True".
            wh (str): Whether to whiten the data. Default is "False".
            svd (str or int): SVD solver to use. Default is "auto".
            over (int or None): Random state for the SVD solver. Default is "10".

        Returns:
            None
        """
        if self.controller.frames[ppf.PrePFrame].df is None:
            tk.messagebox.showerror('Python Error', "Please import a file first.")
            return

        if Target not in self.controller.frames[ppf.PrePFrame].df.columns:
            tk.messagebox.showerror('Python Error', "Target column not found. Please enter a valid column name.")
            return

        if self.controller.frames[ppf.PrePFrame].X_train is not None or self.controller.frames[ppf.PrePFrame].y_train is not None:
            tk.messagebox.showerror('Python Error', "Please Note that the changes are not saved in training split (redo the train test split).")
        
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
        try:
            self.controller.frames[ppf.PrePFrame].dfPCA = pd.DataFrame(pca.fit_transform(X),columns=[f"{i+1}" for i in range(pca.fit_transform(X).shape[1])])
        except ValueError as e:
            tk.messagebox.showerror('Python Error', e)
            return
        self.controller.frames[ppf.PrePFrame].dfPCA[Target] = y

        tk.messagebox.showinfo('Info', 'PCA applied Successfully: \nDF shape without PCA : {} \nDF shape with PCA: {} '.format(self.controller.frames[ppf.PrePFrame].df.shape,self.controller.frames[ppf.PrePFrame].dfPCA.shape))
        
    def saveChanges(self):
        if self.controller.frames[ppf.PrePFrame].dfPCA is not None:
            self.controller.frames[ppf.PrePFrame].df = self.controller.frames[ppf.PrePFrame].dfPCA.copy()
            self.controller.frames[ppf.PrePFrame].dfOHE = self.controller.frames[ppf.PrePFrame].df.copy()
            self.controller.frames[ppf.PrePFrame].dfNSC = self.controller.frames[ppf.PrePFrame].df.copy()
            self.controller.frames[ppf.PrePFrame].dfLE = self.controller.frames[ppf.PrePFrame].df.copy()
            self.controller.frames[ppf.PrePFrame].df_msv = self.controller.frames[ppf.PrePFrame].df.copy()
            self.updateCols()
            tk.messagebox.showinfo('Info', 'Changes saved to Dataframe, rollback not available.')
            
    def rollback(self):
        if self.controller.frames[ppf.PrePFrame].dfPCA is not None and self.controller.frames[ppf.PrePFrame].df is not None:
            self.controller.frames[ppf.PrePFrame].dfPCA = self.controller.frames[ppf.PrePFrame].df.copy()
            self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].dfPCA)
            tk.messagebox.showinfo('Info', 'Rollback successful')
            
            
    def updateCols(self):
        
        self.controller.frames[ppf.PrePFrame].dfCols = self.controller.frames[ppf.PrePFrame].df.columns.tolist()
        self.controller.frames[ppf.PrePFrame].dfCols_num = self.controller.frames[ppf.PrePFrame].df_msv.select_dtypes(include='number').columns.tolist()
        self.controller.frames[ppf.PrePFrame].dfCols_cat = self.controller.frames[ppf.PrePFrame].df_msv.select_dtypes(include='object').columns.tolist()
        self.controller.frames[ppf.PrePFrame].train_test_split_frame.targetCol_optMenu.configure(values=self.controller.frames[ppf.PrePFrame].dfCols)
        self.controller.frames[ppf.PrePFrame].train_test_split_frame.targetCol_optMenu.configure(variable=tk.StringVar(value=self.controller.frames[ppf.PrePFrame].dfCols[-1]))
        
        self.controller.frames[ppf.PrePFrame].norm_sc_frame.nCols_optMenu.configure(values=self.controller.frames[ppf.PrePFrame].dfNSC.columns.tolist())
        self.controller.frames[ppf.PrePFrame].norm_sc_frame.nCols_optMenu.configure(variable=tk.StringVar(value=self.controller.frames[ppf.PrePFrame].dfNSC.columns.tolist()[-1]))
        self.controller.frames[ppf.PrePFrame].norm_sc_frame.scCols_optMenu.configure(values=self.controller.frames[ppf.PrePFrame].dfNSC.columns.tolist())
        self.controller.frames[ppf.PrePFrame].norm_sc_frame.scCols_optMenu.configure(variable=tk.StringVar(value=self.controller.frames[ppf.PrePFrame].dfNSC.columns.tolist()[-1]))
        self.controller.frames[ppf.PrePFrame].norm_sc_frame.mmCols_optMenu.configure(values=self.controller.frames[ppf.PrePFrame].dfNSC.columns.tolist())
        self.controller.frames[ppf.PrePFrame].norm_sc_frame.mmCols_optMenu.configure(variable=tk.StringVar(value=self.controller.frames[ppf.PrePFrame].dfNSC.columns.tolist()[-1]))
        self.controller.frames[ppf.PrePFrame].norm_sc_frame.mabsCols_optMenu.configure(values=self.controller.frames[ppf.PrePFrame].dfNSC.columns.tolist())
        self.controller.frames[ppf.PrePFrame].norm_sc_frame.mabsCols_optMenu.configure(variable=tk.StringVar(value=self.controller.frames[ppf.PrePFrame].dfNSC.columns.tolist()[-1]))
        
        self.controller.frames[ppf.PrePFrame].ohe_frame.target_optMenu.configure(values=self.controller.frames[ppf.PrePFrame].dfOHE.columns.tolist())
        self.controller.frames[ppf.PrePFrame].ohe_frame.target_optMenu.configure(variable=tk.StringVar(value=self.controller.frames[ppf.PrePFrame].dfOHE.columns.tolist()[-1]))  
        
        self.controller.frames[ppf.PrePFrame].le_frame.target_optMenu.configure(values=self.controller.frames[ppf.PrePFrame].dfLE.columns.tolist())
        self.controller.frames[ppf.PrePFrame].le_frame.target_optMenu.configure(variable=tk.StringVar(value=self.controller.frames[ppf.PrePFrame].dfLE.columns.tolist()[-1]))
        
        self.Target_optMenu.configure(values=self.controller.frames[ppf.PrePFrame].dfCols)
        self.Target_optMenu.configure(variable=tk.StringVar(value=self.controller.frames[ppf.PrePFrame].dfCols[-1]))
        
        self.controller.frames[vsf.visulizeFrame].matplotlib_frame.x_dropdown.configure(values=self.controller.frames[ppf.PrePFrame].dfCols)
        self.controller.frames[vsf.visulizeFrame].matplotlib_frame.x_dropdown.configure(variable=tk.StringVar(value=self.controller.frames[ppf.PrePFrame].dfCols[-1]))
        self.controller.frames[vsf.visulizeFrame].matplotlib_frame.y_dropdown.configure(variable=tk.StringVar(value=self.controller.frames[ppf.PrePFrame].dfCols[-1]))
        self.controller.frames[vsf.visulizeFrame].matplotlib_frame.y_dropdown.configure(values=self.controller.frames[ppf.PrePFrame].dfCols)
        self.controller.frames[vsf.visulizeFrame].matplotlib_frame.z_dropdown.configure(values=self.controller.frames[ppf.PrePFrame].dfCols)
        self.controller.frames[vsf.visulizeFrame].matplotlib_frame.z_dropdown.configure(variable=tk.StringVar(value=self.controller.frames[ppf.PrePFrame].dfCols[-1]))
        
        self.controller.frames[vsf.visulizeFrame].seaborn_frame.x_dropdown.configure(values=self.controller.frames[ppf.PrePFrame].dfCols)
        self.controller.frames[vsf.visulizeFrame].seaborn_frame.x_dropdown.configure(variable=tk.StringVar(value=self.controller.frames[ppf.PrePFrame].dfCols[-1]))
        self.controller.frames[vsf.visulizeFrame].seaborn_frame.y_dropdown.configure(values=self.controller.frames[ppf.PrePFrame].dfCols)
        self.controller.frames[vsf.visulizeFrame].seaborn_frame.y_dropdown.configure(variable=tk.StringVar(value=self.controller.frames[ppf.PrePFrame].dfCols[-1]))
        
        self.controller.frames[ppf.PrePFrame].msv_frame.Cols_optMenu.configure(values=list(self.controller.frames[ppf.PrePFrame].dfCols))
        if len(self.controller.frames[ppf.PrePFrame].dfCols_num)>0:
            self.controller.frames[ppf.PrePFrame].msv_frame.replaceMean_optMenu.configure(values=list(self.controller.frames[ppf.PrePFrame].dfCols_num))
        self.controller.frames[ppf.PrePFrame].msv_frame.Cols_optMenu.configure(variable=tk.StringVar(value=self.controller.frames[ppf.PrePFrame].dfCols[-1]))
        
        if len(self.controller.frames[ppf.PrePFrame].dfCols_num) > 0:
            self.controller.frames[ppf.PrePFrame].msv_frame.replaceMean_optMenu.configure(variable=tk.StringVar(value=self.controller.frames[ppf.PrePFrame].dfCols_num[-1]))
            self.controller.frames[ppf.PrePFrame].msv_frame.replaceMedian_optMenu.configure(values=list(self.controller.frames[ppf.PrePFrame].dfCols_num))
            self.controller.frames[ppf.PrePFrame].msv_frame.replaceMedian_optMenu.configure(variable=tk.StringVar(value=self.controller.frames[ppf.PrePFrame].dfCols_num[-1]))
            self.controller.frames[ppf.PrePFrame].msv_frame.replaceMode_optMenu.configure(values=list(self.controller.frames[ppf.PrePFrame].dfCols_cat))
        if len(self.controller.frames[ppf.PrePFrame].dfCols_cat) > 0:
            self.controller.frames[ppf.PrePFrame].msv_frame.replaceMode_optMenu.configure(variable=tk.StringVar(value=self.controller.frames[ppf.PrePFrame].dfCols_cat[-1]))
        self.controller.frames[ppf.PrePFrame].msv_frame.replaceWithValue_optMenu.configure(values=list(self.controller.frames[ppf.PrePFrame].dfCols))
        self.controller.frames[ppf.PrePFrame].msv_frame.replaceWithValue_optMenu.configure(variable=tk.StringVar(value=self.controller.frames[ppf.PrePFrame].dfCols[-1]))