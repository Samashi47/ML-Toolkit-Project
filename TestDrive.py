import tkinter as tk
import customtkinter as ctk
import customMenu
import ppframe as ppf
import import_frame as imf

ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
            

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        
        self.title("ML Toolkit")
        
        self.geometry(f"{1300}x{720}")
        # Menu Bar
        menu = customMenu.Menu(self)

        file_menu = menu.menu_bar(text="File", tearoff=0)
        file_menu.add_command(label="Open",command=lambda:self.frames[ppf.PrePFrame].getFile())
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        
        PreP_menu = menu.menu_bar(text="Preprocessing", tearoff=0)
        PreP_menu.add_command(label="Train Test Split",command=lambda:self.frames[ppf.PrePFrame].show_frame("train_test_split"))
        PreP_menu.add_command(label="Missing Values")
        PreP_menu.add_command(label="Normalization")
        PreP_menu.add_command(label="Standard Scaling")
        PreP_menu.add_command(label="One-Hot Encoding")
        PreP_menu.add_command(label="Label Encoding")
        PreP_menu.add_separator()
        PreP_menu.add_command(label="PCA")
        
        # add a undersampling submenu
        PreP_submenu = customMenu.Menu(PreP_menu)
        undersampling_sub_menu = PreP_submenu.menu_bar(text="Undersampling", tearoff=0)
        undersampling_sub_menu.add_command(label='ClusterCentroids')
        undersampling_sub_menu.add_command(label='CondensedNearestNeighbour')
        undersampling_sub_menu.add_command(label='EditedNearestNeighbours')
        
        # add a oversampling submenu
        oversampling_sub_menu = PreP_submenu.menu_bar(text="Oversampling", tearoff=0)
        oversampling_sub_menu.add_command(label='SMOTE',command=lambda:self.frames[ppf.PrePFrame].show_frame("smote"))
        oversampling_sub_menu.add_command(label='SVMSMOTE')
        oversampling_sub_menu.add_command(label='ADA-SYN')
        
        PreP_menu.add_cascade(label="Undersampling", menu=undersampling_sub_menu)
        PreP_menu.add_cascade(label="Oversampling", menu=oversampling_sub_menu)
        
        container = ctk.CTkFrame(self, width=self.winfo_width(), height=self.winfo_height())
        self.resizable(False, False)
        container.configure(fg_color="#101010")
        container.pack(side="top", expand=True, fill="both")

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        for F in (imf.StartFrame, ppf.PrePFrame):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(imf.StartFrame)
    
    def show_frame(self, cont):
        current_frame = self.frames[cont]
        current_frame.configure(fg_color="#101010")
        current_frame.tkraise()


app = App()
app.mainloop()