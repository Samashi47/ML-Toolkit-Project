import tkinter as tk
import customtkinter as ctk
import ppframe as ppf


class StartFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        # configure grid layout (4x4)
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent)
        self.path = tk.StringVar()
        self.import_frame = ctk.CTkFrame(self, width=self.winfo_width(), height=self.winfo_height(), corner_radius=0, fg_color="#200E3A")
        # import entry
        self.import_entry = ctk.CTkEntry(self,width=800,height=40,textvariable=self.path)
        self.import_entry.configure(state="disabled")
        self.import_entry.place(relx=0.5, rely=0.4, anchor="center")
        #import button
        self.import_button = ctk.CTkButton(self,width=400,height=50, text="Import",command=lambda:self.getFile_wrapper())
        self.import_button.configure(fg_color="#200E3A")
        self.import_button.place(relx=0.5, rely=0.5, anchor="center")
        # Show File button
        self.show_file_button = ctk.CTkButton(self,width=400,height=50, text="Show File",command=lambda:self.controller.show_frame(ppf.PrePFrame))
        self.show_file_button.configure(fg_color="#200E3A")
        self.show_file_button.place(relx=0.5, rely=0.6, anchor="center")
               
    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def getFile_wrapper(self):
        self.controller.frames[ppf.PrePFrame].getFile()
    
    def show_wrapper(self):
        self.controller.frames[ppf.PrePFrame].show()