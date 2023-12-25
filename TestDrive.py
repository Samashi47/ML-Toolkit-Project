import tkinter as tk
import tkinter.messagebox
from tkinter.filedialog import askopenfilename
import customtkinter as ctk
import customMenu
import pandas as pd
from tksheet import Sheet

ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class StartFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        # configure grid layout (4x4)
        
        global app
        
        ctk.CTkFrame.__init__(self, parent)
        self.import_frame = ctk.CTkFrame(self, width=self.winfo_width(), height=self.winfo_height(), corner_radius=0, fg_color="#200E3A")
        # import entry
        self.import_entry = ctk.CTkEntry(self,width=800,height=30, textvariable= self.retPath())
        self.import_entry.configure(fg_color="#200E3A")
        self.import_entry.place(relx=0.5, rely=0.4, anchor="center")
        #import button
        self.import_button = ctk.CTkButton(self,width=400,height=50, text="Import File",command=lambda:self.getCSV_wrapper())
        self.import_button.configure(fg_color="#200E3A")
        self.import_button.place(relx=0.5, rely=0.5, anchor="center")
        # Show File button
        self.show_file_button = ctk.CTkButton(self,width=400,height=50, text="Show File",command=lambda:controller.show_frame(PrePFrame))
        self.show_file_button.configure(fg_color="#200E3A")
        self.show_file_button.place(relx=0.5, rely=0.7, anchor="center")
        
        
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

    def getCSV_wrapper(self):
        global app
        app.frames[PrePFrame].getCSV()
    
    def show_wrapper(self):
        global app
        app.frames[PrePFrame].show()
    
    def retPath(self):
        global app
        return app.frames[PrePFrame].path.get()

class PrePFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.path = str()
        self.data_frame = ctk.CTkFrame(self, width=self.winfo_width(), height=self.winfo_height(), corner_radius=0, fg_color="#200E3A")
        
        label_1 = ctk.CTkLabel(self)
        label_1.configure(font=('Arial',12), justify='center', text='PREDIKSI IHSG BBCA.JK')
        label_1.pack(side='top')
        button_1 = ctk.CTkButton(self)
        button_1.configure(text='Import File', command=lambda: self.getCSV())
        button_1.place(relx='0.14', rely='0.66', anchor="center")
        button_2 = ctk.CTkButton(self)
        button_2.configure(text='Show File', command=lambda: self.show())
        button_2.place(relx='0.55', rely='0.66', anchor="center")

        # Frame to hold DataFrame
        self.df_frame = ctk.CTkFrame(self,height=200, width=200)
        self.df_frame.pack(side='top', pady=10)

        self.df = None  # Initialize df as an instance variable

    def getCSV(self):
        global app
        self.path = tk.filedialog.askopenfilename()
        if self.path.endswith('.csv'):
            self.df = pd.read_csv(self.path)
        elif self.path.endswith(('.xls', '.xlsx')):
            self.df = pd.read_excel(self.path)
        else:
            print("Unsupported file format. Please select a CSV or Excel file.")
        if str(self.path.get()) != "":
            self.succes_label = ctk.CTkLabel(app.frames[StartFrame],width=400,height=50, text="File imported successfully!")
            self.succes_label.place(relx=0.5, rely=0.6, anchor="center")


    def show(self):
        if self.df is None:
            print("Please import a file first.")
            return

        # Clear previous DataFrame display
        for widget in self.df_frame.winfo_children():
            widget.destroy()

        # Display DataFrame using tksheet
        sheet = Sheet(self.df_frame)
        sheet.enable_bindings()
        sheet.grid(row=0, column=0, sticky="nswe")

        # Insert data
        sheet.set_sheet_data(self.df.values.tolist())
    


class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        
        self.title("ML Toolkit")
        
        self.geometry(f"{1100}x{580}")
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)
        # Menu Bar
        menu = customMenu.Menu(self)

        file_menu = menu.menu_bar(text="File", tearoff=0)
        file_menu.add_command(label="Open",command=lambda:self.frames[StartFrame].browser())
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


app = App()
app.mainloop()
