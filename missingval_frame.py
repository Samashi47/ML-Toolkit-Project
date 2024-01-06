import tkinter as tk
import customtkinter as ctk
import pandas as pd
import sys
import os
import io
import ppframe as ppf

class MissingValsFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent,fg_color='transparent',corner_radius=20)
        
        pd.set_option('display.max_rows', None)  # Set option to display all rows
        
        # Missing Values Frame
        
        self.removeCol_label = ctk.CTkLabel(self,font=('Arial',17), text="Remove Columns : ")
        self.removeCol_label.place(anchor="center",relx=0.11, rely=0.16)
        self.Cols_optMenu = ctk.CTkOptionMenu(self, width=190, height=30,values=[],dynamic_resizing=True)
        self.Cols_optMenu.configure(fg_color="#200E3A")
        self.Cols_optMenu.place(relx=0.11, rely=0.30, anchor="center")
        self.removeCol_button = ctk.CTkButton(master=self,text='Remove',width=190,height=30,command=lambda:self.removeCol(self.Cols_optMenu.get()))
        self.removeCol_button.configure(fg_color="#200E3A")
        self.removeCol_button.place(anchor="center",relx=0.11, rely=0.44)
        
        self.seph = tk.ttk.Separator(self, orient='horizontal', style='TSeparator')
        self.seph.place(relx=0.01, rely=0.55, width=1260, bordermode="outside")
        
        self.sep1v = tk.ttk.Separator(self, orient='vertical')
        self.sep1v.place(relx=0.25, rely=0.1, height=400, bordermode="outside")
        
        self.removeRow_label = ctk.CTkLabel(self,font=('Arial',17), text="Remove Rows :")
        self.removeRow_label.place(anchor="center",relx=0.11, rely=0.64)
        self.removeRow_button = ctk.CTkButton(master=self,text='Remove rows w/ Nulls',width=190,height=30,command=lambda:self.removeNArows())
        self.removeRow_button.configure(fg_color="#200E3A")
        self.removeRow_button.place(anchor="center",relx=0.11, rely=0.78)

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
        self.replaceWithValue_entry = ctk.CTkEntry(self, width=145, height=30)
        self.replaceWithValue_entry.configure(fg_color="#200E3A")
        self.replaceWithValue_entry.place(relx=0.76, rely=0.78, anchor="center")
        self.replaceWithValue_button = ctk.CTkButton(master=self,text='Replace',width=190,height=30,command=lambda:self.replaceWithValue(self.replaceWithValue_optMenu.get(),self.replaceWithValue_entry.get()))
        self.replaceWithValue_button.configure(fg_color="#200E3A")
        self.replaceWithValue_button.place(anchor="center",relx=0.7, rely=0.92)
               
        self.import_file_button = ctk.CTkButton(master=self,text='Import...',width=200,height=45,command=lambda:self.controller.frames[ppf.PrePFrame].getFile())
        self.import_file_button.configure(fg_color="#200E3A")
        self.import_file_button.place(anchor="center",relx=0.92, rely=0.12)
        
        self.showEntireData_button = ctk.CTkButton(master=self,text='Load Original Dataset',width=200,height=45,command=lambda:self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].df))
        self.showEntireData_button.configure(fg_color="#200E3A")
        self.showEntireData_button.place(anchor="center",relx=0.92, rely=0.27)
        
        self.loadMissValsDF_button = ctk.CTkButton(master=self,text='Load missing values Dataframe',width=200,height=45,command=lambda:self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].df_msv))
        self.loadMissValsDF_button.configure(fg_color="#200E3A")
        self.loadMissValsDF_button.place(anchor="center",relx=0.92, rely=0.42)
        
        self.CountMissVals_button = ctk.CTkButton(master=self,text='Count missing values',width=200,height=45,command=lambda:self.printMissingVals())
        self.CountMissVals_button.configure(fg_color="#200E3A")
        self.CountMissVals_button.place(anchor="center",relx=0.92, rely=0.57)
        
        self.printDFInfo_button = ctk.CTkButton(master=self,text='Show Dataframe info',width=200,height=45,command=lambda:self.printDFInfo())
        self.printDFInfo_button.configure(fg_color="#200E3A")
        self.printDFInfo_button.place(anchor="center",relx=0.92, rely=0.72)
        
        self.SaveChanges_button = ctk.CTkButton(master=self,text='Save changes to Dataframe',width=200,height=45,command=lambda:self.saveChanges())
        self.SaveChanges_button.configure(fg_color="#200E3A")
        self.SaveChanges_button.place(anchor="center",relx=0.92, rely=0.87)
        
        self.toplevel_window = None
        
    def printMissingVals(self):
        if self.controller.frames[ppf.PrePFrame].df_msv is not None:
            MissVals = str(self.controller.frames[ppf.PrePFrame].df_msv.isnull().sum())
            if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
                self.toplevel_window = ToplevelWindow(MissVals)  # create window if its None or destroyed
            else:
                self.toplevel_window.focus()  # if window exists focus it
        
    def saveChanges(self):
        if self.controller.frames[ppf.PrePFrame].df_msv is not None:
            self.controller.frames[ppf.PrePFrame].df = self.controller.frames[ppf.PrePFrame].df_msv
            tk.messagebox.showinfo('Info', 'Changes saved to Dataframe')
            
    def printDFInfo(self):
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
        if self.controller.frames[ppf.PrePFrame].df_msv is not None:
            if col in self.controller.frames[ppf.PrePFrame].dfCols:
                self.controller.frames[ppf.PrePFrame].df_msv.drop(col, axis=1, inplace=True)
                self.controller.frames[ppf.PrePFrame].dfCols = self.controller.frames[ppf.PrePFrame].df_msv.columns.tolist()
                self.controller.frames[ppf.PrePFrame].dfCols_num = self.controller.frames[ppf.PrePFrame].df_msv.select_dtypes(include='number').columns.tolist()
                self.controller.frames[ppf.PrePFrame].dfCols_cat = self.controller.frames[ppf.PrePFrame].df_msv.select_dtypes(include='object').columns.tolist()
                self.Cols_optMenu.configure(values=list(self.controller.frames[ppf.PrePFrame].dfCols))
                self.replaceMean_optMenu.configure(values=list(self.controller.frames[ppf.PrePFrame].dfCols_num))
                self.Cols_optMenu.configure(variable=tk.StringVar(value=self.controller.frames[ppf.PrePFrame].dfCols[-1]))
                self.replaceMean_optMenu.configure(variable=tk.StringVar(value=self.controller.frames[ppf.PrePFrame].dfCols_num[-1]))
                self.replaceMedian_optMenu.configure(values=list(self.controller.frames[ppf.PrePFrame].dfCols_num))
                self.replaceMedian_optMenu.configure(variable=tk.StringVar(value=self.controller.frames[ppf.PrePFrame].dfCols_num[-1]))
                self.replaceMode_optMenu.configure(values=list(self.controller.frames[ppf.PrePFrame].dfCols_cat))
                self.replaceMode_optMenu.configure(variable=tk.StringVar(value=self.controller.frames[ppf.PrePFrame].dfCols_cat[-1]))
                self.replaceWithValue_optMenu.configure(values=list(self.controller.frames[ppf.PrePFrame].dfCols))
                self.replaceWithValue_optMenu.configure(variable=tk.StringVar(value=self.controller.frames[ppf.PrePFrame].dfCols[-1]))
                tk.messagebox.showinfo('Info', 'Column removed from MV Dataframe')
            else:
                tk.messagebox.showerror('Python Error', "Please select a column from the list.")
                return
            
    def removeNArows(self):
        if self.controller.frames[ppf.PrePFrame].df_msv is not None:
            if self.controller.frames[ppf.PrePFrame].df_msv.isnull().values.any():
                self.controller.frames[ppf.PrePFrame].df_msv.dropna(inplace=True)
                tk.messagebox.showinfo('Info', 'Rows with null values removed from MV Dataframe')
            else:
                tk.messagebox.showerror('Python Error', "No null values in the Dataframe.")
                return
            
    def replaceWithMean(self,col):
        if self.controller.frames[ppf.PrePFrame].df_msv is not None:
            if self.controller.frames[ppf.PrePFrame].df_msv[col].isnull().values.any():
                self.controller.frames[ppf.PrePFrame].df_msv[col].fillna(self.controller.frames[ppf.PrePFrame].df_msv[col].mean(), inplace=True)
                tk.messagebox.showinfo('Info', 'Null values replaced with mean in MV Dataframe')
            else:
                tk.messagebox.showerror('Python Error', "No null values in the column.")
                return
            
    def replaceWithMedian(self,col):
        if self.controller.frames[ppf.PrePFrame].df_msv is not None:
            if self.controller.frames[ppf.PrePFrame].df_msv[col].isnull().values.any():
                self.controller.frames[ppf.PrePFrame].df_msv[col].fillna(self.controller.frames[ppf.PrePFrame].df_msv[col].median(), inplace=True)
                tk.messagebox.showinfo('Info', 'Null values replaced with median in MV Dataframe')
            else:
                tk.messagebox.showerror('Python Error', "No null values in the column.")
                return
            
    def replaceWithMode(self,col):
        if self.controller.frames[ppf.PrePFrame].df_msv is not None:
            if self.controller.frames[ppf.PrePFrame].df_msv[col].isnull().values.any():
                self.controller.frames[ppf.PrePFrame].df_msv[col].fillna(self.controller.frames[ppf.PrePFrame].df_msv[col].mode()[0], inplace=True)
                tk.messagebox.showinfo('Info', 'Null values replaced with mode in MV Dataframe')
            else:
                tk.messagebox.showerror('Python Error', "No null values in the column.")
                return
            
    def replaceWithValue(self, col, value):
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
                tk.messagebox.showinfo('Info', 'Null values replaced with value in MV Dataframe')
            else:
                tk.messagebox.showerror('Python Error', "No null values in the column.")
                return

class ToplevelWindow(ctk.CTkToplevel):
    def __init__(self,txt):
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
        