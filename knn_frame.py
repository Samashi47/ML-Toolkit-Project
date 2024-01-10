import pickle
import tkinter as tk
import customtkinter as ctk
from sklearn.neighbors import KNeighborsClassifier
import  models_frame as mf
import ppframe as ppf
from tkinter import messagebox

class KnnFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent, fg_color='transparent', corner_radius=20)

        self.svm = ctk.CTkLabel(self, font=('Arial', 30), text="KNN")
        self.svm.place(anchor="center", relx=0.43, rely=0.07)

        # SVM Frame

        self.weights_label = ctk.CTkLabel(self, font=('Arial', 17), text="weights : ")
        self.weights_label.place(anchor="center", relx=0.15, rely=0.25)
        self.weights_optMenu = ctk.CTkOptionMenu(self, width=190, height=30, values=["uniform", "distance"])
        self.weights_optMenu.configure(fg_color="#200E3A")
        self.weights_optMenu.place(relx=0.3, rely=0.26, anchor="center")

        self.neighbors_label = ctk.CTkLabel(self, font=('Arial', 17), text="n_neighbors : ")
        self.neighbors_label.place(anchor="center", relx=0.15, rely=0.45)
        self.neighbors_entry = ctk.CTkEntry(self, width=190, height=30, placeholder_text="int >0 - default = 5")
        self.neighbors_entry.place(relx=0.30, rely=0.46, anchor="center")

        self.algorithm_label = ctk.CTkLabel(self, font=('Arial', 17), text="algorithm : ")
        self.algorithm_label.place(anchor="center", relx=0.15, rely=0.65)
        self.algorithm_optMenu = ctk.CTkOptionMenu(self, width=190, height=30, values=["auto", "ball_tree", "kd_tree", "brute"])
        self.algorithm_optMenu.configure(fg_color="#200E3A")
        self.algorithm_optMenu.place(relx=0.3, rely=0.66, anchor="center")

        self.p_label = ctk.CTkLabel(self, font=('Arial', 17), text="p : ")
        self.p_label.place(anchor="center", relx=0.51, rely=0.25)
        self.p_entry = ctk.CTkEntry(self, width=190, height=30, placeholder_text="float >0  - default = 2")
        self.p_entry.place(relx=0.65, rely=0.26, anchor="center")

        self.leaf_label = ctk.CTkLabel(self, font=('Arial', 17), text="leaf_size : ")
        self.leaf_label.place(anchor="center", relx=0.51, rely=0.45)
        self.leaf_entry = ctk.CTkEntry(self, width=190, height=30, placeholder_text="int >0 - default = 30 ")
        self.leaf_entry.place(relx=0.65, rely=0.46, anchor="center")

        self.jobs_label = ctk.CTkLabel(self, font=('Arial', 17), text="n_jobs : ")
        self.jobs_label.place(anchor="center", relx=0.51, rely=0.65)
        self.jobs_entry = ctk.CTkEntry(self, width=190, height=30, placeholder_text="int >0 - default = None")
        self.jobs_entry.place(relx=0.65, rely=0.66, anchor="center")

        self.import_file_button = ctk.CTkButton(master=self, text='Import...', width=170, height=45,
                                                command=lambda: self.controller.frames[ppf.PrePFrame].getFile())
        self.import_file_button.configure(fg_color="#200E3A")
        self.import_file_button.place(anchor="center", relx=0.93, rely=0.42)

        self.evaluateModel_button = ctk.CTkButton(master=self, text='Evaluate Model', width=170, height=45,
                                                  command=lambda: self.controller.frames[
                                                      mf.ModFrame].evaluateModel())
        self.evaluateModel_button.configure(fg_color="#200E3A")
        self.evaluateModel_button.place(anchor="center", relx=0.93, rely=0.57)

        self.SaveChanges_button = ctk.CTkButton(master=self, text='Save Model', width=170, height=45,
                                                command=lambda: self.saveModel())
        self.SaveChanges_button.configure(fg_color="#200E3A")
        self.SaveChanges_button.place(anchor="center", relx=0.93, rely=0.72)

        self.svm_button = ctk.CTkButton(master=self, text='Apply Knn ', font=('Arial', 15), width=400,
                                             height=40,
                                             command=lambda: self.applyKnn(str(self.weights_optMenu.get()),
                                                                            str(self.neighbors_entry.get()),
                                                                            str(self.algorithm_optMenu.get()),
                                                                            str(self.p_entry.get()),
                                                                            str(self.leaf_entry.get()),
                                                                            str(self.jobs_entry.get())
                                                                           ))
        self.svm_button.configure(fg_color="#200E3A")
        self.svm_button.place(anchor="center", relx=0.43, rely=0.9)


    def applyKnn(self,weig="uniform",neigh=5,algo="auto",p=2,leaf=30,jobs=None):
        x = self.controller.frames[ppf.PrePFrame].X_train
        if x is None:
            tk.messagebox.showerror('Python Error', "Splite the data first.")
            return

        if neigh == '':
            neigh = 5
        if p == '':
            p = 2
        if leaf == '':
            leaf = 30
        if jobs == '':
            jobs = None


        if isinstance(jobs, str) and jobs != 'None':
            try:
                jobs = int(jobs)
                if jobs < 0:
                    tk.messagebox.showerror('Python Error', " n_jobs  must be positif. ")
                    return
            except:
                tk.messagebox.showerror('Python Error', "n_jobs  must be an int or None.")
                return
        elif jobs == 'None':
            jobs = None

        if isinstance(p, str):
            try:
                p = float(p)
                if p<0:
                  tk.messagebox.showerror('Python Error', " P must be positif ")
                  return
            except:
                tk.messagebox.showerror('Python Error', " P must be an float ")
                return

        if isinstance(leaf, str):
            try:
                leaf = int(leaf)
                if leaf<0:
                  tk.messagebox.showerror('Python Error', " leaf_size must be positif ")
                  return

            except:
                tk.messagebox.showerror('Python Error', " leaf_size must be a positif int ")
                return

        if isinstance(neigh, str):
            try:
                neigh = int(neigh)
                if neigh<0:
                  tk.messagebox.showerror('Python Error', " n_neighbors must be positif ")
                  return
            except:
                tk.messagebox.showerror('Python Error', " n_neighbors must be an int ")
                return

        # Initialize the Knn classifier
        self.controller.frames[mf.ModFrame].model = KNeighborsClassifier(n_neighbors=neigh,algorithm=algo,p=p,n_jobs=jobs,leaf_size=leaf)

        self.controller.frames[mf.ModFrame].model.fit(self.controller.frames[ppf.PrePFrame].X_train,
                                                      self.controller.frames[ppf.PrePFrame].y_train)
        tk.messagebox.showinfo('Info', 'Training successful')

    def saveModel(self):
        if self.controller.frames[mf.ModFrame].model is None:
            tk.messagebox.showerror('Python Error', "Please train a model first.")
            return
        filename = tk.filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                                   filetypes=(("model files", "*.sav"), ("all files", "*.*")))
        if filename == '':
            return
        pickle.dump(self.controller.frames[mf.ModFrame].model, open(filename+'.sav', 'wb'))
        tk.messagebox.showinfo('Info', 'Model saved successfully')