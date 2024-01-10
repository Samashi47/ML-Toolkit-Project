import tkinter as tk
import tkinter.messagebox
from tkinter.filedialog import askopenfilename
import customtkinter as ctk
import customMenu

ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class StartFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        # configure grid layout (4x4)
        
        ctk.CTkFrame.__init__(self, parent)
        self.import_frame = ctk.CTkFrame(self, width=self.winfo_width(), height=self.winfo_height(), corner_radius=0, fg_color="#200E3A")
        self.path = tk.StringVar()
        self.import_entry = ctk.CTkEntry(self,width=800,height=30, textvariable=self.path)
        self.import_entry.configure(fg_color="#200E3A")
        self.import_entry.place(relx=0.5, rely=0.4, anchor="center")
        
        self.import_button = ctk.CTkButton(self,width=400,height=50, text="Import File",command=lambda:self.browser())
        self.import_button.configure(fg_color="#200E3A")
        self.import_button.place(relx=0.5, rely=0.5, anchor="center")
        print(str(self.path.get()))

    def browser(self):
        name = askopenfilename()
        if name:
            self.path.set(name)
        if str(self.path.get()) != "":
            self.succes_label = ctk.CTkLabel(self,width=400,height=50, text="File imported successfully!")
            self.succes_label.place(relx=0.5, rely=0.6, anchor="center")
               
    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)


class PrePFrame(ctk.CTkFrame):
    #class PCAFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        # create checkbox and switch frame
        # self.checkbox_slider_frame = ctk.CTkFrame(self, width=1100, height=50, corner_radius=0, fg_color="#200E3A")
        # self.checkbox_slider_frame.grid(row=1, column=3, sticky="nsew")
        # self.checkbox_1 = ctk.CTkCheckBox(master=self.checkbox_slider_frame)
        # self.checkbox_1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")
        # self.checkbox_2 = ctk.CTkCheckBox(master=self.checkbox_slider_frame)
        # self.checkbox_2.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="n")
        # self.checkbox_3 = ctk.CTkCheckBox(master=self.checkbox_slider_frame)
        # self.checkbox_3.grid(row=3, column=0, pady=20, padx=20, sticky="n")
    


class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        
        global app
        self.title("ML Toolkit")
        
        self.geometry(f"{1100}x{580}")
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)
        # Menu Bar
        menu = customMenu.Menu(self)

        file_menu = menu.menu_bar(text="File", tearoff=0)
        file_menu.add_command(label="Open",command=lambda:self.browser())
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        
        PreP_menu = menu.menu_bar(text="Preprocessing", tearoff=0)
        PreP_menu.add_command(label="PCA")
        PreP_menu.add_separator()
        
        # add a undersampling submenu
        PreP_submenu = customMenu.Menu(PreP_menu)
        undersampling_sub_menu = PreP_submenu.menu_bar(text="Undersampling", tearoff=0)
        undersampling_sub_menu.add_command(label='ClusterCentroids')
        undersampling_sub_menu.add_command(label='CondensedNearestNeighbour')
        undersampling_sub_menu.add_command(label='EditedNearestNeighbours')
        undersampling_sub_menu.add_command(label='TomekLinks')
        undersampling_sub_menu.add_command(label='RepeatedEditedNearestNeighbours')
        
        # add a oversampling submenu
        oversampling_sub_menu = PreP_submenu.menu_bar(text="Oversampling", tearoff=0)
        oversampling_sub_menu.add_command(label='RandomOverSampler',command=lambda: print(app.frames[StartFrame].path.get()))
        oversampling_sub_menu.add_command(label='SMOTE')
        oversampling_sub_menu.add_command(label='SMOTENC')
        oversampling_sub_menu.add_command(label='SMOTEN')
        oversampling_sub_menu.add_command(label='SVMSMOTE')
        oversampling_sub_menu.add_command(label='BorderlineSMOTE')
        oversampling_sub_menu.add_command(label='KmeansSMOTE')
        oversampling_sub_menu.add_command(label='ADA-SYN')
        
        PreP_menu.add_cascade(label="Undersampling", menu=undersampling_sub_menu)
        PreP_menu.add_cascade(label="Oversampling", menu=oversampling_sub_menu)
        PreP_menu.add_separator()
        
        container = ctk.CTkFrame(self, width=self.winfo_width(), height=self.winfo_height())
        container.configure(fg_color="#101010")
        container.pack(side="top", expand=True, fill="both")

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}

        for F in (StartFrame, PrePFrame):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartFrame)
    
    def show_frame(self, cont, val=None):
        # if val == "PCA":
        # current_frame = self.frames[cont].PCAFrame
        current_frame = self.frames[cont]
        current_frame.configure(fg_color="#101010")
        current_frame.tkraise()
        print(val)


if __name__ == "__main__":
    app = App()
    app.mainloop()
