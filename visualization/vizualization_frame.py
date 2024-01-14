import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import os
import seaborn as sns
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import visualization.subframes.matplotlib_frame as mpl
import visualization.subframes.seaborn_frame as snsf
import preprocessing.ppframe as ppf

class visulizeFrame(ctk.CTkFrame):
    """
    A custom frame class for visualization in the ML Toolkit Project.

    Attributes:
        controller (object): The controller object for the frame.
        path (tk.StringVar): The path of the visualization.
        figure (matplotlib.figure.Figure): The figure object for the visualization.
        ax (matplotlib.axes.Axes): The axes object for the visualization.
        ax_3d (matplotlib.axes.Axes3D): The 3D axes object for the visualization.
        TopFrame (ctk.CTkFrame): The top frame of the visualization.
        visualization_canvas (ctk.CTkCanvas): The canvas for the visualization.
        canvas (matplotlib.backends.backend_tkagg.FigureCanvasTkAgg): The canvas widget for the visualization.
        canvas_widget (tk.Widget): The tkinter widget for the canvas.
        toolbar (NavigationToolbar2Tk): The toolbar for the visualization.
        matplotlib_frame (mpl.MatplotlibFrame): The matplotlib frame for the visualization.
        seaborn_frame (snsf.SeabornFrame): The seaborn frame for the visualization.
    """
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent)
        self.rowconfigure((0, 1), weight=1)
        self.columnconfigure((0), weight=1)
        self.path = tk.StringVar()
        self.figure = Figure(figsize=(2, 2), dpi=50)
        self.ax = self.figure.add_subplot(111)
        self.ax_3d = None

        #TopFrame
        self.TopFrame = ctk.CTkFrame(self, width=self.winfo_width(), height=self.winfo_height() / 2, corner_radius=20)
        self.TopFrame.grid(row=0, columnspan=4, padx=(10, 10), pady=(10, 10), sticky="nsew")

        # Create the canvas for visualization
        self.visualization_canvas = ctk.CTkCanvas(self, width=self.winfo_width(), height=self.winfo_height() / 2)
        self.visualization_canvas.grid(row=1, columnspan=4, padx=(10, 10), pady=(0, 10), in_=self, sticky="nsew")
        
        
        # Create the initial canvas widget
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.visualization_canvas)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.visualization_canvas)
        self.toolbar.update()
        self.toolbar.pack(side=tk.LEFT, fill=tk.Y)  # Align the toolbar on the right side vertically
        
        # Files: matplotlib_frame and seaborn_frame
        self.matplotlib_frame = mpl.MatplotlibFrame(self.TopFrame, self.controller)
        self.seaborn_frame = snsf.SeabornFrame(self.TopFrame, self.controller)

    # Add a method to update the canvas with new plot data
    def update_canvas(self):
        self.canvas.draw()

    def clear_plot(self):
        self.ax.clear()
        self.update_canvas()
    
    def plot_data_seaborn(self, x_label, y_label, diagram_type):
        """
        Plot data using Seaborn library based on user selections.

        Args:
            x_label (str): The label for the x-axis.
            y_label (str): The label for the y-axis.
            diagram_type (str): The type of diagram to be plotted.

        Returns:
            None
        """
        data = self.controller.frames[ppf.PrePFrame].df
        # Clear all existing subplots from the figure
        for self.ax in self.figure.get_axes():
            self.ax.remove()
        # Create a new subplot
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_label)
        self.ax.set_title(diagram_type+" Diagram"+" of "+x_label+" and "+y_label)
        # Seaborn plot based on user selections
        if diagram_type == "scatter":
            sns.scatterplot(x=x_label, y=y_label, data=data, ax=self.ax)
        elif diagram_type == "barplot":
            sns.barplot(x=x_label, y=y_label, data=data, ax=self.ax)
        elif diagram_type == "boxplot":
            sns.boxplot(x=x_label, y=y_label, data=data, ax=self.ax)
        elif diagram_type == "violinplot":
            sns.violinplot(x=x_label, y=y_label, data=data, ax=self.ax)
        elif diagram_type == "heatmap":
            pivot_table = data.pivot_table(values=y_label, index=x_label, aggfunc="mean")
            sns.heatmap(pivot_table, annot=True, cmap="YlGnBu", ax=self.ax)
        else:
            return

        self.update_canvas()

    def plot_data_matplotlib(self, x_axis, y_axis, z_axis, diagram_type):
        """
        Plot data using Matplotlib library.

        Args:
            x_axis (str): The column name for the x-axis.
            y_axis (str): The column name for the y-axis.
            z_axis (str): The column name for the z-axis (optional, used for 3D plots).
            diagram_type (str): The type of diagram to plot.

        Returns:
            None
        """
        data = self.controller.frames[ppf.PrePFrame].df

        # Clear all existing subplots from the figure
        for self.ax in self.figure.get_axes():
            self.ax.remove()

        # Create a new subplot
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlabel(x_axis)
        self.ax.set_ylabel(y_axis)
        self.ax.set_title(diagram_type+" Diagram"+" of "+x_axis+" and "+y_axis)

        if diagram_type == "Line":
            # Line plot with legend for differentiating lines
            self.ax.plot(data[x_axis], data[y_axis], label=z_axis)
            self.ax.legend()
        elif diagram_type == "Scatter":
            self.ax.scatter(data[x_axis], data[y_axis])
        elif diagram_type == "Bar":
            self.ax.bar(data[x_axis], data[y_axis])
        elif diagram_type == "Histogram":
            self.ax.hist(data[y_axis], bins='auto', alpha=0.7, rwidth=0.85)
        elif diagram_type == "Boxplot":
            self.ax.boxplot(data[y_axis])
        elif diagram_type == "Pie":
            self.ax.pie(data[y_axis], labels=data[x_axis], autopct='%1.1f%%', startangle=90)
        elif diagram_type == "Area":
            self.ax.fill_between(data[x_axis], data[y_axis], label=y_axis, alpha=0.5)
            if any(feature for feature in [x_axis, y_axis] if feature):
                self.ax.legend()
        elif diagram_type == "Violin":
            sns.violinplot(x=data[x_axis], y=data[y_axis], ax=self.ax)
            self.ax.set_title("Violin Plot")
        elif diagram_type == "3D":
            if z_axis:
            # Create a new subplot for the 3D plot
                self.ax_3d = self.figure.add_subplot(111, projection='3d')
                self.ax_3d.plot_trisurf(data[x_axis], data[y_axis], data[z_axis], cmap='viridis')
                self.ax_3d.set_xlabel(x_axis, fontsize=30, rotation = 0)
                self.ax_3d.set_ylabel(y_axis, fontsize=30, rotation = 0)
                self.ax_3d.set_zlabel(z_axis, fontsize=30, rotation = 0)
                self.ax_3d.set_title(diagram_type+" Diagram"+" of "+x_axis+" and "+y_axis+'and'+z_axis)
        elif diagram_type == "Error Bars":
            error = data[y_axis] * 0.1  # Replace with your error calculation logic
            self.ax.errorbar(data[x_axis], data[y_axis], yerr=error)
        else:
            # Handle the case where x_axis or y_axis is empty
            self.ax.set_xlabel(x_axis)
            self.ax.set_ylabel(y_axis)
            self.ax.set_title(f"No data available for {diagram_type} plot")

        self.update_canvas()

    def save_diagram_as_png(self, filename="seaborn_diagram.png"):
        """
        Saves the diagram as a PNG file.

        Args:
            filename (str, optional): The name of the PNG file to be saved. Defaults to "seaborn_diagram.png".
        """
        # Check if the save directory exists, create if not
        save_dir = "saved_diagrams"
        os.makedirs(save_dir, exist_ok=True)

        # Save the figure as PNG
        save_path = os.path.join(save_dir, filename)
        self.figure.savefig(save_path, bbox_inches="tight")

        messagebox.showinfo("Save Successful", f"Diagram saved as {save_path}")
        