import tkinter as tk
import customtkinter as ctk
import pandas as pd
import sys
import os
import io
import preprocessing.ppframe as ppf
import visualization.vizualization_frame as vsf

class MissingValsFrame(ctk.CTkFrame):
    """
    A custom frame for handling missing values in a DataFrame.

    Attributes:
        controller (object): The parent controller object.
        removeCol_label (ctk.CTkLabel): Label for removing columns.
        Cols_optMenu (ctk.CTkOptionMenu): Option menu for selecting columns to remove.
        removeCol_button (ctk.CTkButton): Button for removing columns.
        seph (tk.ttk.Separator): Horizontal separator.
        sep1v (tk.ttk.Separator): Vertical separator.
        removeRow_label (ctk.CTkLabel): Label for removing rows with null values.
        removeRow_button (ctk.CTkButton): Button for removing rows with null values.
        replaceMean_label (ctk.CTkLabel): Label for replacing with mean.
        replaceMean_optMenu (ctk.CTkOptionMenu): Option menu for selecting columns to replace with mean.
        replaceMean_button (ctk.CTkButton): Button for replacing with mean.
        replaceMode_label (ctk.CTkLabel): Label for replacing with mode.
        replaceMode_optMenu (ctk.CTkOptionMenu): Option menu for selecting columns to replace with mode.
        replaceMode_button (ctk.CTkButton): Button for replacing with mode.
        sep2v (tk.ttk.Separator): Vertical separator.
        replaceMedian_label (ctk.CTkLabel): Label for replacing with median.
        replaceMedian_optMenu (ctk.CTkOptionMenu): Option menu for selecting columns to replace with median.
        replaceMedian_button (ctk.CTkButton): Button for replacing with median.
        replaceWithValue_label (ctk.CTkLabel): Label for replacing with a specific value.
        replaceWithValue_optMenu (ctk.CTkOptionMenu): Option menu for selecting columns to replace with a specific value.
        replaceWithValue_entry (ctk.CTkEntry): Entry field for entering the specific value.
        replaceWithValue_button (ctk.CTkButton): Button for replacing with a specific value.
        import_file_button (ctk.CTkButton): Button for importing a file.
        showEntireData_button (ctk.CTkButton): Button for loading the original dataset.
        loadMissValsDF_button (ctk.CTkButton): Button for loading the missing values DataFrame.
        CountMissVals_button (ctk.CTkButton): Button for counting missing values.
        printDFInfo_button (ctk.CTkButton): Button for showing DataFrame info.
        rollback_button (ctk.CTkButton): Button for rolling back changes.
        SaveChanges_button (ctk.CTkButton): Button for saving changes to DataFrame.
        toplevel_window (object): Top-level window object for displaying information.

    Methods:
        printMissingVals: Prints the count of missing values in the DataFrame.
        saveChanges: Saves the changes made to the DataFrame.
        rollback: Rolls back the changes made to the DataFrame.
        printDFInfo: Prints information about the DataFrame.
        removeCol: Removes a column from the DataFrame.
    """
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent,fg_color='transparent',corner_radius=20)
        
        pd.set_option('display.max_rows', None)  # Set option to display all rows
        
        # Missing Values Frame
        
        self.removeCol_label = ctk.CTkLabel(self,font=('Arial',17), text="Remove Columns : ")
        self.removeCol_label.place(anchor="center",relx=0.13, rely=0.16)
        self.Cols_optMenu = ctk.CTkOptionMenu(self, width=190, height=30,values=[],dynamic_resizing=True)
        self.Cols_optMenu.configure(fg_color="#200E3A")
        self.Cols_optMenu.place(relx=0.13, rely=0.30, anchor="center")
        self.removeCol_button = ctk.CTkButton(master=self,text='Remove',width=190,height=30,command=lambda:self.removeCol(self.Cols_optMenu.get()))
        self.removeCol_button.configure(fg_color="#200E3A")
        self.removeCol_button.place(anchor="center",relx=0.13, rely=0.44)
        
        self.seph = tk.ttk.Separator(self, orient='horizontal', style='TSeparator')
        self.seph.place(relx=0.01, rely=0.55, width=1260, bordermode="outside")
        
        self.sep1v = tk.ttk.Separator(self, orient='vertical')
        self.sep1v.place(relx=0.25, rely=0.1, height=400, bordermode="outside")
        
        self.removeRow_label = ctk.CTkLabel(self,font=('Arial',17), text="Remove Rows With Null Values:")
        self.removeRow_label.place(anchor="center",relx=0.13, rely=0.64)
        self.removeRow_button = ctk.CTkButton(master=self,text='Remove rows w/ Nulls',width=190,height=45,command=lambda:self.removeNArows())
        self.removeRow_button.configure(fg_color="#200E3A")
        self.removeRow_button.place(anchor="center",relx=0.13, rely=0.82)

        self.replaceMean_label = ctk.CTkLabel(self,font=('Arial',17), text="Replace with mean : ")
        self.replaceMean_label.place(anchor="center",relx=0.4, rely=0.16)
        self.replaceMean_optMenu = ctk.CTkOptionMenu(self, width=190, height=30,values=[],dynamic_resizing=True)
        self.replaceMean_optMenu.configure(fg_color="#200E3A")
        self.replaceMean_optMenu.place(relx=0.4, rely=0.30, anchor="center")
        self.replaceMean_button = ctk.CTkButton(master=self,text='Replace',width=190,height=30,command=lambda:self.replaceWithMean(self.replaceMean_optMenu.get()))
        self.replaceMean_button.configure(fg_color="#200E3A")
        self.replaceMean_button.place(anchor="center",relx=0.4, rely=0.44)
        
        self.replaceMode_label = ctk.CTkLabel(self,font=('Arial',17), text="Replace with mode : ")
        self.replaceMode_label.place(anchor="center",relx=0.7, rely=0.16)
        self.replaceMode_optMenu = ctk.CTkOptionMenu(self, width=190, height=30,values=[],dynamic_resizing=True)
        self.replaceMode_optMenu.configure(fg_color="#200E3A")
        self.replaceMode_optMenu.place(relx=0.7, rely=0.30, anchor="center")
        self.replaceMode_button = ctk.CTkButton(master=self,text='Replace',width=190,height=30, command=lambda:self.replaceWithMode(self.replaceMode_optMenu.get()))
        self.replaceMode_button.configure(fg_color="#200E3A")
        self.replaceMode_button.place(anchor="center",relx=0.7, rely=0.44)
        
        self.sep2v = tk.ttk.Separator(self, orient='vertical')
        self.sep2v.place(relx=0.55, rely=0.1, height=400, bordermode="outside")
        
        self.replaceMedian_label = ctk.CTkLabel(self,font=('Arial',17), text="Replace with median : ")
        self.replaceMedian_label.place(anchor="center",relx=0.4, rely=0.64)
        self.replaceMedian_optMenu = ctk.CTkOptionMenu(self, width=190, height=30,values=[],dynamic_resizing=True)
        self.replaceMedian_optMenu.configure(fg_color="#200E3A")
        self.replaceMedian_optMenu.place(relx=0.4, rely=0.78, anchor="center")
        self.replaceMedian_button = ctk.CTkButton(master=self,text='Replace',width=190,height=30,command=lambda:self.replaceWithMedian(self.replaceMedian_optMenu.get()))
        self.replaceMedian_button.configure(fg_color="#200E3A")
        self.replaceMedian_button.place(anchor="center",relx=0.4, rely=0.92)
        
        self.replaceWithValue_label = ctk.CTkLabel(self,font=('Arial',17), text="Replace with value : ")
        self.replaceWithValue_label.place(anchor="center",relx=0.7, rely=0.64)
        self.replaceWithValue_optMenu = ctk.CTkOptionMenu(self, width=145, height=30,values=[],dynamic_resizing=True)
        self.replaceWithValue_optMenu.configure(fg_color="#200E3A")
        self.replaceWithValue_optMenu.place(relx=0.63, rely=0.78, anchor="center")
        self.replaceWithValue_entry = ctk.CTkEntry(self, width=145, height=30,placeholder_text="Enter value")
        self.replaceWithValue_entry.place(relx=0.76, rely=0.78, anchor="center")
        self.replaceWithValue_button = ctk.CTkButton(master=self,text='Replace',width=190,height=30,command=lambda:self.replaceWithValue(self.replaceWithValue_optMenu.get(),self.replaceWithValue_entry.get()))
        self.replaceWithValue_button.configure(fg_color="#200E3A")
        self.replaceWithValue_button.place(anchor="center",relx=0.7, rely=0.92)
               
        self.import_file_button = ctk.CTkButton(master=self,text='Import...',width=200,height=40,command=lambda:self.controller.frames[ppf.PrePFrame].getFile())
        self.import_file_button.configure(fg_color="#200E3A")
        self.import_file_button.place(anchor="center",relx=0.92, rely=0.08)
        
        self.showEntireData_button = ctk.CTkButton(master=self,text='Load Original Dataset',width=200,height=40,command=lambda:self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].df))
        self.showEntireData_button.configure(fg_color="#200E3A")
        self.showEntireData_button.place(anchor="center",relx=0.92, rely=0.22)
        
        self.loadMissValsDF_button = ctk.CTkButton(master=self,text='Load missing values Dataframe',width=200,height=40,command=lambda:self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].df_msv))
        self.loadMissValsDF_button.configure(fg_color="#200E3A")
        self.loadMissValsDF_button.place(anchor="center",relx=0.92, rely=0.36)
        
        self.CountMissVals_button = ctk.CTkButton(master=self,text='Count missing values',width=200,height=40,command=lambda:self.printMissingVals())
        self.CountMissVals_button.configure(fg_color="#200E3A")
        self.CountMissVals_button.place(anchor="center",relx=0.92, rely=0.5)
        
        self.printDFInfo_button = ctk.CTkButton(master=self,text='Show Dataframe info',width=200,height=40,command=lambda:self.printDFInfo())
        self.printDFInfo_button.configure(fg_color="#200E3A")
        self.printDFInfo_button.place(anchor="center",relx=0.92, rely=0.64)
        
        self.rollback_button = ctk.CTkButton(master=self,text='Rollback',width=200,height=40,command=lambda:self.rollback())
        self.rollback_button.configure(fg_color="#200E3A")
        self.rollback_button.place(anchor="center",relx=0.92, rely=0.78)
        
        self.SaveChanges_button = ctk.CTkButton(master=self,text='Save changes to Dataframe',width=200,height=40,command=lambda:self.saveChanges())
        self.SaveChanges_button.configure(fg_color="#200E3A")
        self.SaveChanges_button.place(anchor="center",relx=0.92, rely=0.92)
        
        self.toplevel_window = None
        
    def printMissingVals(self):
        """
        Prints the count of missing values in the DataFrame.
        """
        if self.controller.frames[ppf.PrePFrame].df_msv is not None:
            MissVals = str(self.controller.frames[ppf.PrePFrame].df_msv.isnull().sum())
            if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
                self.toplevel_window = ToplevelWindow(MissVals)  # create window if its None or destroyed
            else:
                self.toplevel_window.focus()  # if window exists focus it
        
    def saveChanges(self):
        """
        Saves the changes made to the DataFrame.
        """
        if self.controller.frames[ppf.PrePFrame].df_msv is not None:
            self.controller.frames[ppf.PrePFrame].df = self.controller.frames[ppf.PrePFrame].df_msv.copy()
            self.controller.frames[ppf.PrePFrame].dfPCA = self.controller.frames[ppf.PrePFrame].df.copy()
            self.controller.frames[ppf.PrePFrame].dfLE = self.controller.frames[ppf.PrePFrame].df.copy()
            self.controller.frames[ppf.PrePFrame].dfOHE = self.controller.frames[ppf.PrePFrame].df.copy()
            self.controller.frames[ppf.PrePFrame].dfNSC = self.controller.frames[ppf.PrePFrame].df.copy()
            self.updateCols()
            tk.messagebox.showinfo('Info', 'Changes saved to Dataframe, rollback not available.')
            
    def rollback(self):
        """
        Rolls back the changes made to the DataFrame.
        """
        if self.controller.frames[ppf.PrePFrame].df_msv is not None and self.controller.frames[ppf.PrePFrame].df is not None:
            self.controller.frames[ppf.PrePFrame].df_msv = self.controller.frames[ppf.PrePFrame].df.copy()
            self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].df_msv)
            tk.messagebox.showinfo('Info', 'Rollback successful')
            
    def printDFInfo(self):
        """
        Prints information about the DataFrame.
        """
        if self.controller.frames[ppf.PrePFrame].df_msv is not None:
            # Redirect the standard output to a StringIO object
            output = io.StringIO()
            sys.stdout = output

            # Call the df.info() method
            self.controller.frames[ppf.PrePFrame].df_msv.info()

            # Get the output as a string
            DFInfo = output.getvalue()

            # Reset the standard output
            sys.stdout = sys.__stdout__

            if DFInfo:
                if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
                    self.toplevel_window = ToplevelWindow(DFInfo)  # create window if it's None or destroyed
                else:
                    self.toplevel_window.focus()
            else:
                print("No information available for the DataFrame.")
                
    def removeCol(self, col):
        """
        Removes a column from the DataFrame.

        Args:
            col (str): The name of the column to remove.
        """
        if self.controller.frames[ppf.PrePFrame].df_msv is not None:
            if col in self.controller.frames[ppf.PrePFrame].dfCols:
                self.controller.frames[ppf.PrePFrame].df_msv.drop(col, axis=1, inplace=True)
                self.controller.frames[ppf.PrePFrame].dfCols = self.controller.frames[ppf.PrePFrame].df_msv.columns.tolist()
                self.controller.frames[ppf.PrePFrame].dfCols_num = self.controller.frames[ppf.PrePFrame].df_msv.select_dtypes(include='number').columns.tolist()
                self.controller.frames[ppf.PrePFrame].dfCols_cat = self.controller.frames[ppf.PrePFrame].df_msv.select_dtypes(include='object').columns.tolist()
                self.Cols_optMenu.configure(values=list(self.controller.frames[ppf.PrePFrame].dfCols))
                if len(self.controller.frames[ppf.PrePFrame].dfCols_num)>0:
                    self.replaceMean_optMenu.configure(values=list(self.controller.frames[ppf.PrePFrame].dfCols_num))
                self.Cols_optMenu.configure(variable=tk.StringVar(value=self.controller.frames[ppf.PrePFrame].dfCols[-1]))
                
                if len(self.controller.frames[ppf.PrePFrame].dfCols_num) > 0:
                    self.replaceMean_optMenu.configure(variable=tk.StringVar(value=self.controller.frames[ppf.PrePFrame].dfCols_num[-1]))
                    self.replaceMedian_optMenu.configure(values=list(self.controller.frames[ppf.PrePFrame].dfCols_num))
                    self.replaceMedian_optMenu.configure(variable=tk.StringVar(value=self.controller.frames[ppf.PrePFrame].dfCols_num[-1]))
                    self.replaceMode_optMenu.configure(values=list(self.controller.frames[ppf.PrePFrame].dfCols_cat))
                if len(self.controller.frames[ppf.PrePFrame].dfCols_cat) > 0:
                    self.replaceMode_optMenu.configure(variable=tk.StringVar(value=self.controller.frames[ppf.PrePFrame].dfCols_cat[-1]))
                self.replaceWithValue_optMenu.configure(values=list(self.controller.frames[ppf.PrePFrame].dfCols))
                self.replaceWithValue_optMenu.configure(variable=tk.StringVar(value=self.controller.frames[ppf.PrePFrame].dfCols[-1]))
                self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].df_msv)
                tk.messagebox.showinfo('Info', 'Column removed from MV Dataframe')
            else:
                tk.messagebox.showerror('Python Error', "Please select a column from the list.")
                return
            
    def updateCols(self):
        """
        Updates the columns in various dropdown menus based on the current dataframe.
        """
        
        self.controller.frames[ppf.PrePFrame].dfCols = self.controller.frames[ppf.PrePFrame].df.columns.tolist()

        self.controller.frames[ppf.PrePFrame].train_test_split_frame.targetCol_optMenu.configure(values=list(self.controller.frames[ppf.PrePFrame].dfCols))
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
        
        self.controller.frames[ppf.PrePFrame].pca_frame.Target_optMenu.configure(values=self.controller.frames[ppf.PrePFrame].dfCols)
        self.controller.frames[ppf.PrePFrame].pca_frame.Target_optMenu.configure(variable=tk.StringVar(value=self.controller.frames[ppf.PrePFrame].dfCols[-1]))
        
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
            
    def removeNArows(self):
        """
        Removes rows containing null values from the MV Dataframe.

        If the MV Dataframe contains null values, this method drops the rows
        with null values and updates the MV Dataframe accordingly. It also
        displays the updated MV Dataframe and shows an information message
        indicating that rows with null values have been removed. If the MV
        Dataframe does not contain any null values, it shows an error message
        indicating that there are no null values in the Dataframe.

        Returns:
            None
        """
        if self.controller.frames[ppf.PrePFrame].df_msv is not None:
            if self.controller.frames[ppf.PrePFrame].df_msv.isnull().values.any():
                self.controller.frames[ppf.PrePFrame].df_msv.dropna(inplace=True)
                self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].df_msv)
                tk.messagebox.showinfo('Info', 'Rows with null values removed from MV Dataframe')
            else:
                tk.messagebox.showerror('Python Error', "No null values in the Dataframe.")
                return
            
    def replaceWithMean(self,col):
        """
        Replace null values in a specific column with the mean value of that column.

        Args:
            col (str): The name of the column to replace null values in.

        Returns:
            None
        """
        if self.controller.frames[ppf.PrePFrame].df_msv is not None:
            if self.controller.frames[ppf.PrePFrame].df_msv[col].isnull().values.any():
                self.controller.frames[ppf.PrePFrame].df_msv[col].fillna(self.controller.frames[ppf.PrePFrame].df_msv[col].mean(), inplace=True)
                self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].df_msv)
                tk.messagebox.showinfo('Info', 'Null values replaced with mean in MV Dataframe')
            else:
                tk.messagebox.showerror('Python Error', "No null values in the column.")
                return
    
    
        
    def replaceWithMedian(self,col):
        """
        Replaces null values in a specific column with the median value of that column.

        Args:
            col (str): The name of the column to replace null values in.

        Returns:
            None
        """
        if self.controller.frames[ppf.PrePFrame].df_msv is not None:
            if self.controller.frames[ppf.PrePFrame].df_msv[col].isnull().values.any():
                self.controller.frames[ppf.PrePFrame].df_msv[col].fillna(self.controller.frames[ppf.PrePFrame].df_msv[col].median(), inplace=True)
                self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].df_msv)
                tk.messagebox.showinfo('Info', 'Null values replaced with median in MV Dataframe')
            else:
                tk.messagebox.showerror('Python Error', "No null values in the column.")
                return
            
    def replaceWithMode(self,col):
        """
        Replaces null values in a specific column with the mode value.

        Args:
            col (str): The name of the column to replace null values in.

        Returns:
            None
        """
        if self.controller.frames[ppf.PrePFrame].df_msv is not None:
            if self.controller.frames[ppf.PrePFrame].df_msv[col].isnull().values.any():
                self.controller.frames[ppf.PrePFrame].df_msv[col].fillna(self.controller.frames[ppf.PrePFrame].df_msv[col].mode()[0], inplace=True)
                self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].df_msv)
                tk.messagebox.showinfo('Info', 'Null values replaced with mode in MV Dataframe')
            else:
                tk.messagebox.showerror('Python Error', "No null values in the column.")
                return
            
    def replaceWithValue(self, col, value):
        """
        Replaces null values in a specific column of the dataframe with a given value.

        Args:
            col (str): The name of the column to replace null values in.
            value (str or int or float): The value to replace null values with.

        Returns:
            None
        """
        if self.controller.frames[ppf.PrePFrame].df_msv is not None:
            if self.controller.frames[ppf.PrePFrame].df_msv[col].isnull().values.any():
                if value.isnumeric() and self.controller.frames[ppf.PrePFrame].df_msv[col].dtype != 'object':
                    value = float(value)
                elif not value.isnumeric() and self.controller.frames[ppf.PrePFrame].df_msv[col].dtype == 'object':
                    value = str(value)
                else:
                    tk.messagebox.showerror('Python Error', "Please enter a value of the correct type.")
                    return
                self.controller.frames[ppf.PrePFrame].df_msv[col].fillna(value, inplace=True)
                self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].df_msv)
                tk.messagebox.showinfo('Info', 'Null values replaced with value in MV Dataframe')
            else:
                tk.messagebox.showerror('Python Error', "No null values in the column.")
                return

class ToplevelWindow(ctk.CTkToplevel):
    
    def __init__(self,txt):
        """
        A custom top-level window for displaying missing values.

        Args:
            txt (str): The text to be displayed in the window.

        Attributes:
            txt (str): The text to be displayed in the window.
            scrollable_frame (ctk.CTkScrollableFrame): The scrollable frame widget.
            missVals_text (ctk.CTkLabel): The label widget for displaying the missing values text.
        """
        ctk.CTkToplevel.__init__(self)
        self.title("ML Toolkit - Missing Values")
        self.geometry("500x400")
        self.resizable(False, False)
        self.iconbitmap(os.path.join("images","ML-icon.ico"))
        
        self.txt = txt

        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Missing Values")
        self.scrollable_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)
        self.scrollable_frame.grid_columnconfigure((0,1,2), weight=1)
        self.missVals_text = ctk.CTkLabel(master=self.scrollable_frame, font=('Arial',15), text=txt)
        self.missVals_text.grid(row=0, column=1, sticky="nsew")
        