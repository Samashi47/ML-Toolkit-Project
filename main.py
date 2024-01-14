"""
This script represents the main application for the ML Toolkit project.
It imports necessary modules and defines the main application class.
The class creates a GUI window and sets up the menu bar and frames for different functionalities.
"""

import platform
import tkinter as tk
import customtkinter as ctk
import customMenu
import os
import ctypes
import preprocessing.ppframe as ppf
import modeling.models_frame as mf
import visualization.vizualization_frame as vsf
import import_frame as imf
import docs as dcs

ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
            

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        """
        Initializes the main application class.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        ctk.CTk.__init__(self, *args, **kwargs)
        self.title("ML Toolkit")
        self.geometry(f"{1300}x{720}")
        self.iconbitmap(os.path.join("images","ML-icon.ico"))
        self.myappid = 'heh' # arbitrary string
        if platform.system() == "Windows":
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(self.myappid)
        menu = customMenu.Menu(self)

        file_menu = menu.menu_bar(text="File", tearoff=0)
        file_menu.add_command(label="Open",command=lambda:self.frames[ppf.PrePFrame].getFile())
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        
        PreP_menu = menu.menu_bar(text="Preprocessing", tearoff=0,)
        PreP_menu.add_command(label="Train Test Split",command=lambda:self.show_frame("train_test_split",ppf.PrePFrame))
        PreP_menu.add_command(label="Missing Values Handler",command=lambda:self.show_frame("misv",ppf.PrePFrame))
        PreP_menu.add_command(label="Normalization & Standardization",command=lambda:self.show_frame("norm_sc",ppf.PrePFrame))
        PreP_menu.add_command(label="One-Hot Encoding",command=lambda:self.show_frame("ohe",ppf.PrePFrame))
        PreP_menu.add_command(label="Label Encoding",command=lambda:self.show_frame("le",ppf.PrePFrame))
        PreP_menu.add_separator()
        PreP_menu.add_command(label="PCA",command=lambda:self.show_frame("PCA",ppf.PrePFrame))
        PreP_menu.add_command(label='CondensedNearestNeighbour',command=lambda:self.show_frame("cnn",ppf.PrePFrame))
        PreP_menu.add_command(label='SVMSMOTE',command=lambda:self.show_frame("svmsmote",ppf.PrePFrame))
        
        Model_menu = menu.menu_bar(text="Modeling", tearoff=0,)
        Model_menu.add_command(label="DecisionTreeClassifier",command=lambda:self.show_frame("dt",mf.ModelsFrame))
        Model_menu.add_command(label="RandomForestClassifier",command=lambda:self.show_frame("rf",mf.ModelsFrame))
        Model_menu.add_command(label="KNNClassifier",command=lambda:self.show_frame("knn",mf.ModelsFrame))
        Model_menu.add_command(label="SVM",command=lambda:self.show_frame("svm",mf.ModelsFrame))
        Model_menu.add_command(label="Naive Bayes",command=lambda:self.show_frame("nb",mf.ModelsFrame))
        Model_menu.add_command(label="Logistic Regression",command=lambda:self.show_frame("lr",mf.ModelsFrame))
        
        Viz_menu = menu.menu_bar(text="Visualization", tearoff=0,)
        Viz_menu.add_command(label="Seaborn",command=lambda:self.show_frame("sns",vsf.visulizeFrame))
        Viz_menu.add_command(label="Matplotlib",command=lambda:self.show_frame("mpl",vsf.visulizeFrame))
        
        about_menu = menu.menu_bar(text="About", tearoff=0)
        about_menu.add_command(label="Docs",command=lambda:self.show_main_frame(dcs.Docs))
        about_menu.add_command(label="About",command=lambda:tk.messagebox.showinfo("About", "ML Toolkit - V1.0\nCreated by:\n\n- Ahmed Samady | @Samashi47\n- Fahd Chibani | @Dhafahd\n- Marouan Daghmoumi | @Marouan19"))
        
        container = ctk.CTkFrame(self, width=self.winfo_width(), height=self.winfo_height())
        self.resizable(False, False)
        container.configure(fg_color="#101010")
        container.pack(side="top", expand=True, fill="both")

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        for F in (imf.StartFrame, ppf.PrePFrame, mf.ModelsFrame, vsf.visulizeFrame, dcs.Docs):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_main_frame(imf.StartFrame)
    
    def show_main_frame(self, cont):
        """
        Shows the main frame.

        Args:
            cont: The frame to show.
        """
        current_frame = self.frames[cont]
        current_frame.configure(fg_color="#101010")
        current_frame.tkraise()


    def show_frame(self, frame, main):
        """
        Shows a specific frame.

        Args:
            frame: The frame to show.
            main: The main frame to show.
        """
        if self.frames[ppf.PrePFrame].df is None:
            tk.messagebox.showerror('Python Error', "Please import a file first.")
            return
        frames = {
            "train_test_split": self.frames[ppf.PrePFrame].train_test_split_frame,
            "svmsmote": self.frames[ppf.PrePFrame].smote_frame,
            "misv": self.frames[ppf.PrePFrame].msv_frame,
            "cnn": self.frames[ppf.PrePFrame].cnn_frame,
            "PCA": self.frames[ppf.PrePFrame].pca_frame,
            "norm_sc": self.frames[ppf.PrePFrame].norm_sc_frame,
            "ohe": self.frames[ppf.PrePFrame].ohe_frame,
            "le": self.frames[ppf.PrePFrame].le_frame,
            "dt": self.frames[mf.ModelsFrame].dt_frame,
            "rf": self.frames[mf.ModelsFrame].rf_frame,
            "knn": self.frames[mf.ModelsFrame].knn_frame,
            "svm": self.frames[mf.ModelsFrame].svm_frame,
            "nb": self.frames[mf.ModelsFrame].nb_frame,
            "lr": self.frames[mf.ModelsFrame].lr_frame,
            "sns": self.frames[vsf.visulizeFrame].seaborn_frame,
            "mpl": self.frames[vsf.visulizeFrame].matplotlib_frame
        }
        self.show_main_frame(main)
        frame_to_show = frames.get(frame)
        if frame_to_show is None:
            return  # Invalid frame parameter
        
        if main == ppf.PrePFrame:
            for f in frames.values():
                if f == frame_to_show:
                    f.place(relx=0.01, rely=0, relwidth=0.98, relheight=0.98, in_=self.frames[ppf.PrePFrame].TopFrame, bordermode="outside")
                else:
                    f.place_forget()
        elif main == vsf.visulizeFrame:
            for f in frames.values():
                if f == frame_to_show:
                    f.place(relx=0.01, rely=0, relwidth=0.98, relheight=0.98, in_=self.frames[vsf.visulizeFrame].TopFrame, bordermode="outside")
                else:
                    f.place_forget()
        else:
            for f in frames.values():
                if f == frame_to_show:
                    f.place(relx=0.01, rely=0, relwidth=0.98, relheight=0.98, in_=self.frames[mf.ModelsFrame].TopFrame, bordermode="outside")
                else:
                    f.place_forget()
    
app = App()
app.protocol("WM_DELETE_WINDOW", app.quit)
app.mainloop()