import customtkinter as ctk
from tkinter import messagebox
from matplotlib.figure import Figure
import visualization.vizualization_frame as vsf

class MatplotlibFrame(ctk.CTkFrame):
    """
    A custom frame class for creating a matplotlib plotter frame.

    Args:
        parent: The parent widget.
        controller: The controller object.

    Attributes:
        figure: The matplotlib Figure object.
        ax: The matplotlib Axes object.
        title_label: The label for the title of the plot.
        x_label: The label for selecting the X-axis label.
        x_dropdown: The dropdown menu for selecting the X-axis label.
        y_label: The label for selecting the Y-axis label.
        y_dropdown: The dropdown menu for selecting the Y-axis label.
        z_label: The label for selecting the Z-axis label.
        z_dropdown: The dropdown menu for selecting the Z-axis label.
        diagram_label: The label for selecting the diagram type.
        diagram_dropdown: The dropdown menu for selecting the diagram type.
        submit_button: The button for submitting the plot.
        save_button: The button for saving the plot.
    """
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent,corner_radius=20,fg_color='transparent')

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)

        # Title
        self.title_label = ctk.CTkLabel(self, text="matplotlib Plotter", font=('Arial', 30))
        self.title_label.place(relx=0.5, rely=0.08, anchor="center")

        # X Label
        self.x_label = ctk.CTkLabel(self,font=('Arial',17), text="Select X Label: ")
        self.x_label.place(anchor="center",relx=0.1, rely=0.4)
        self.x_dropdown = ctk.CTkOptionMenu(self, width=150, height=30,values=[])
        self.x_dropdown.configure(fg_color="#200E3A")
        self.x_dropdown.place(relx=0.25, rely=0.41, anchor="center")


        # Y Label
        self.y_label = ctk.CTkLabel(self,font=('Arial',17), text="Select Y Label: ")
        self.y_label.place(anchor="center",relx=0.1, rely=0.6)
        self.y_dropdown = ctk.CTkOptionMenu(self, width=150, height=30,values=[])
        self.y_dropdown.configure(fg_color="#200E3A")
        self.y_dropdown.place(relx=0.25, rely=0.61, anchor="center")

        
        # Z Label
        self.z_label = ctk.CTkLabel(self, font=('Arial', 17), text="Select Z Label: ")
        self.z_label.place(anchor="center", relx=0.402, rely=0.4)
        self.z_dropdown = ctk.CTkOptionMenu(self, width=150, height=30, values=[])
        self.z_dropdown.configure(fg_color="#200E3A")
        self.z_dropdown.place(relx=0.62, rely=0.41, anchor="center")
        
        # Diagram Type
        self.diagram_label = ctk.CTkLabel(self,font=('Arial',17), text="Select Diagram Type: ")
        self.diagram_label.place(anchor="center",relx=0.42, rely=0.6)
        diagram_types = ["Line", "Scatter", "Bar", "Histogram", "Boxplot", "Pie", "Area", "Violin", "3D",
                         "Error Bars"]
        self.diagram_dropdown = ctk.CTkOptionMenu(self,width=150,height=30,values=diagram_types)
        self.diagram_dropdown.configure(fg_color="#200E3A")
        self.diagram_dropdown.place(relx=0.62, rely=0.61, anchor="center")

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
        Submits the selected labels and diagram type for plotting.

        Retrieves the selected labels and diagram type from the dropdown menus.
        Checks if all required fields are selected.
        Finds the visulateFrame instance in the controller's frames.
        Clears the existing plot in the visulateFrame instance.
        Calls the plot_data_matplotlib method in the visulateFrame instance to plot the data.

        Raises:
            - Error: If visulateFrame instance is not found in controller frames.
            - Error: If X Label, Y Label, and Diagram Type are not selected.
        """
        x_label = self.x_dropdown.get()
        y_label = self.y_dropdown.get()
        z_label = self.z_dropdown.get()
        diagram_type = self.diagram_dropdown.get()

        if (x_label is not None) and (y_label is not None) and (diagram_type is not None):
            # Find the visulateFrame instance in the controller's frames
            visulate_frame = None
            for frame in self.controller.frames.values():
                if isinstance(frame, vsf.visulizeFrame):
                    visulate_frame = frame
                    break

            # Check if a visulateFrame instance was found
            if visulate_frame:
                # Clear the existing plot before plotting new data
                visulate_frame.clear_plot()
                visulate_frame.plot_data_matplotlib(x_label, y_label,z_label, diagram_type)
            else:
                print("Error: visulateFrame instance not found in controller frames.")
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