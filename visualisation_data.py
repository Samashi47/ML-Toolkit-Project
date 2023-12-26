import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import simpledialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class FileImporterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Importer")

        self.import_button = tk.Button(root, text="Import File", command=self.import_file)
        self.import_button.pack(pady=20)

        self.visualize_button = tk.Button(root, text="Visualize File", command=self.visualize_file)
        self.visualize_button.pack(pady=20)

        self.column_listbox = tk.Listbox(root, selectmode=tk.SINGLE)
        self.column_listbox.pack(pady=10)

        self.choose_target_button = tk.Button(root, text="Choose Target Column", command=self.choose_target_column)
        self.choose_target_button.pack(pady=20)

        self.explore_button = tk.Button(root, text="Explore Data", command=self.explore_data)
        self.explore_button.pack(pady=20)

        self.file_data = None
        self.target_column = None

        # Text widget for displaying messages
        self.message_text = tk.Text(self.root, height=2, state=tk.DISABLED)
        self.message_text.pack(expand=True, fill="both", padx=10, pady=10)

        # Frame for displaying Matplotlib plot
        self.plot_frame = tk.Frame(self.root)
        self.plot_frame.pack(side=tk.RIGHT, anchor=tk.NE, padx=10, pady=10)

    def import_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")])
        if file_path:
            try:
                # Use pandas to read the file
                self.file_data = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path)
                self.display_message("Success", "File imported successfully!")
            except Exception as e:
                self.display_message("Error", f"Error importing file: {str(e)}")

    def visualize_file(self):
        if self.file_data is not None:
            # Display the entire data in a table using Treeview
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

            # Populate the column listbox
            self.column_listbox.delete(0, tk.END)
            for col in self.file_data.columns:
                self.column_listbox.insert(tk.END, col)

        else:
            self.display_message("Info", "Please import a file first.")

    def choose_target_column(self):
        selection = self.column_listbox.curselection()
        if selection:
            self.target_column = self.column_listbox.get(selection[0])
            self.display_message("Info", f"Target column set to: {self.target_column}")
        else:
            self.display_message("Info", "Please select a column from the list.")

    def explore_data(self):
        if self.file_data is not None:
            if self.target_column:
                # Include all columns as features (excluding the target column)
                features = [col for col in self.file_data.columns if col != self.target_column]

                valid_plot_types = ["line", "scatter", "bar", "histogram", "boxplot", "pie", "area", "violin", "heatmap", "3d", "errorbars"]
                dialog_title = "Choose Plot Type"
                dialog_prompt = f"Choose the type of plot you want to explore ({', '.join(valid_plot_types)}):"
                plot_type = simpledialog.askstring(dialog_title, dialog_prompt, parent=self.root)

                if plot_type is not None and plot_type.lower() in valid_plot_types:
                    self.plot_data(plot_type.lower(), features)
                else:
                    self.display_message("Info", f"Invalid plot type. Choose one of: {', '.join(valid_plot_types)}")
            else:
                self.display_message("Info", "Please choose a target column first.")
        else:
            self.display_message("Info", "Please import a file first.")

    def plot_data(self, plot_type, features):
        plt.figure(figsize=(8, 6))

        if plot_type == "line":
            for feature in features:
                # Convert the y-axis data to numeric values
                y_data = pd.to_numeric(self.file_data[feature], errors='coerce')

                plt.plot(self.file_data.index, y_data, label=feature)

            plt.xlabel("Index")
            plt.ylabel("Values")
            plt.title("Line Plot of Features")

            # Add a legend only if labels are provided
            if any(feature for feature in features if feature):
                plt.legend()

        # Add conditions for other plot types

        plt.tight_layout()

        # Clear previous plot from the frame
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        # Display the plot in the frame
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