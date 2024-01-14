import customtkinter as ctk
from tkinter import messagebox
from matplotlib.figure import Figure
import visualization.vizualization_frame as vsf


class SeabornFrame(ctk.CTkFrame):
    """
    A custom frame class for creating a Seaborn plotter GUI.

    Attributes:
        controller (object): The controller object for managing the frames.
        figure (matplotlib.figure.Figure): The figure object for the plot.
        ax (matplotlib.axes.Axes): The axes object for the plot.
        title_label (ctk.CTkLabel): The label for the title of the plot.
        x_dropdown (ctk.CTkOptionMenu): The dropdown menu for selecting the X label.
        x_label (ctk.CTkLabel): The label for the X label selection.
        y_label (ctk.CTkLabel): The label for the Y label selection.
        y_dropdown (ctk.CTkOptionMenu): The dropdown menu for selecting the Y label.
        diagram_label (ctk.CTkLabel): The label for the diagram type selection.
        diagram_dropdown (ctk.CTkOptionMenu): The dropdown menu for selecting the diagram type.
        submit_button (ctk.CTkButton): The button for submitting the plot.
        save_button (ctk.CTkButton): The button for saving the plot.

    Methods:
        __init__(self, parent, controller): Initializes the SeabornFrame object.
        submit(self): Submits the plot with the selected labels and diagram type.
        save(self): Saves the plot as a PNG file.
    """
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent,corner_radius=20,fg_color='transparent')

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)

        # Title
        self.title_label = ctk.CTkLabel(self, text="Seaborn Plotter", font=('Arial', 30))
        self.title_label.place(relx=0.5, rely=0.08, anchor="center")

        # X Label
        self.x_dropdown = ctk.CTkOptionMenu(self, width=150, height=30,values=[])
        self.x_dropdown.configure(fg_color="#200E3A")
        self.x_dropdown.place(relx=0.40, rely=0.31, anchor="center")

        self.x_label = ctk.CTkLabel(self,font=('Arial',17), text="Select X Label: ")
        self.x_label.place(anchor="center",relx=0.16, rely=0.3)

        # Y Label
        self.y_label = ctk.CTkLabel(self,font=('Arial',17), text="Select Y Label: ")
        self.y_label.place(anchor="center",relx=0.16, rely=0.5)

        self.y_dropdown = ctk.CTkOptionMenu(self, width=150, height=30,values=[])
        self.y_dropdown.configure(fg_color="#200E3A")
        self.y_dropdown.place(relx=0.40, rely=0.51, anchor="center")

        # Diagram Type
        self.diagram_label = ctk.CTkLabel(self,font=('Arial',17), text="Select Diagram Type: ")
        self.diagram_label.place(anchor="center",relx=0.177, rely=0.7)

        self.diagram_dropdown = ctk.CTkOptionMenu(self,width=150,height=30,values=["scatter", "barplot", "boxplot", "violinplot", "heatmap"])
        self.diagram_dropdown.configure(fg_color="#200E3A")
        self.diagram_dropdown.place(relx=0.40, rely=0.71, anchor="center")

        # Submit Button
        self.submit_button = ctk.CTkButton(self,width=300,height=45, text="Visualize",  command=self.submit)
        self.submit_button.configure(fg_color="#200E3A")
        self.submit_button.place(anchor="center",relx=0.85, rely=0.41)
        # Save Button
        self.save_button = ctk.CTkButton(self, width=300, height=40, text="Save"
                                           , command=self.save)
        self.save_button.configure(fg_color="#200E3A")
        self.save_button.place(anchor="center",relx=0.85, rely=0.61)

    def submit(self):
        """
        Submits the selected X Label, Y Label, and Diagram Type to plot the data using seaborn.
        
        Parameters:
        - None
        
        Returns:
        - None
        """
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