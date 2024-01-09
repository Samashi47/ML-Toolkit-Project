import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkinter import messagebox
import preprocessing.ppframe as ppf
from matplotlib.figure import Figure
import visualization.vizualization_frame as vsf


class SeabornFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent,corner_radius=20,fg_color='transparent')

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)

        # Title
        self.title_label = ctk.CTkLabel(self, text="Visualization using Seaborn", font=('Arial', 20, 'bold'))
        self.title_label.place(relx=0.5, rely=0.1, anchor="center")


        # X Label
        self.x_variable = tk.StringVar()
        self.x_dropdown = ctk.CTkOptionMenu(self, width=30, height=30,values=[])
        self.x_dropdown.place(relx=0.40, rely=0.31, anchor="center")

        self.x_label = ctk.CTkLabel(self,font=('Arial',17), text="Select X Label: ")
        self.x_label.place(anchor="center",relx=0.177, rely=0.3)


        # Y Label
        self.y_label = ctk.CTkLabel(self,font=('Arial',17), text="Select Y Label: ")
        self.y_label.place(anchor="center",relx=0.175, rely=0.5)

        self.y_variable = tk.StringVar()
        self.y_dropdown = ctk.CTkOptionMenu(self, width=30, height=30,values=[])
        self.y_dropdown.place(relx=0.40, rely=0.51, anchor="center")

        # Diagram Type
        self.diagram_label = ctk.CTkLabel(self,font=('Arial',17), text="Select Diagram Type: ")
        self.diagram_label.place(anchor="center",relx=0.177, rely=0.7)

        self.diagram_dropdown = ctk.CTkOptionMenu(self,width=30,height=30,values=["scatter", "barplot", "boxplot", "violinplot", "heatmap"])
        self.diagram_dropdown.place(relx=0.40, rely=0.71, anchor="center")

        # Submit Button
        self.submit_button = ctk.CTkButton(self,width=400,height=45, text="Submit",  command=self.submit)
        self.submit_button.configure(fg_color="#200E3A")
        self.submit_button.place(anchor="center",relx=0.74, rely=0.51)
        # Save Button
        self.submit_button = ctk.CTkButton(self, width=400, height=40, text="Save"
                                           , command=self.save)
        self.submit_button.configure(fg_color="#200E3A")
        self.submit_button.place(anchor="center",relx=0.74, rely=0.71)
        #data
        self.submit_button = ctk.CTkButton(self, width=400, height=40, text="Use the uploaded data")
        self.submit_button.configure(fg_color="#200E3A")
        self.submit_button.place(anchor="center",relx=0.74, rely=0.31)



    def submit(self):
        x_label = self.x_dropdown.get()
        y_label = self.y_dropdown.get()
        diagram_type = self.diagram_dropdown.get()

        if x_label and y_label and diagram_type:
            # Find the visulizeFrame instance in the controller's frames
            visulate_frame = None
            for frame in self.controller.frames.values():
                if isinstance(frame, vsf.visulizeFrame):
                    visulate_frame = frame
                    break

            # Check if a visulizeFrame instance was found
            if visulate_frame:
                visulate_frame.plot_data_seaborn(x_label, y_label, diagram_type)
            else:
                print("Error: visulizeFrame instance not found in controller frames.")
        else:
            messagebox.showerror("Error", "Please select X Label, Y Label, and Diagram Type.")

    def save(self):
        visulate_frame = None
        for frame in self.controller.frames.values():
            if isinstance(frame, vsf.visulizeFrame):
                visulate_frame = frame
                break

        # Check if a visulizeFrame instance was found
        if visulate_frame:
            visulate_frame.save_diagram_as_png()