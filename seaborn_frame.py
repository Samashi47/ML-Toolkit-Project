import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkinter import messagebox
import ppframe as ppf
from matplotlib.figure import Figure
import Visulateframe as visulateFrame


class SeabornFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = controller  # Assuming the controller attribute points to visulateFrame

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)

        # Title
        self.title_label = ttk.Label(self, text="Visualization using Seaborn", font=('Arial', 20, 'bold'))
        self.title_label.place(relx=0.5, rely=0.1, anchor="center")

        # X Label
        self.x_variable = tk.StringVar()
        self.x_dropdown = ttk.Combobox(self, width=30, height=30,
                                          textvariable=self.x_variable, state="readonly")
        self.x_dropdown.place(relx=0.40, rely=0.31, anchor="center")

        self.x_label = ctk.CTkLabel(self,font=('Arial',17), text="Select X Label: ")
        self.x_label.place(anchor="center",relx=0.177, rely=0.3)

        # Y Label
        self.y_label = tk.Label(self,font=('Arial',17), text="Select Y Label: ")
        self.y_label.place(anchor="center",relx=0.175, rely=0.5)

        self.y_variable = tk.StringVar()
        self.y_dropdown = ttk.Combobox(self, width=30, height=30, textvariable=self.y_variable, state="readonly")
        self.y_dropdown.place(relx=0.40, rely=0.51, anchor="center")

        # Diagram Type
        self.diagram_label = tk.Label(self,font=('Arial',17), text="Select Diagram Type: ")
        self.diagram_label.place(anchor="center",relx=0.177, rely=0.7)

        diagram_types = ["scatter", "barplot", "boxplot", "violinplot", "heatmap"]
        self.diagram_variable = tk.StringVar()
        self.diagram_dropdown = ttk.Combobox(self,width=30,height=30,
                                          textvariable=self.diagram_variable, values=diagram_types, state="readonly")
        self.diagram_dropdown.place(relx=0.40, rely=0.71, anchor="center")

        # Submit Button
        self.submit_button = ctk.CTkButton(self, width=400, height=45, text="Submit", command=self.submit)
        self.submit_button.configure(fg_color="#200E3A")
        self.submit_button.place(anchor="center", relx=0.74, rely=0.71)
        # Save Button
        self.save_button = ctk.CTkButton(self, width=400, height=40, text="Save"
                                         , command=self.save)
        self.save_button.configure(fg_color="#200E3A")
        self.save_button.place(anchor="center", relx=0.74, rely=0.91)
        # use old data Button
        self.data_button = ctk.CTkButton(self, width=400, height=40, text="Use the uploaded Data", command=self.data)
        self.data_button.configure(fg_color="#200E3A")
        self.data_button.place(anchor="center", relx=0.74, rely=0.31)
        # import Button
        self.import_button = ctk.CTkButton(self, width=400, height=40, text="Import Data",
                                           command=lambda: self.controller.frames[ppf.PrePFrame].getFile())
        self.import_button.configure(fg_color="#200E3A")
        self.import_button.place(anchor="center", relx=0.74, rely=0.51)

        # Populate dropdowns when the frame is created
        self.bind("<Map>", self.populate_dropdowns)

    def populate_dropdowns(self, event=None):
        # Get the reference to the PrePFrame
        prep_frame = self.controller.frames[ppf.PrePFrame]

        # Get the DataFrame from the PrePFrame
        data = prep_frame.df
        if data is None:
            print("Error: DataFrame is not loaded.")
            return
        else:
            # Populate X and Y dropdowns with column names
            columns = data.columns.tolist()
            self.x_dropdown['values'] = columns
            self.y_dropdown['values'] = columns


    def submit(self):
        x_label = self.x_variable.get()
        y_label = self.y_variable.get()
        diagram_type = self.diagram_variable.get()

        if x_label and y_label and diagram_type:
            # Find the visulateFrame instance in the controller's frames
            visulate_frame = None
            for frame in self.controller.frames.values():
                if isinstance(frame, visulateFrame.visulateFrame):
                    visulate_frame = frame
                    break

            # Check if a visulateFrame instance was found
            if visulate_frame:
                # Clear the existing plot before plotting new data
                visulate_frame.clear_plot()
                visulate_frame.plot_data_seaborn(x_label, y_label, diagram_type)
            else:
                print("Error: visulateFrame instance not found in controller frames.")
        else:
            messagebox.showerror("Error", "Please select X Label, Y Label, and Diagram Type.")


    def data(self):
        if not self.x_dropdown['values']:
            self.populate_dropdowns()

    def save(self):
        visulate_frame = None
        for frame in self.controller.frames.values():
            if isinstance(frame, visulateFrame.visulateFrame):
                visulate_frame = frame
                break

        # Check if a visulateFrame instance was found
        if visulate_frame:
            visulate_frame.save_diagram_as_png()
