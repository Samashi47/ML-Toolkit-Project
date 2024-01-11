import pickle
import tkinter as tk
import customtkinter as ctk
import  modeling.models_frame as mf
import preprocessing.ppframe as ppf
from sklearn.naive_bayes import MultinomialNB,GaussianNB
from tkinter import messagebox


class NbFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent, fg_color='transparent', corner_radius=20)


        self.sepv = tk.ttk.Separator(self, orient='vertical', style='TSeparator')
        self.sepv.place(relx=0.40, rely=0.01, height=720, bordermode="outside")

        # Gaussian Naive Bayes Frame

        self.gaus_label = ctk.CTkLabel(self, font=('Arial', 30), text="Gaussian Naive Bayes ")
        self.gaus_label.place(anchor="center", relx=0.18, rely=0.3)
        self.smooth_label = ctk.CTkLabel(self, font=('Arial', 17), text="var_smoothing : ")
        self.smooth_label.place(anchor="center",relx=0.095, rely=0.5)
        self.smooth_entry = ctk.CTkEntry(self, width=190, height=30, placeholder_text="float - default = 1e-9")
        self.smooth_entry.place(relx=0.23, rely=0.51, anchor="center")
        self.nbg_button = ctk.CTkButton(master=self, text='Train GNB', font=('Arial', 15), width=190,
                                             height=40,
                                             command=lambda: self.applyNbg( str(self.smooth_entry.get())))
        self.nbg_button.configure(fg_color="#200E3A")
        self.nbg_button.place(anchor="center",relx=0.18, rely=0.72)

        # Multinomial Naive Bayes Frame

        self.mult_label = ctk.CTkLabel(self,font=('Arial',30),text="Multinomial Naive Bayes")
        self.mult_label.place(anchor="center",relx=0.64, rely=0.3)
        self.alpha_label = ctk.CTkLabel(self,font=('Arial',17),text="alpha : ")
        self.alpha_label.place(anchor="center",relx=0.47, rely=0.5)
        self.alpha_entry = ctk.CTkEntry(self,width=190,height=30,placeholder_text="float - default = 1.0")
        self.alpha_entry.place(relx=0.57, rely=0.51, anchor="center")
        self.prior_label = ctk.CTkLabel(self,font=('Arial',17),text="fit_prior: ")
        self.prior_label.place(anchor="center",relx=0.69, rely=0.5)
        self.prior_OptMenu = ctk.CTkOptionMenu(self,width=120,height=30,values=["True","False"])
        self.prior_OptMenu.configure(fg_color="#200E3A")
        self.prior_OptMenu.place(relx=0.78, rely=0.51, anchor="center")

        self.nbm_button = ctk.CTkButton(master=self, text='Train MNB', font=('Arial', 15), width=190,
                                        height=40,
                                        command=lambda: self.applyNbm(str(self.alpha_entry.get()),
                                                                      str(self.prior_OptMenu.get())
                                                                      ))
        self.nbm_button.configure(fg_color="#200E3A")
        self.nbm_button.place(anchor="center", relx=0.64, rely=0.72)


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


    def applyNbg(self,smooth=1e-9):
        if self.controller.frames[ppf.PrePFrame].df is None:
            tk.messagebox.showerror('Python Error', "Please import a file first.")
            return
        if self.controller.frames[ppf.PrePFrame].X_train is None or self.controller.frames[ppf.PrePFrame].y_train is None:
            tk.messagebox.showerror('Python Error', "Please run train test split first.")
            return
        if smooth == '':
            smooth = 1e-9

        if isinstance(smooth, str):
            try:
                smooth = float(smooth)
                if smooth<0:
                  tk.messagebox.showerror('Python Error', "var_smoothing must be positif ")
                  return
            except:
                tk.messagebox.showerror('Python Error', " var_smoothing must be an float ")
                return

        # Initialiser le classificateur
        self.controller.frames[mf.ModelsFrame].model = GaussianNB(var_smoothing=smooth)
        # Entraîner le modèle
        self.controller.frames[mf.ModelsFrame].model.fit(self.controller.frames[ppf.PrePFrame].X_train,
                                                       self.controller.frames[ppf.PrePFrame].y_train)
        tk.messagebox.showinfo('Info', 'Training successful')



    def applyNbm(self,alp=1.0,pri="True"):
        if self.controller.frames[ppf.PrePFrame].df is None:
            tk.messagebox.showerror('Python Error', "Please import a file first.")
            return
        if self.controller.frames[ppf.PrePFrame].X_train is None or self.controller.frames[ppf.PrePFrame].y_train is None:
            tk.messagebox.showerror('Python Error', "Please run train test split first.")
            return
        
        if any(self.controller.frames[ppf.PrePFrame].X_test.dtypes == object):
            tk.messagebox.showerror('Python Error', "Categorical columns represented as strings are not supported. Please convert them to numerical values.")
            return
        
        if alp =='':
            alp =1.0

        if isinstance(alp, str):
            try:
                alp = float(alp)
                if alp<0:
                    tk.messagebox.showerror('Python Error', "Alpha must be positive ")
                    return
            except:
                tk.messagebox.showerror('Python Error', " Alpha must be a float ")
                return

        pri = True if pri.lower() == 'true' else False

        # Check for negative values in input data
        if (self.controller.frames[ppf.PrePFrame].X_train < 0).any().any():
            tk.messagebox.showerror('Python Error', "Negative values in data passed to MultinomialNB")
            return
        self.controller.frames[mf.ModelsFrame].model = MultinomialNB(alpha=alp, fit_prior=pri)
        try:
            self.controller.frames[mf.ModelsFrame].model.fit(self.controller.frames[ppf.PrePFrame].X_train,self.controller.frames[ppf.PrePFrame].y_train)
            tk.messagebox.showinfo('Info', 'Training successful')
            return
        except ValueError as e:
            tk.messagebox.showerror('Python Error', str(e))
            return
        


    def saveModel(self):
        if self.controller.frames[mf.ModelsFrame].model is None:
            tk.messagebox.showerror('Python Error', "Please train a model first.")
            return
        filename = tk.filedialog.asksaveasfilename(initialdir="/", title="Select file", filetypes=(("model files", "*.sav"), ("all files", "*.*")))
        if filename == '':
            return
        pickle.dump(self.controller.frames[mf.ModelsFrame].model, open(filename+'.sav', 'wb'))
        tk.messagebox.showinfo('Info', 'Model saved successfully')