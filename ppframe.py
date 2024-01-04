import tkinter as tk
import customtkinter as ctk
import pandas as pd
from tksheet import Sheet
import ttsframe as ttsf
import import_frame as imf
import svmsmote_frame as smf
import missingval_frame as msv
class PrePFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent)
        self.rowconfigure((0,1), weight=1)
        self.columnconfigure((0), weight=1)
        self.path = tk.StringVar()
        
        # Top Frame
        
        self.TopFrame = ctk.CTkFrame(self, width=self.winfo_width(), height=self.winfo_height()/2, corner_radius=20)
        self.TopFrame.grid(row=0,columnspan=4,padx=(10, 10), pady=(10, 10), sticky="nsew")

        # Frame to hold DataFrame
        self.df_frame = ctk.CTkFrame(self, width=self.winfo_width(), height=self.winfo_height()/2, corner_radius=20)
        self.df_frame.grid(row=1,columnspan=4,padx=(10, 10), pady=(0, 10), in_=self, sticky="nsew")
        self.df_frame.grid_propagate(False)  # Fix: Set grid_propagate to False

        self.df = None  # Initialize df as an instance variable
        self.df_msv = None
        self.X_train, self.X_test, self.y_train, self.y_test = None, None, None, None
        self.X_train_resampled, self.y_train_resampled = None, None
        self.train_test_split_frame = ttsf.TrainTestSplitFrame(self.TopFrame, controller)
        self.train_test_split_frame.place(relx=0.01, rely=0, relwidth=0.98, relheight=0.98, in_=self.TopFrame,bordermode="outside")
        
        self.smote_frame = smf.SVMSmoteFrame(self.TopFrame, controller)
        self.smote_frame.place(relx=0.01, rely=0, relwidth=0.98, relheight=0.98, in_=self.TopFrame,bordermode="outside")

        self.msv_frame = msv.MissingValsFrame(self.TopFrame, controller)
        self.msv_frame.place(relx=0.01, rely=0, relwidth=0.98, relheight=0.98, in_=self.TopFrame,bordermode="outside")
        
        self.show_frame("misv")
                
    def show_frame(self, frame):
        frames = {
            "train_test_split": self.train_test_split_frame,
            "svmsmote": self.smote_frame,
            "misv": self.msv_frame
        }

        frame_to_show = frames.get(frame)
        if frame_to_show is None:
            return  # Invalid frame parameter

        for f in frames.values():
            if f == frame_to_show:
                f.place(relx=0.01, rely=0, relwidth=0.98, relheight=0.98, in_=self.TopFrame, bordermode="outside")
            else:
                f.place_forget()
                
    def getFile(self):
        self.path = tk.filedialog.askopenfilename()
        if self.path.endswith('.csv') or self.path.endswith('.data'):
            self.df = pd.read_csv(self.path)
        elif self.path.endswith(('.xls', '.xlsx')):
            self.df = pd.read_excel(self.path)
        elif self.path.endswith(('.json')):
            self.df = pd.read_json(self.path)
        elif self.path.endswith(('.xml')):
            self.df = pd.read_xml(self.path)
        else:
            tk.messagebox.showerror('Python Error', "Unsupported file format. Please select a CSV, Excel, JSON or XML file.")
            return
        if str(self.path) != "":
            self.succes_label = ctk.CTkLabel(self.controller.frames[imf.StartFrame],font=('Arial',18),width=400,height=50, text="File imported successfully!")
            self.succes_label.place(relx=0.5, rely=0.7, anchor="center")
            self.controller.frames[imf.StartFrame].path.set(self.path)
            self.showDataFrame(self.df)
            
    
    def showDataFrame(self, data):
        
        if data is None or (isinstance(data, pd.DataFrame) and data.empty):
            tk.messagebox.showerror('Python Error', "Please import a file first.")
            return

        # Clear previous DataFrame display
        for widget in self.df_frame.winfo_children():
            widget.destroy()

        # Display DataFrame using tksheet
        if isinstance(data, pd.Series):
            data = data.to_frame()
            
        # Display DataFrame using tksheet
        sheet = Sheet(self.df_frame, width=self.winfo_width()-30, 
                      height=(self.winfo_height()/2)-30,
                      page_up_down_select_row=True, 
                      column_width=120, 
                      startup_select=(0,1,"rows"), 
                      headers=data.columns.tolist(), 
                      theme="dark blue",
                      row_index_width=50,
                      empty_horizontal=0,
                      empty_vertical=0)
        
        sheet.enable_bindings()
        sheet.grid(row=0, column=0, sticky="nsew", columnspan=4)  # Modified line

        # Insert data
        sheet.set_sheet_data(data.values.tolist())