import tkinter as tk
import customtkinter as ctk
import matplotlib_frame as MatplotlibFrame
import seaborn_frame as SeabornFrame
import seaborn as sns
import ppframe as ppf
from matplotlib.figure import Figure
from tkinter import messagebox
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkagg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os


class visulateFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent)
        self.rowconfigure((0, 1), weight=1)
        self.columnconfigure((0), weight=1)
        self.path = tk.StringVar()
        self.visualization_canvas = tk.Canvas(self)
        self.figure_seaborn = Figure(figsize=(2, 2), dpi=50)
        self.ax_seaborn = self.figure_seaborn.add_subplot(111)

        self.figure_matplotlib = Figure(figsize=(2, 2), dpi=50)
        self.ax_matplotlib = self.figure_matplotlib.add_subplot(111)

        #TopFrame
        self.TopFrame = ctk.CTkFrame(self, width=self.winfo_width(), height=self.winfo_height() / 2, corner_radius=20)
        self.TopFrame.grid(row=0, columnspan=4, padx=(10, 10), pady=(10, 10), sticky="nsew")

        # Create the canvas for visualization
        self.visualization_canvas = ctk.CTkCanvas(self, width=self.winfo_width(), height=self.winfo_height() / 2)
        self.visualization_canvas.grid(row=1, columnspan=4, padx=(10, 10), pady=(0, 10), in_=self, sticky="nsew")
        self.visualization_canvas.grid_propagate(False)  # Fix: Set grid_propagate to False


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

    def plot_data_seaborn(self, x_label, y_label, diagram_type):
        data = self.controller.frames[ppf.PrePFrame].df
        # Clear the previous canvas widget
        self.visualization_canvas.delete("all")

        # Seaborn plot based on user selections
        if diagram_type == "scatter":
            sns.scatterplot(x=x_label, y=y_label, data=data, ax=self.ax_seaborn)
        elif diagram_type == "barplot":
            sns.barplot(x=x_label, y=y_label, data=data, ax=self.ax_seaborn)
        elif diagram_type == "boxplot":
            sns.boxplot(x=x_label, y=y_label, data=data, ax=self.ax_seaborn)
        elif diagram_type == "violinplot":
            sns.violinplot(x=x_label, y=y_label, data=data, ax=self.ax_seaborn)
        elif diagram_type == "heatmap":
            pivot_table = data.pivot_table(values=y_label, index=x_label, aggfunc="mean")
            sns.heatmap(pivot_table, annot=True, cmap="YlGnBu", ax=self.ax_seaborn)
        else:
            return

        # Clear previous plot from the frame
        for canvas_widget in self.visualization_canvas.winfo_children():
            canvas_widget.destroy()

        # Draw the new plot on the canvas
        canvas = FigureCanvasTkAgg(self.figure_seaborn, master=self.visualization_canvas)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def plot_data_matplotlib(self, x_label, y_label, diagram_type):
        data = self.controller.frames[ppf.PrePFrame].df

        # Clear the previous canvas widget
        self.visualization_canvas.delete("all")

        # Matplotlib plot based on user selections
        if diagram_type == "Line":
            plt.plot(data[x_label], data[y_label])
        elif diagram_type == "Scatter":
            plt.scatter(data[x_label], data[y_label])
        elif diagram_type == "Bar":
            plt.bar(data[x_label], data[y_label])
        elif diagram_type == "Histogram":
            plt.hist(data[y_label], bins='auto')
        elif diagram_type == "Boxplot":
            plt.boxplot(data[y_label])
        elif diagram_type == "Pie":
            plt.pie(data[y_label], labels=data[x_label], autopct='%1.1f%%')
        elif diagram_type == "Area":
            plt.fill_between(data[x_label], data[y_label], alpha=0.5)
        elif diagram_type == "Violin":
            sns.violinplot(x=x_label, y=y_label, data=data)
        elif diagram_type == "Heatmap":
            pivot_table = data.pivot_table(values=y_label, index=x_label, aggfunc="mean")
            sns.heatmap(pivot_table, annot=True, cmap="YlGnBu")
        elif diagram_type == "3D":
            # Implement 3D plot logic
            pass
        elif diagram_type == "Error Bars":
            # Implement error bars plot logic
            pass
        else:
            return

        self.visualization_canvas.delete("all")
        # Clear previous plot from the frame
        for widget in self.visualization_canvas.winfo_children():
            widget.destroy()
        # Draw the new plot on the canvas
        canvas = FigureCanvasTkAgg(self.figure_matplotlib, master=self.visualization_canvas)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def save_diagram_as_png(self, filename="seaborn_diagram.png"):
        # Check if the save directory exists, create if not
        save_dir = "saved_diagrams"
        os.makedirs(save_dir, exist_ok=True)

        # Save the figure as PNG
        save_path = os.path.join(save_dir, filename)
        self.figure.savefig(save_path, bbox_inches="tight")

        messagebox.showinfo("Save Successful", f"Diagram saved as {save_path}")