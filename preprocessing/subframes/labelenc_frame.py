import tkinter as tk
import customtkinter as ctk
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import preprocessing.ppframe as ppf


class LabelEncFrame(ctk.CTkFrame):
    """
    A custom tkinter frame for applying label encoding to a column in a dataframe.

    Attributes:
        controller (object): The controller object for managing the frames.
        LabelEnc_label (object): The label widget for displaying the title.
        target_label (object): The label widget for displaying the column to encode.
        target_optMenu (object): The option menu widget for selecting the column to encode.
        LE_button (object): The button widget for applying label encoding.
        import_file_button (object): The button widget for importing a file.
        showEntireData_button (object): The button widget for loading the original dataset.
        loadLEdf_button (object): The button widget for loading the label encoded dataframe.
        rollback_button (object): The button widget for rolling back changes.
        SaveChanges_button (object): The button widget for saving changes to the dataframe.
    """
    def __init__(self, parent, controller):
        """
        Initializes the LabelEncFrame.

        Args:
            parent (object): The parent widget.
            controller (object): The controller object for managing the frames.
        """
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent,fg_color='transparent',corner_radius=20)
        
        self.LabelEnc_label = ctk.CTkLabel(self,font=('Arial',30),text="Label Encoder: ")
        self.LabelEnc_label.place(anchor="center",relx=0.5, rely=0.08)
        
        self.target_label = ctk.CTkLabel(self,font=('Arial',17),text="Column to encode: ")
        self.target_label.place(anchor="center",relx=0.42, rely=0.5)
        self.target_optMenu = ctk.CTkOptionMenu(self, width=190, height=30,values=[],dynamic_resizing=True)
        self.target_optMenu.configure(fg_color="#200E3A")
        self.target_optMenu.place(relx=0.57, rely=0.51, anchor="center")
        
        self.LE_button = ctk.CTkButton(master=self, text='Apply Label Encoding', font=('Arial', 15), width=400, height=40,
                                          command=lambda:self.applyLE(self.target_optMenu.get()))
        self.LE_button.configure(fg_color="#200E3A")
        self.LE_button.place(anchor="center",relx=0.5, rely=0.9)
        
        self.import_file_button = ctk.CTkButton(master=self,text='Import...',width=200,height=45,command=lambda:self.controller.frames[ppf.PrePFrame].getFile())
        self.import_file_button.configure(fg_color="#200E3A")
        self.import_file_button.place(anchor="center",relx=0.92, rely=0.24)
        
        self.showEntireData_button = ctk.CTkButton(master=self,text='Load Original Dataset',width=200,height=45,command=lambda:self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].df))
        self.showEntireData_button.configure(fg_color="#200E3A")
        self.showEntireData_button.place(anchor="center",relx=0.92, rely=0.39)
        
        self.loadLEdf_button = ctk.CTkButton(master=self,text='Load LE Dataframe',width=200,height=45,command=lambda:self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].dfLE))
        self.loadLEdf_button.configure(fg_color="#200E3A")
        self.loadLEdf_button.place(anchor="center",relx=0.92, rely=0.54)
        
        self.rollback_button = ctk.CTkButton(master=self,text='Rollback',width=200,height=45,command=lambda:self.rollback())
        self.rollback_button.configure(fg_color="#200E3A")
        self.rollback_button.place(anchor="center",relx=0.92, rely=0.69)
        
        self.SaveChanges_button = ctk.CTkButton(master=self,text='Save changes to Dataframe',width=200,height=45,command=lambda:self.saveChanges())
        self.SaveChanges_button.configure(fg_color="#200E3A")
        self.SaveChanges_button.place(anchor="center",relx=0.92, rely=0.84)
        
    def applyLE(self,target):
        """
        Applies label encoding to the selected column in the label encoded dataframe.

        Args:
            target (str): The column to encode.
        """
        if self.controller.frames[ppf.PrePFrame].dfLE is None:
            tk.messagebox.showerror('Python Error', "Please import a file first.")
            return
        
        if self.controller.frames[ppf.PrePFrame].dfLE[target].dtype != 'object':
            tk.messagebox.showerror('Python Error', "Please select a column with dtype 'object'.")
            return
        
        self.controller.frames[ppf.PrePFrame].dfLE[target] = pd.DataFrame(LabelEncoder().fit_transform(self.controller.frames[ppf.PrePFrame].dfLE[target]))
        self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].dfLE)
        tk.messagebox.showinfo('Info', 'Label Encoding successful')
        
    
    def saveChanges(self):
        """
        Saves the changes made to the label encoded dataframe to the original dataframe.
        """
        if self.controller.frames[ppf.PrePFrame].dfLE is not None:
            self.controller.frames[ppf.PrePFrame].df = self.controller.frames[ppf.PrePFrame].dfLE.copy()
            self.controller.frames[ppf.PrePFrame].dfPCA = self.controller.frames[ppf.PrePFrame].df.copy()
            self.controller.frames[ppf.PrePFrame].dfNSC = self.controller.frames[ppf.PrePFrame].df.copy()
            self.controller.frames[ppf.PrePFrame].dfOHE = self.controller.frames[ppf.PrePFrame].df.copy()
            self.controller.frames[ppf.PrePFrame].df_msv = self.controller.frames[ppf.PrePFrame].df.copy()
            tk.messagebox.showinfo('Info', 'Changes saved to Dataframe, rollback not available.')
            
    def rollback(self):
        """
        Rolls back the changes made to the label encoded dataframe.
        """
        if self.controller.frames[ppf.PrePFrame].dfLE is not None and self.controller.frames[ppf.PrePFrame].df is not None:
            self.controller.frames[ppf.PrePFrame].dfLE = self.controller.frames[ppf.PrePFrame].df.copy()
            self.controller.frames[ppf.PrePFrame].showDataFrame(self.controller.frames[ppf.PrePFrame].dfLE)
            tk.messagebox.showinfo('Info', 'Rollback successful')