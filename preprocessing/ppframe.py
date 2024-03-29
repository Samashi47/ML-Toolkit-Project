import tkinter as tk
import customtkinter as ctk
from tksheet import Sheet
import pandas as pd
import import_frame as imf
import preprocessing.subframes.ttsframe as ttsf
import preprocessing.subframes.svmsmote_frame as smf
import preprocessing.subframes.missingval_frame as msv
import preprocessing.subframes.cnn_frame as cnnf
import preprocessing.subframes.pca_frame as pcaf
import preprocessing.subframes.norm_sc_frame as nscf
import preprocessing.subframes.onehot_enc_frame as ohef
import preprocessing.subframes.labelenc_frame as lef
import visualization.vizualization_frame as vsf

class PrePFrame(ctk.CTkFrame):
    """
    A custom tkinter frame for preprocessing operations.

    Attributes:
    - controller: The controller object.
    - TopFrame: The top frame of the PrePFrame.
    - df_frame: The frame to hold the DataFrame.
    - df: The DataFrame object.
    - df_msv: The DataFrame object for missing value operations.
    - dfPCA: The DataFrame object for PCA operations.
    - dfNSC: The DataFrame object for normalization and scaling operations.
    - dfOHE: The DataFrame object for one-hot encoding operations.
    - dfLE: The DataFrame object for label encoding operations.
    - X_train: The training data.
    - X_test: The testing data.
    - y_train: The training labels.
    - y_test: The testing labels.
    - X_train_resampled: The resampled training data.
    - y_train_resampled: The resampled training labels.
    - dfCols: The list of column names in the DataFrame.
    - dfCols_num: The list of numerical column names in the DataFrame.
    - dfCols_cat: The list of categorical column names in the DataFrame.
    - train_test_split_frame: The TrainTestSplitFrame object.
    - smote_frame: The SVMSmoteFrame object.
    - msv_frame: The MissingValsFrame object.
    - cnn_frame: The CNNFrame object.
    - pca_frame: The PCAFrame object.
    - norm_sc_frame: The NormSCFrame object.
    - ohe_frame: The OneHotEncFrame object.
    - le_frame: The LabelEncFrame object.
    - succes_label: The success label widget.
    """

    def __init__(self, parent, controller):
        """
        Initializes a PrePFrame object.

        Parameters:
        - parent: The parent widget.
        - controller: The controller object.
        """
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

        self.df, self.df_msv, self.dfPCA, self.dfNSC, self.dfOHE, self.dfLE= None, None, None, None, None, None
        self.X_train, self.X_test, self.y_train, self.y_test = None, None, None, None
        self.X_train_resampled, self.y_train_resampled = None, None
        self.dfCols,self.dfCols_num,self.dfCols_cat = None, None, None
        
        self.train_test_split_frame = ttsf.TrainTestSplitFrame(self.TopFrame, controller)
        self.train_test_split_frame.place(relx=0.01, rely=0, relwidth=0.98, relheight=0.98, in_=self.TopFrame,bordermode="outside")
        
        self.smote_frame = smf.SVMSmoteFrame(self.TopFrame, controller)
        self.smote_frame.place(relx=0.01, rely=0, relwidth=0.98, relheight=0.98, in_=self.TopFrame,bordermode="outside")

        self.msv_frame = msv.MissingValsFrame(self.TopFrame, controller)
        self.msv_frame.place(relx=0.01, rely=0, relwidth=0.98, relheight=0.98, in_=self.TopFrame,bordermode="outside")
        
        self.cnn_frame = cnnf.CNNFrame(self.TopFrame, controller)
        self.cnn_frame.place(relx=0.01, rely=0, relwidth=0.98, relheight=0.98, in_=self.TopFrame,bordermode="outside")
        
        self.pca_frame = pcaf.PCAFrame(self.TopFrame, controller)
        self.pca_frame.place(relx=0.01, rely=0, relwidth=0.98, relheight=0.98, in_=self.TopFrame,bordermode="outside")
        
        self.norm_sc_frame = nscf.NormSCFrame(self.TopFrame, controller)
        self.norm_sc_frame.place(relx=0.01, rely=0, relwidth=0.98, relheight=0.98, in_=self.TopFrame,bordermode="outside")
        
        self.ohe_frame = ohef.OneHotEncFrame(self.TopFrame, controller)
        self.ohe_frame.place(relx=0.01, rely=0, relwidth=0.98, relheight=0.98, in_=self.TopFrame,bordermode="outside")
        
        self.le_frame = lef.LabelEncFrame(self.TopFrame, controller)
        self.le_frame.place(relx=0.01, rely=0, relwidth=0.98, relheight=0.98, in_=self.TopFrame,bordermode="outside")
        
        self.show_frame("train_test_split")
        
    def show_frame(self, frame):
        """
        Shows the specified frame and hides the other frames.

        Parameters:
        - frame: The name of the frame to show.
        """
        frames = {
            "train_test_split": self.train_test_split_frame,
            "svmsmote": self.smote_frame,
            "misv": self.msv_frame,
            "cnn": self.cnn_frame,
            "PCA": self.pca_frame,
            "norm_sc": self.norm_sc_frame,
            "ohe": self.ohe_frame,
            "le": self.le_frame
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
        """
        Opens a file dialog to select a file and imports it as a DataFrame.
        """
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
            self.controller.frames[imf.StartFrame].show_file_button.configure(state='normal')
            self.df_msv = self.df.copy()
            self.dfPCA = self.df.copy()
            self.dfNSC = self.df.copy()
            self.dfOHE = self.df.copy()
            self.dfLE = self.df.copy()
            self.showDataFrame(self.df)
            self.getColumns()
    
    def showDataFrame(self, data):
        """
        Displays the DataFrame using tksheet.

        Parameters:
        - data: The DataFrame to display.
        """
        if data is None:
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
    
    def getColumns(self):
        """
        Retrieves the column names from the DataFrame and updates the dropdown menus in the frames.
        """
        if self.df is not None:
            self.dfCols = self.df_msv.columns.tolist()
            self.dfCols_num = self.df_msv.select_dtypes(include='number').columns.tolist()
            self.dfCols_cat = self.df_msv.select_dtypes(include='object').columns.tolist()
            
            if len(self.dfCols_num) == 0:
                self.dfCols_num = ['No numerical columns']
                self.controller.frames[PrePFrame].msv_frame.replaceMean_button.configure(state='disabled')
                self.controller.frames[PrePFrame].msv_frame.replaceMean_optMenu.configure(state='disabled')
                self.controller.frames[PrePFrame].msv_frame.replaceMedian_button.configure(state='disabled')
                self.controller.frames[PrePFrame].msv_frame.replaceMedian_optMenu.configure(state='disabled')
            else:
                self.controller.frames[PrePFrame].msv_frame.replaceMean_button.configure(state='normal')
                self.controller.frames[PrePFrame].msv_frame.replaceMean_optMenu.configure(state='normal')
                self.controller.frames[PrePFrame].msv_frame.replaceMedian_button.configure(state='normal')
                self.controller.frames[PrePFrame].msv_frame.replaceMedian_optMenu.configure(state='normal')
                
            if len(self.dfCols_cat) == 0:
                self.dfCols_cat = ['No categorical columns']
                self.controller.frames[PrePFrame].msv_frame.replaceMode_button.configure(state='disabled')
                self.controller.frames[PrePFrame].msv_frame.replaceMode_optMenu.configure(state='disabled')
            else:
                self.controller.frames[PrePFrame].msv_frame.replaceMode_button.configure(state='normal')
                self.controller.frames[PrePFrame].msv_frame.replaceMode_optMenu.configure(state='normal')
                
            self.controller.frames[PrePFrame].train_test_split_frame.targetCol_optMenu.configure(values=self.dfCols)
            self.controller.frames[PrePFrame].train_test_split_frame.targetCol_optMenu.configure(variable=tk.StringVar(value=self.dfCols[-1]))
            
            self.controller.frames[PrePFrame].msv_frame.Cols_optMenu.configure(values=self.dfCols)
            self.controller.frames[PrePFrame].msv_frame.Cols_optMenu.configure(variable=tk.StringVar(value=self.dfCols[-1]))
            self.controller.frames[PrePFrame].msv_frame.replaceWithValue_optMenu.configure(values=self.dfCols)
            self.controller.frames[PrePFrame].msv_frame.replaceWithValue_optMenu.configure(variable=tk.StringVar(value=self.dfCols[-1]))
            self.controller.frames[PrePFrame].msv_frame.replaceMean_optMenu.configure(values=self.dfCols_num)
            self.controller.frames[PrePFrame].msv_frame.replaceMean_optMenu.configure(variable=tk.StringVar(value=self.dfCols_num[-1]))
            self.controller.frames[PrePFrame].msv_frame.replaceMedian_optMenu.configure(values=self.dfCols_num)
            self.controller.frames[PrePFrame].msv_frame.replaceMedian_optMenu.configure(variable=tk.StringVar(value=self.dfCols_num[-1]))
            self.controller.frames[PrePFrame].msv_frame.replaceMode_optMenu.configure(values=self.dfCols_cat)
            self.controller.frames[PrePFrame].msv_frame.replaceMode_optMenu.configure(variable=tk.StringVar(value=self.dfCols_cat[-1]))
            
            self.controller.frames[PrePFrame].pca_frame.Target_optMenu.configure(values=self.dfCols)
            self.controller.frames[PrePFrame].pca_frame.Target_optMenu.configure(variable=tk.StringVar(value=self.dfCols[-1]))
            
            self.controller.frames[PrePFrame].norm_sc_frame.nCols_optMenu.configure(values=self.dfNSC.columns.tolist())
            self.controller.frames[PrePFrame].norm_sc_frame.nCols_optMenu.configure(variable=tk.StringVar(value=self.dfNSC.columns.tolist()[-1]))
            self.controller.frames[PrePFrame].norm_sc_frame.scCols_optMenu.configure(values=self.dfNSC.columns.tolist())
            self.controller.frames[PrePFrame].norm_sc_frame.scCols_optMenu.configure(variable=tk.StringVar(value=self.dfNSC.columns.tolist()[-1]))
            self.controller.frames[PrePFrame].norm_sc_frame.mmCols_optMenu.configure(values=self.dfNSC.columns.tolist())
            self.controller.frames[PrePFrame].norm_sc_frame.mmCols_optMenu.configure(variable=tk.StringVar(value=self.dfNSC.columns.tolist()[-1]))
            self.controller.frames[PrePFrame].norm_sc_frame.mabsCols_optMenu.configure(values=self.dfNSC.columns.tolist())
            self.controller.frames[PrePFrame].norm_sc_frame.mabsCols_optMenu.configure(variable=tk.StringVar(value=self.dfNSC.columns.tolist()[-1]))
            
            self.controller.frames[PrePFrame].ohe_frame.target_optMenu.configure(values=self.dfOHE.columns.tolist())
            self.controller.frames[PrePFrame].ohe_frame.target_optMenu.configure(variable=tk.StringVar(value=self.dfOHE.columns.tolist()[-1]))           
            
            self.controller.frames[PrePFrame].le_frame.target_optMenu.configure(values=self.dfLE.columns.tolist())
            self.controller.frames[PrePFrame].le_frame.target_optMenu.configure(variable=tk.StringVar(value=self.dfLE.columns.tolist()[-1]))
            
            self.controller.frames[vsf.visulizeFrame].matplotlib_frame.x_dropdown.configure(values=self.dfCols)
            self.controller.frames[vsf.visulizeFrame].matplotlib_frame.x_dropdown.configure(variable=tk.StringVar(value=self.dfCols[-1]))
            self.controller.frames[vsf.visulizeFrame].matplotlib_frame.y_dropdown.configure(variable=tk.StringVar(value=self.dfCols[-1]))
            self.controller.frames[vsf.visulizeFrame].matplotlib_frame.y_dropdown.configure(values=self.dfCols)
            self.controller.frames[vsf.visulizeFrame].matplotlib_frame.z_dropdown.configure(values=self.dfCols)
            self.controller.frames[vsf.visulizeFrame].matplotlib_frame.z_dropdown.configure(variable=tk.StringVar(value=self.dfCols[-1]))
            
            self.controller.frames[vsf.visulizeFrame].seaborn_frame.x_dropdown.configure(values=self.dfCols)
            self.controller.frames[vsf.visulizeFrame].seaborn_frame.x_dropdown.configure(variable=tk.StringVar(value=self.dfCols[-1]))
            self.controller.frames[vsf.visulizeFrame].seaborn_frame.y_dropdown.configure(values=self.dfCols)
            self.controller.frames[vsf.visulizeFrame].seaborn_frame.y_dropdown.configure(variable=tk.StringVar(value=self.dfCols[-1]))
        else:
            return