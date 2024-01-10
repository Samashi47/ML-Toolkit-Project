import tkinter as tk
import customtkinter as ctk
import matplotlib_frame as MatplotlibFrame
import seaborn_frame as SeabornFrame
import seaborn as sns
import ppframe as ppf
from matplotlib.figure import Figure
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os


class visulateFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent)
        self.rowconfigure((0, 1), weight=1)
        self.columnconfigure((0), weight=1)
        self.path = tk.StringVar()
        self.figure = Figure(figsize=(2, 2), dpi=50)
        self.ax = self.figure.add_subplot(111)

        #TopFrame
        self.TopFrame = ctk.CTkFrame(self, width=self.winfo_width(), height=self.winfo_height() / 2, corner_radius=20)
        self.TopFrame.grid(row=0, columnspan=4, padx=(10, 10), pady=(10, 10), sticky="nsew")

        # Create the canvas for visualization
        self.visualization_canvas = ctk.CTkCanvas(self, width=self.winfo_reqwidth(), height=self.winfo_reqheight() / 2)
        self.visualization_canvas.grid(row=1, column=0, columnspan=4, padx=(10, 10), pady=(0, 10), sticky="nsew")

        # Create the initial canvas widget
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.visualization_canvas)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Files: matplotlib_frame and seaborn_frame
        self.matplotlib_frame = MatplotlibFrame.MatplotlibFrame(self, controller)
        self.seaborn_frame = SeabornFrame.SeabornFrame(self, controller)

        self.show_frames("Seaborn")

    def show_frames(self, frame):
        if frame == "Matplotlib":
            frame_to_show = self.matplotlib_frame
            frame_to_hide = self.seaborn_frame
        elif frame == "Seaborn":
            frame_to_show = self.seaborn_frame
            frame_to_hide = self.matplotlib_frame
        else:
            return 0

        frame_to_show.place(relx=0.01, rely=0, relwidth=0.98, relheight=0.98, in_=self.TopFrame, bordermode="outside")
        frame_to_hide.place_forget()

    # Add a method to update the canvas with new plot data
    def update_canvas(self):
        self.canvas.draw()

    def clear_plot(self):
        self.ax.clear()
        self.update_canvas()

    def plot_data_seaborn(self, x_label, y_label, diagram_type):
        data = self.controller.frames[ppf.PrePFrame].df
        self.ax.clear()
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
        data = self.controller.frames[ppf.PrePFrame].df

        # Clear all existing subplots from the figure
        for ax in self.figure.get_axes():
            ax.remove()

        # Create a new subplot
        self.ax = self.figure.add_subplot(111)

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
            # Create a new subplot for the 3D plot
            ax_3d = self.figure.add_subplot(111, projection='3d')
            ax_3d.plot_trisurf(data[x_axis], data[y_axis], data[z_axis], cmap='viridis')
        elif diagram_type == "Error Bars":
            error = data[y_axis] * 0.1  # Replace with your error calculation logic
            self.ax.errorbar(data[x_axis], data[y_axis], yerr=error)
        else:
            # Handle the case where x_axis or y_axis is empty
            self.ax.set_xlabel(x_axis)
            self.ax.set_ylabel(y_axis)
            self.ax.set_title(f"No data available for {diagram_type} plot")

        self.update_canvas()

    def save_diagram_as_png(self, filename="diagram.png"):
        # Check if the save directory exists, create if not
        save_dir = "saved_diagrams"
        os.makedirs(save_dir, exist_ok=True)

        # Save the figure as PNG
        save_path = os.path.join(save_dir, filename)
        self.figure.savefig(save_path, bbox_inches="tight")

        messagebox.showinfo("Save Successful", f"Diagram saved as {save_path}")