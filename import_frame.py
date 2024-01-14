import tkinter as tk
import customtkinter as ctk
import preprocessing.ppframe as ppf

class StartFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
            """
            Initializes the ImportFrame class.

            Args:
                parent: The parent widget.
                controller: The controller object.

            Returns:
                None
            """
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
            self.import_button = ctk.CTkButton(self,width=400,height=50, text="Import",command=lambda:self.controller.frames[ppf.PrePFrame].getFile())
            self.import_button.configure(fg_color="#200E3A")
            self.import_button.place(relx=0.5, rely=0.5, anchor="center")
            # Show File button
            self.show_file_button = ctk.CTkButton(self,width=400,height=50, text="Show File",state='disabled',command=lambda:self.controller.show_main_frame(ppf.PrePFrame))
            self.show_file_button.configure(fg_color="#200E3A")
            self.show_file_button.place(relx=0.5, rely=0.6, anchor="center")
               
    