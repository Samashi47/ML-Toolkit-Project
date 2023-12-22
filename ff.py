import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd
from tksheet import Sheet

class NewprojectApp:
    def __init__(self, master=None):
        # build ui
        main_window = ttk.Frame(master)
        label_1 = ttk.Label(main_window)
        label_1.config(font='{sans } 12 {bold}', justify='center', padding='100', text='PREDIKSI IHSG BBCA.JK')
        label_1.pack(side='top')
        button_1 = ttk.Button(main_window)
        button_1.config(text='Import File', command=self.getCSV)
        button_1.place(anchor='nw', relx='0.14', rely='0.66', x='0', y='0')
        button_2 = ttk.Button(main_window)
        button_2.config(text='Show File', command=self.show)
        button_2.place(anchor='nw', relwidth='0.31', relx='0.55', rely='0.66', x='0', y='0')

        # Frame to hold DataFrame
        self.df_frame = ttk.Frame(main_window)
        self.df_frame.pack(side='top', pady=10)

        main_window.config(height='200', width='200')
        main_window.pack(side='top')

        # Main widget
        self.mainwindow = main_window
        self.df = None  # Initialize df as an instance variable

    def run(self):
        self.mainwindow.mainloop()

    def getCSV(self):
        file_path = filedialog.askopenfilename()
        if file_path.endswith('.csv'):
            self.df = pd.read_csv(file_path)
        elif file_path.endswith(('.xls', '.xlsx')):
            self.df = pd.read_excel(file_path)
        else:
            print("Unsupported file format. Please select a CSV or Excel file.")
            return


    def show(self):
        if self.df is None:
            print("Please import a file first.")
            return

        # Clear previous DataFrame display
        for widget in self.df_frame.winfo_children():
            widget.destroy()

        # Display DataFrame using tksheet
        sheet = Sheet(self.df_frame)
        sheet.enable_bindings()
        sheet.grid(row=0, column=0, sticky="nswe")

        # Insert data
        sheet.set_sheet_data(self.df.values.tolist())

if __name__ == '__main__':
    root = tk.Tk()
    app = NewprojectApp(root)
    app.run()
