import tkinter as tk
import customtkinter as ctk
import pandas as pd
import ppframe as ppf
import io
import sys

class MissingValsFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent,fg_color='transparent',corner_radius=20)
        
        pd.set_option('display.max_rows', None)  # Set option to display all rows
        
        self.separator = tk.ttk.Separator(self, orient='vertical')
        self.separator.place(relx=0.5, rely=0.5, relheight=0.9, bordermode="outside")
        
        self.import_file_button = ctk.CTkButton(master=self,text='Import...',width=200,height=45,command=lambda:self.controller.frames[ppf.PrePFrame].getFile())
        self.import_file_button.configure(fg_color="#200E3A")
        self.import_file_button.place(anchor="center",relx=0.92, rely=0.12)
        
        self.showEntireData_button = ctk.CTkButton(master=self,text='Load Entire Dataset',width=200,height=45,command=lambda:self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].df))
        self.showEntireData_button.configure(fg_color="#200E3A")
        self.showEntireData_button.place(anchor="center",relx=0.92, rely=0.27)
        
        self.loadMissValsDF_button = ctk.CTkButton(master=self,text='Load missing values Dataframe',width=200,height=45,command=lambda:self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].df_msv))
        self.loadMissValsDF_button.configure(fg_color="#200E3A")
        self.loadMissValsDF_button.place(anchor="center",relx=0.92, rely=0.42)
        
        self.CountMissVals_button = ctk.CTkButton(master=self,text='Count missing values',width=200,height=45,command=lambda:self.printMissingVals())
        self.CountMissVals_button.configure(fg_color="#200E3A")
        self.CountMissVals_button.place(anchor="center",relx=0.92, rely=0.57)
        
        self.SaveChanges_button = ctk.CTkButton(master=self,text='Save changes to Dataframe',width=200,height=45,command=lambda:self.saveChanges())
        self.SaveChanges_button.configure(fg_color="#200E3A")
        self.SaveChanges_button.place(anchor="center",relx=0.92, rely=0.72)
        
        self.printDFInfo_button = ctk.CTkButton(master=self,text='Show Dataframe info',width=200,height=45,command=lambda:self.printDFInfo())
        self.printDFInfo_button.configure(fg_color="#200E3A")
        self.printDFInfo_button.place(anchor="center",relx=0.92, rely=0.87)
        
        self.toplevel_window = None
        
    def printMissingVals(self):
        if self.controller.frames[ppf.PrePFrame].df is not None:
            MissVals = str(self.controller.frames[ppf.PrePFrame].df.isnull().sum())
            if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
                self.toplevel_window = ToplevelWindow(MissVals)  # create window if its None or destroyed
            else:
                self.toplevel_window.focus()  # if window exists focus it
        
    def saveChanges(self):
        if self.controller.frames[ppf.PrePFrame].df_msv is not None:
            self.controller.frames[ppf.PrePFrame].df = self.controller.frames[ppf.PrePFrame].df_msv
            tk.messagebox.showinfo('Info', 'Changes saved to Dataframe')
            
    def printDFInfo(self):
        if self.controller.frames[ppf.PrePFrame].df is not None:
            # Redirect the standard output to a StringIO object
            output = io.StringIO()
            sys.stdout = output

            # Call the df.info() method
            self.controller.frames[ppf.PrePFrame].df.info()

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

class ToplevelWindow(ctk.CTkToplevel):
    def __init__(self,txt):
        ctk.CTkToplevel.__init__(self)
        self.geometry("500x400")
        self.resizable(False, False)
        self.txt = txt

        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Missing Values")
        self.scrollable_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)
        self.scrollable_frame.grid_columnconfigure((0,1,2), weight=1)
        self.missVals_text = ctk.CTkLabel(master=self.scrollable_frame, font=('Arial',15), text=txt)
        self.missVals_text.grid(row=0, column=1, sticky="nsew")
        