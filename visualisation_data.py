import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class FileImporterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Toolkit")
        self.root.attributes("-fullscreen", True)
        self.file_data = None

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.RIGHT, anchor=tk.NE, padx=10, pady=10)

        self.plot_frame = tk.Frame(self.root)
        self.plot_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

        self.import_button = tk.Button(self.button_frame, text="Import File", command=self.import_file, width=15, height=2)
        self.import_button.pack(pady=20)

        self.visualize_button = tk.Button(self.button_frame, text="Visualize File", command=self.visualize_file, width=15, height=2)
        self.visualize_button.pack(pady=20)

        self.x_label = tk.Label(self.button_frame, text="Select X Axis:")
        self.x_label.pack(pady=10)
        self.x_variable = tk.StringVar()
        self.x_variable.set("Index")  # Default value
        self.x_dropdown = ttk.Combobox(self.button_frame, textvariable=self.x_variable)
        self.x_dropdown.pack(pady=10)

        self.y_label = tk.Label(self.button_frame, text="Select Y Axis:")
        self.y_label.pack(pady=10)
        self.y_variable = tk.StringVar()
        self.y_variable.set("")  # Default value
        self.y_dropdown = ttk.Combobox(self.button_frame, textvariable=self.y_variable)
        self.y_dropdown.pack(pady=10)
        self.diagram_variable = tk.StringVar()
        self.diagram_variable.set("")  # Default value

        self.diagram_label = tk.Label(self.button_frame, text="Select diagramm type:")
        self.diagram_label.pack(pady=10)
        diagram_types = ["Line", "Scatter", "Bar", "Histogram", "Boxplot", "Pie", "Area", "Violin", "Heatmap", "3D",
                         "Error Bars"]

        self.diagram_dropdown = ttk.Combobox(self.button_frame, textvariable=self.diagram_variable,
                                             values=diagram_types)
        self.diagram_dropdown.pack(pady=10)
        self.explore_button = tk.Button(self.button_frame, text="Explore Data", command=self.explore_data, width=15, height=2)
        self.explore_button.pack(pady=20)

        self.message_text = tk.Text(self.root, height=2, state=tk.DISABLED)
        self.message_text.pack(expand=True, fill="both", padx=10, pady=10)

    def import_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")])
        if file_path:
            try:
                self.file_data = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path)
                self.display_message("Success", "File imported successfully!")
            except Exception as e:
                self.display_message("Error", f"Error importing file: {str(e)}")

    def visualize_file(self):
        if self.file_data is not None:
            if hasattr(self, 'treeview'):
                self.treeview.destroy()

            self.treeview = ttk.Treeview(self.root)
            self.treeview["columns"] = tuple(self.file_data.columns)

            for col in self.treeview["columns"]:
                self.treeview.heading(col, text=col)
                self.treeview.column(col, anchor="center")

            for i, row in self.file_data.iterrows():
                self.treeview.insert("", tk.END, values=tuple(row))

            self.treeview.pack(expand=True, fill="both", padx=10, pady=10)

            self.x_dropdown['values'] = tuple(self.file_data.columns)
            self.y_dropdown['values'] = tuple(self.file_data.columns)

        else:
            self.display_message("Info", "Please import a file first.")

    def explore_data(self):
        if self.file_data is not None:
            # Get the selected diagram type
            diagram_type = self.diagram_variable.get().lower()

            if diagram_type:
                # Get the X and Y axes
                x_axis = self.x_variable.get()
                y_axis = self.y_variable.get()

                # Call the plot_data function with the selected diagram type and X, Y axes
                self.plot_data(diagram_type, x_axis, y_axis)
            else:
                self.display_message("Info", "Please select at least one diagram type.")
        else:
            self.display_message("Info", "Please import a file first.")

    def select_diagram_type(self):
        selected_indices = self.diagram_listbox.curselection()

        if selected_indices:
            selected_diagram = self.diagram_listbox.get(selected_indices[0])
            self.display_message("Info", f"Selected Diagram: {selected_diagram}")
        else:
            self.display_message("Info", "Please select at least one diagram type.")

    def plot_data(self, diagram_type, x_axis, y_axis):
        plt.figure(figsize=(8, 6))

        # Filter out non-numeric values for X and Y axes
        x_data = pd.to_numeric(self.file_data[x_axis], errors='coerce').dropna()
        y_data = pd.to_numeric(self.file_data[y_axis], errors='coerce').dropna()

        if not x_data.empty and not y_data.empty:
            if diagram_type == "line":
                plt.plot(x_data, y_data)
                plt.xlabel(x_axis)
                plt.ylabel(y_axis)
                plt.title("Line Plot")
            elif diagram_type == "scatter":
                plt.scatter(x_data, y_data)
                plt.xlabel(x_axis)
                plt.ylabel(y_axis)
                plt.title("Scatter Plot")
            elif diagram_type == "bar":
                plt.bar(x_data, y_data)
                plt.xlabel(x_axis)
                plt.ylabel(y_axis)
                plt.title("Bar Plot")
            elif diagram_type == "histogram":
                plt.hist(y_data, bins='auto', alpha=0.7, rwidth=0.85)
            elif diagram_type == "boxplot":
                plt.boxplot(y_data)
            elif diagram_type == "pie":
                plt.pie(y_data, labels=x_data, autopct='%1.1f%%', startangle=90)
                plt.title("Pie Chart")
            elif diagram_type == "area":
                plt.fill_between(x_data, y_data, label=y_axis, alpha=0.5)
                plt.xlabel(x_axis)
                plt.ylabel(y_axis)
                plt.title("Area Plot")
                if any(feature for feature in [x_axis, y_axis] if feature):
                    plt.legend()
            elif diagram_type == "violin":
                plt.violinplot([y_data], showmeans=True)
                plt.xticks([1], [y_axis])
                plt.ylabel(y_axis)
                plt.title("Violin Plot")
            elif diagram_type == "heatmap":
                plt.imshow([y_data], cmap='viridis', aspect='auto', interpolation='none')
                plt.colorbar()
                plt.xlabel(x_axis)
                plt.ylabel(y_axis)
                plt.title("Heatmap")
            elif diagram_type == "3D":
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                ax.plot_trisurf(x_data, y_data, cmap='viridis')
                ax.set_xlabel(x_axis)
                ax.set_ylabel(y_axis)
                ax.set_zlabel("Z-axis")
        elif diagram_type == "errorbars":
                error = y_data * 0.1  # Replace with your error calculation logic
                plt.errorbar(x_data, y_data, yerr=error)
                plt.xlabel(x_axis)
                plt.ylabel(y_axis)
                plt.title("Error Bars Plot")
        else:
            # Handle the case where x_data or y_data is empty
            plt.xlabel(x_axis)
            plt.ylabel(y_axis)
            plt.title(f"No data available for {diagram_type} plot")

        # Clear previous plot from the frame
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        # Use FigureCanvasTkAgg to embed the plot in the Tkinter window
        canvas = FigureCanvasTkAgg(plt.gcf(), master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def display_message(self, title, message):
        self.message_text.config(state=tk.NORMAL)
        self.message_text.delete(1.0, tk.END)
        self.message_text.insert(tk.END, f"{title}: {message}")
        self.message_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileImporterApp(root)
    root.mainloop()
