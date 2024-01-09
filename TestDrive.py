import tkinter as tk
import customtkinter as ctk
import customMenu
import os
import ctypes
import preprocessing.ppframe as ppf
import modeling.models_frame as mf
import visualization.vizualization_frame as vsf
import import_frame as imf

ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
            

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        self.title("ML Toolkit")
        self.geometry(f"{1300}x{720}")
        self.iconbitmap(os.path.join("images","ML-icon.ico"))
        self.myappid = 'heh' # arbitrary string
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
        Model_menu.add_command(label="RandomForestClassifier")
        Model_menu.add_command(label="KNeighborsClassifier")
        Model_menu.add_command(label="SVM")
        Model_menu.add_command(label="Naive Bayes")
        Model_menu.add_command(label="Linear Regression")
        
        Viz_menu = menu.menu_bar(text="Visualization", tearoff=0,)
        Viz_menu.add_command(label="Seaborn",command=lambda:self.show_frame("sns",vsf.visulizeFrame))
        Viz_menu.add_command(label="Matplotlib",command=lambda:self.show_frame("mpl",vsf.visulizeFrame))
        
        container = ctk.CTkFrame(self, width=self.winfo_width(), height=self.winfo_height())
        self.resizable(False, False)
        container.configure(fg_color="#101010")
        container.pack(side="top", expand=True, fill="both")

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        for F in (imf.StartFrame, ppf.PrePFrame, mf.ModelsFrame,vsf.visulizeFrame):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_main_frame(imf.StartFrame)
    
    def show_main_frame(self, cont):
        current_frame = self.frames[cont]
        current_frame.configure(fg_color="#101010")
        current_frame.tkraise()


    def show_frame(self, frame, main):
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