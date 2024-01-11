import pickle
import tkinter as tk
import customtkinter as ctk
import  modeling.models_frame as mf
import preprocessing.ppframe as ppf
from sklearn.svm import SVC


class SvmFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent, fg_color='transparent', corner_radius=20)

        self.svm = ctk.CTkLabel(self, font=('Arial', 30), text="SVM")
        self.svm.place(anchor="center", relx=0.5, rely=0.08)

        # SVM Frame

        self.ker_label = ctk.CTkLabel(self, font=('Arial', 17), text="kernel : ")
        self.ker_label.place(anchor="center", relx=0.15, rely=0.25)
        self.ker_optMenu = ctk.CTkOptionMenu(self, width=190, height=30, values=["rbf", "linear", "sigmoid","precomputed","poly"])
        self.ker_optMenu.configure(fg_color="#200E3A")
        self.ker_optMenu.place(relx=0.3, rely=0.26, anchor="center")

        self.RandS_label = ctk.CTkLabel(self, font=('Arial', 17), text="Random state : ")
        self.RandS_label.place(anchor="center", relx=0.15, rely=0.45)
        self.RandS_entry = ctk.CTkEntry(self, width=190, height=30, placeholder_text="int - default = None")
        self.RandS_entry.place(relx=0.30, rely=0.46, anchor="center")

        self.C_label = ctk.CTkLabel(self, font=('Arial', 17), text="C : ")
        self.C_label.place(anchor="center", relx=0.15, rely=0.65)
        self.C_entry = ctk.CTkEntry(self, width=190, height=30, placeholder_text="float - default = 1.0")
        self.C_entry.place(relx=0.30, rely=0.66, anchor="center")

        self.degree_label = ctk.CTkLabel(self, font=('Arial', 17), text="Degree : ")
        self.degree_label.place(anchor="center", relx=0.51, rely=0.25)
        self.degree_entry = ctk.CTkEntry(self, width=190, height=30, placeholder_text="int - default = 3")
        self.degree_entry.place(relx=0.65, rely=0.26, anchor="center")

        self.gamma_label = ctk.CTkLabel(self, font=('Arial', 17), text="Gamma : ")
        self.gamma_label.place(anchor="center", relx=0.51, rely=0.45)
        self.gamma_entry = ctk.CTkEntry(self, width=190, height=30, placeholder_text="float - default = scale ")
        self.gamma_entry.place(relx=0.65, rely=0.46, anchor="center")

        self.iter_label = ctk.CTkLabel(self, font=('Arial', 17), text="max_iter : ")
        self.iter_label.place(anchor="center", relx=0.51, rely=0.65)
        self.iter_entry = ctk.CTkEntry(self, width=190, height=30, placeholder_text="int >0 - default = -1")
        self.iter_entry.place(relx=0.65, rely=0.66, anchor="center")

        self.import_file_button = ctk.CTkButton(master=self, text='Import...', width=170, height=45,
                                                command=lambda: self.controller.frames[ppf.PrePFrame].getFile())
        self.import_file_button.configure(fg_color="#200E3A")
        self.import_file_button.place(anchor="center", relx=0.93, rely=0.42)

        self.evaluateModel_button = ctk.CTkButton(master=self, text='Evaluate Model', width=170, height=45,
                                                  command=lambda: self.controller.frames[
                                                      mf.ModelsFrame].evaluateModel())
        self.evaluateModel_button.configure(fg_color="#200E3A")
        self.evaluateModel_button.place(anchor="center", relx=0.93, rely=0.57)

        self.SaveChanges_button = ctk.CTkButton(master=self, text='Save Model', width=170, height=45,
                                                command=lambda: self.saveModel())
        self.SaveChanges_button.configure(fg_color="#200E3A")
        self.SaveChanges_button.place(anchor="center", relx=0.93, rely=0.72)

        self.svm_button = ctk.CTkButton(master=self, text='Train', font=('Arial', 15), width=400,
                                             height=40,
                                             command=lambda: self.applySVM(str(self.ker_optMenu.get()),
                                                                            str(self.RandS_entry.get()),
                                                                            str(self.C_entry.get()),
                                                                            str(self.degree_entry.get()),
                                                                            str(self.gamma_entry.get()),
                                                                            str(self.iter_entry.get())
                                                                           ))
        self.svm_button.configure(fg_color="#200E3A")
        self.svm_button.place(anchor="center", relx=0.5, rely=0.94)


    def applySVM(self,ker="rbf",random=None,c=1.0,deg=3,gam="scale",iter=-1):
        
        if self.controller.frames[ppf.PrePFrame].df is None:
            tk.messagebox.showerror('Python Error', "Please import a file first.")
            return
        
        if self.controller.frames[ppf.PrePFrame].X_train is None or self.controller.frames[ppf.PrePFrame].y_train is None:
            tk.messagebox.showerror('Python Error', "Please run train test split first.")
            return

        if any(self.controller.frames[ppf.PrePFrame].X_test.dtypes == object):
            tk.messagebox.showerror('Python Error', "Categorical columns represented as strings are not supported. Please convert them to numerical values.")
            return
        
        if random == '':
            random = None
        if c == '':
            c = 1.0
        if deg == '':
            deg = 3
        if gam == '':
            gam = "scale"
        if iter == '':
            iter = -1

        if isinstance(random, str) and random != 'None':
            try:
                random = int(random)
                if random < 0:
                    tk.messagebox.showerror('Python Error', " Random state must be positif. ")
                    return
            except:
                tk.messagebox.showerror('Python Error', "Random state must be an int or None.")
                return
        elif random == 'None':
            random = None

        if isinstance(c, str):
            try:
                c = float(c)
                if c<0:
                  tk.messagebox.showerror('Python Error', " C must be positif ")
                  return
            except:
                tk.messagebox.showerror('Python Error', " C must be an float ")
                return

        if isinstance(iter, str):
            try:
                iter = int(iter)
                if iter<0:
                  tk.messagebox.showerror('Python Error', " max-iter must be positif ")
                  return

            except:
                tk.messagebox.showerror('Python Error', " max-iter must be a positif int ")
                return

        if isinstance(deg, str):
            try:
                deg = int(deg)
                if deg<0:
                  tk.messagebox.showerror('Python Error', " Degree must be positif ")
                  return
            except:
                tk.messagebox.showerror('Python Error', " Degree must be an int ")
                return

        if isinstance(gam, str) and gam != "scale":
            try:
                gam = int(gam)
                if gam<0:
                  tk.messagebox.showerror('Python Error', " gamma must be positif ")
                  return
            except:
                tk.messagebox.showerror('Python Error', " Gamma must be an int ")
                return
        elif gam == 'scale':
            gam = 'scale'

        self.controller.frames[mf.ModelsFrame].model = SVC(kernel=ker,random_state=random,gamma=gam,C=c,max_iter=iter,degree=deg,probability=True)  # You can change the kernel as needed (linear, rbf, etc.)
        try:
        # Initialize the SVM classifier
            self.controller.frames[mf.ModelsFrame].model.fit(self.controller.frames[ppf.PrePFrame].X_train, self.controller.frames[ppf.PrePFrame].y_train)
            tk.messagebox.showinfo('Info', 'Training successful')
            return
        except ValueError as e:
            tk.messagebox.showerror('Python Error', str(e))
            return
        # Train the SVM model

    def saveModel(self):
        if self.controller.frames[mf.ModelsFrame].model is None:
            tk.messagebox.showerror('Python Error', "Please train a model first.")
            return
        filename = tk.filedialog.asksaveasfilename(initialdir="/", title="Select file", filetypes=(("model files", "*.sav"), ("all files", "*.*")))
        if filename == '':
            return
        pickle.dump(self.controller.frames[mf.ModelsFrame].model, open(filename+'.sav', 'wb'))
        tk.messagebox.showinfo('Info', 'Model saved successfully')