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
        self.target_column = None

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.RIGHT, anchor=tk.NE, padx=10, pady=10)

        self.plot_frame = tk.Frame(self.root)
        self.plot_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

        self.import_button = tk.Button(self.button_frame, text="Import File", command=self.import_file, width=15, height=2)
        self.import_button.pack(pady=20)

        self.visualize_button = tk.Button(self.button_frame, text="Visualize File", command=self.visualize_file, width=15, height=2)
        self.visualize_button.pack(pady=20)

        self.column_listbox = tk.Listbox(self.button_frame, selectmode=tk.SINGLE)
        self.column_listbox.pack(pady=2)

        self.choose_target_button = tk.Button(self.button_frame, text="Choose Target Column", command=self.choose_target_column, width=15, height=2)
        self.choose_target_button.pack(pady=20)

        self.diagram_listbox = tk.Listbox(self.button_frame, selectmode=tk.SINGLE)
        self.diagram_listbox.pack(pady=10)

        diagram_types = ["Line", "Scatter", "Bar", "Histogram", "Boxplot", "Pie", "Area", "Violin", "Heatmap", "3D", "Error Bars"]
        for diagram_type in diagram_types:
            self.diagram_listbox.insert(tk.END, diagram_type)

        self.select_diagram_button = tk.Button(self.button_frame, text="Select Diagram Type", command=self.select_diagram_type, width=20, height=2)
        self.select_diagram_button.pack(pady=20)

        self.explore_button = tk.Button(self.button_frame, text="Explore Data", command=self.explore_data, width=15, height=2)
        self.explore_button.pack(pady=20)

        self.file_data = None
        self.target_column = None

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

            self.column_listbox.delete(0, tk.END)
            for col in self.file_data.columns:
                self.column_listbox.insert(tk.END, col)

        else:
            self.display_message("Info", "Please import a file first.")

    def choose_target_column(self):
        selection = self.column_listbox.curselection()
        if selection:
            selected_column = self.column_listbox.get(selection[0])
            self.target_column = selected_column
            self.display_message("Info", f"Target column set to: {self.target_column}")

            # Add additional feature: Disable the button after a target column is chosen
            self.choose_target_button.config(state=tk.DISABLED)

            # Add additional feature: Change the background color of the selected column in the listbox
            self.column_listbox.itemconfig(selection[0], {'bg': 'lightgreen'})

            # Call explore_data with the selected column
            self.explore_data()
        else:
            self.display_message("Info", "Please select a column from the list.")

    def explore_data(self):
        if self.file_data is not None:
            if self.target_column:
                # Get the selected columns and diagram types
                selected_columns = list(self.column_listbox.get(0, tk.END))
                diagram_type_indices = self.diagram_listbox.curselection()

                if diagram_type_indices:
                    # Get the diagram types
                    diagram_types = [self.diagram_listbox.get(idx).lower() for idx in diagram_type_indices]
                    # Call the plot_data function with the selected columns and diagram types
                    self.plot_data(selected_columns, diagram_types)
                else:
                    self.display_message("Info", "Please select at least one diagram type.")
            else:
                self.display_message("Info", "Please choose a target column first.")
        else:
            self.display_message("Info", "Please import a file first.")

    def select_diagram_type(self):
        selected_indices = self.diagram_listbox.curselection()

        if selected_indices:
            selected_diagrams = [self.diagram_listbox.get(idx) for idx in selected_indices]
            self.display_message("Info", f"Selected Diagrams: {', '.join(selected_diagrams)}")
        else:
            self.display_message("Info", "Please select at least one diagram type.")

    def plot_data(self, features, diagram_types):
        for diagram_type in diagram_types:
            plt.figure(figsize=(8, 6))
            for feature in features:
                y_data = pd.to_numeric(self.file_data[feature], errors='coerce')
                # Remove NaN values
                y_data = y_data.dropna()

                if diagram_type == "line":
                    for feature in features:
                        y_data = pd.to_numeric(self.file_data[feature], errors='coerce')
                        plt.plot(self.file_data.index, y_data, label=feature)
                    plt.xlabel("Index")
                    plt.ylabel("Values")
                    plt.title("Line Plot of Features")
                    if any(feature for feature in features if feature):
                        plt.legend()
                elif diagram_type == "scatter":
                    for feature in features:
                        x_data = self.file_data.index
                        y_data = pd.to_numeric(self.file_data[feature], errors='coerce')
                        plt.scatter(x_data, y_data, label=feature)

                    plt.xlabel("Index")
                    plt.ylabel("Values")
                    plt.title("Scatter Plot of Features")
                    if any(feature for feature in features if feature):
                        plt.legend()
                elif diagram_type == "bar":
                    for feature in features:
                        x_data = self.file_data.index
                        y_data = pd.to_numeric(self.file_data[feature], errors='coerce')
                        plt.bar(x_data, y_data, label=feature)

                    plt.xlabel("Index")
                    plt.ylabel("Values")
                    plt.title("Bar Plot of Features")
                    if any(feature for feature in features if feature):
                        plt.legend()
                elif diagram_type == "histogram":
                    for feature in features:
                        y_data = pd.to_numeric(self.file_data[feature], errors='coerce')

                        y_data = y_data.dropna()  # Drop NaN values

                        plt.hist(y_data, label=feature, alpha=0.7)
                elif diagram_type == "boxplot":
                    data_to_plot = [pd.to_numeric(self.file_data[feature], errors='coerce') for feature in features]
                    plt.boxplot(data_to_plot, labels=features)
                    plt.ylabel("Values")
                    plt.title("Boxplot of Features")
                elif diagram_type == "pie":
                    for feature in features:
                        y_data = pd.to_numeric(self.file_data[feature], errors='coerce')
                        y_data = y_data.dropna()  # Drop NaN values
                        # Modify the labels to match the length of y_data
                        labels = self.file_data.index[:len(y_data)]
                        plt.pie(y_data, labels=labels, autopct='%1.1f%%', startangle=90)
                        plt.title(f"Pie Chart of {feature}")
                elif diagram_type == "area":
                    for feature in features:
                        y_data = pd.to_numeric(self.file_data[feature], errors='coerce')
                        plt.fill_between(self.file_data.index, y_data, label=feature, alpha=0.5)

                    plt.xlabel("Index")
                    plt.ylabel("Values")
                    plt.title("Area Plot of Features")
                    if any(feature for feature in features if feature):
                        plt.legend()
                elif diagram_type == "violin":
                    data_to_plot = [pd.to_numeric(self.file_data[feature], errors='coerce') for feature in features]
                    plt.violinplot(data_to_plot, showmeans=True)
                    plt.xticks(range(1, len(features) + 1), features)
                    plt.ylabel("Values")
                    plt.title("Violin Plot of Features")
                elif diagram_type == "heatmap":
                    data_to_plot = self.file_data[features].apply(pd.to_numeric, errors='coerce')
                    plt.imshow(data_to_plot.T, cmap='viridis', aspect='auto', interpolation='none')
                    plt.colorbar()
                    plt.xlabel("Index")
                    plt.yticks(range(len(features)), features)
                    plt.title("Heatmap of Features")
                elif diagram_type == "3d":
                    fig = plt.figure()
                    ax = fig.add_subplot(111, projection='3d')
                    for feature in features:
                        x_data = self.file_data.index
                        y_data = pd.to_numeric(self.file_data[feature], errors='coerce').fillna(0)
                        ax.plot(x_data, y_data, zs=0, label=feature)
                    ax.set_xlabel("Index")
                    ax.set_ylabel("Values")
                    ax.set_zlabel("Z-axis")
                    ax.set_title("3D Plot of Features")
                    if any(feature for feature in features if feature):
                        ax.legend()
                    # Use FigureCanvasTkAgg from mpl_toolkits.mplot3d
                    canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
                    canvas.draw()
                    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
                elif diagram_type == "errorbars":
                    for feature in features:
                        x_data = self.file_data.index
                        y_data = pd.to_numeric(self.file_data[feature], errors='coerce').fillna(0)
                        error = y_data * 0.1  # Replace with your error calculation logic
                        plt.errorbar(x_data, y_data, yerr=error, label=feature)
                    plt.xlabel("Index")
                    plt.ylabel("Values")
                    plt.title("Error Bars Plot of Features")
                    if any(feature for feature in features if feature):
                        plt.legend()
                    # Use FigureCanvasTkAgg directly without creating a TkAgg backend
                    canvas = FigureCanvasTkAgg(plt.gcf(), master=self.plot_frame)
                    canvas.draw()
                    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

            plt.xlabel("Index")
            plt.ylabel("Values")
            plt.title(f"{str(diagram_type).capitalize()} Plot of Features")
            if any(feature for feature in features if feature):
                plt.legend()
                # Clear previous plot from the frame
            for widget in self.plot_frame.winfo_children():
                widget.destroy()

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