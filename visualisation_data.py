import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import pandas as pd

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

        self.file_data = None
        self.target_column = None

        # Text widget for displaying messages
        self.message_text = tk.Text(self.root, height=2, state=tk.DISABLED)
        self.message_text.pack(expand=True, fill="both", padx=10, pady=10)

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

    def display_message(self, title, message):
        self.message_text.config(state=tk.NORMAL)
        self.message_text.delete(1.0, tk.END)
        self.message_text.insert(tk.END, f"{title}: {message}")
        self.message_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileImporterApp(root)
    root.mainloop()
