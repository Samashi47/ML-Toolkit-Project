import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd
from tksheet import Sheet
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

class NewprojectApp:
    def __init__(self, master=None):
        # build ui
        main_window = ttk.Frame(master)
        button_frame = ttk.Frame(main_window)
        button_frame.pack(side='top')

        button_1 = ttk.Button(button_frame)
        button_1.config(text='Import File', command=self.getCSV)
        button_1.grid(row=0, column=0, padx=5, pady=10)

        button_2 = ttk.Button(button_frame)
        button_2.config(text='Show File', command=self.show)
        button_2.grid(row=0, column=1, padx=5, pady=10)

        button_3 = ttk.Button(button_frame)
        button_3.config(text='Split Data', command=self.splitData)
        button_3.grid(row=1, column=0, padx=5, pady=10)

        button_4 = ttk.Button(button_frame)
        button_4.config(text='Show X_train', command=lambda: self.showDataFrame(self.X_train))
        button_4.grid(row=1, column=1, padx=5, pady=10)

        button_5 = ttk.Button(button_frame)
        button_5.config(text='Show X_test', command=lambda: self.showDataFrame(self.X_test))
        button_5.grid(row=2, column=0, padx=5, pady=10)

        button_6 = ttk.Button(button_frame)
        button_6.config(text='Show y_train', command=lambda: self.showDataFrame(self.y_train))
        button_6.grid(row=2, column=1, padx=5, pady=10)

        button_7 = ttk.Button(button_frame)
        button_7.config(text='Show y_test', command=lambda: self.showDataFrame(self.y_test))
        button_7.grid(row=3, column=0, padx=5, pady=10)

        button_8 = ttk.Button(button_frame)
        button_8.config(text='Apply SMOTE', command=self.applySMOTE)
        button_8.grid(row=3, column=1, padx=5, pady=10)




        # Frame to hold DataFrame
        self.df_frame = ttk.Frame(main_window)
        self.df_frame.pack(side='top', pady=10)

        main_window.config(height='800', width='800')  # Adjusted size
        main_window.pack(side='top')

        # Main widget
        self.mainwindow = main_window
        self.df = None  # Initialize df as an instance variable
        self.X_train, self.X_test, self.y_train, self.y_test = None, None, None, None

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

        # # Call splitData after importing the CSV file
        # self.splitData()

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

    def showDataFrame(self, data):
        if data is None or (isinstance(data, pd.DataFrame) and data.empty):
            print("No data to display.")
            return
        # Clear previous DataFrame display
        for widget in self.df_frame.winfo_children():
            widget.destroy()

        # Display DataFrame using tksheet
        if isinstance(data, pd.Series):
            data = data.to_frame()

        sheet = Sheet(self.df_frame, data=data.values.tolist(), headers=data.columns.tolist())
        sheet.enable_bindings()
        sheet.grid(row=0, column=0, sticky="nswe")
        
    def splitData(self):
        if self.df is None:
            print("Please import a file first.")
            return

        # Assuming the target variable is in the last column
        X = self.df.iloc[:, :-1]
        y = self.df.iloc[:, -1]

        # Encode categorical variables if present
        le = LabelEncoder()
        for col in X.select_dtypes(include=['object']).columns:
            X[col] = le.fit_transform(X[col])

        # Split data into training and testing sets
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Convert float values in y_train and y_test to integers
        self.y_train = self.y_train.astype(int)
        self.y_test = self.y_test.astype(int)

        print("Data Split Successfully!")
        print("X_train shape:", self.X_train.shape)
        print("X_test shape:", self.X_test.shape)
        print("y_train shape:", self.y_train.shape)
        print("y_test shape:", self.y_test.shape)

        
    def applySMOTE(self):
        if self.X_train is None or self.y_train is None:
            print("Please import and split data first.")
            return

        # Apply SMOTE to balance the classes
        smote = SMOTE(sampling_strategy=0.5,random_state=42)
        X_train_resampled, y_train_resampled = smote.fit_resample(self.X_train, self.y_train)

        # Update X_train and y_train with resampled data
        self.X_train = pd.DataFrame(X_train_resampled, columns=self.X_train.columns)
        self.y_train = pd.Series(y_train_resampled, name=self.y_train.name)
        print("Shape of X_train after SMOTE is :", self.X_train.shape)
        print("Shape of y_train after SMOTE is :", self.y_train.shape)
        print("SMOTE applied successfully.")


if __name__ == '__main__':
    root = tk.Tk()
    app = NewprojectApp(root)
    app.run()