import pickle
import tkinter as tk
import customtkinter as ctk
import modeling.models_frame as mf
import preprocessing.ppframe as ppf
from sklearn.linear_model import LogisticRegression

class LRFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent, fg_color='transparent', corner_radius=20)

        self.lr = ctk.CTkLabel(self, font=('Arial', 30), text="Logistic Regression")
        self.lr.place(anchor="center", relx=0.5, rely=0.08)
        
        self.penalty_label = ctk.CTkLabel(self,font=('Arial',17),text="penalty: ")
        self.penalty_label.place(anchor="center",relx=0.035, rely=0.2)
        self.penalty_optMenu = ctk.CTkOptionMenu(self, width=190, height=30,values=['l2', 'l1', 'elasticnet','None'],dynamic_resizing=True)
        self.penalty_optMenu.configure(fg_color="#200E3A")
        self.penalty_optMenu.place(relx=0.18, rely=0.21, anchor="center")
        
        self.dual_label = ctk.CTkLabel(self,font=('Arial',17),text="dual: ")
        self.dual_label.place(anchor="center",relx=0.025, rely=0.4)
        self.dual_optMenu = ctk.CTkOptionMenu(self, width=190, height=30,values=['False', 'True'],dynamic_resizing=True)
        self.dual_optMenu.configure(fg_color="#200E3A")
        self.dual_optMenu.place(relx=0.18, rely=0.41, anchor="center")
        
        self.tol_label = ctk.CTkLabel(self,font=('Arial',17),text="tol: ")
        self.tol_label.place(anchor="center",relx=0.02, rely=0.6)
        self.tol_entry = ctk.CTkEntry(self, width=190, height=30, placeholder_text="float, default=1e-4")
        self.tol_entry.place(relx=0.18, rely=0.61, anchor="center")
        
        self.randomstate_label = ctk.CTkLabel(self,font=('Arial',17),text="random_state: ")
        self.randomstate_label.place(anchor="center",relx=0.047, rely=0.8)
        self.randomstate_entry = ctk.CTkEntry(self, width=190, height=30, placeholder_text="int, default=None")
        self.randomstate_entry.place(relx=0.18, rely=0.81, anchor="center")
        
        self.c_label = ctk.CTkLabel(self,font=('Arial',17),text="C: ")
        self.c_label.place(anchor="center",relx=0.29, rely=0.2)
        self.c_entry = ctk.CTkEntry(self, width=190, height=30, placeholder_text="float, default=1.0")
        self.c_entry.place(relx=0.51, rely=0.21, anchor="center")
        
        self.fitintercept_label = ctk.CTkLabel(self,font=('Arial',17),text="fit_intercept: ")
        self.fitintercept_label.place(anchor="center",relx=0.32, rely=0.4)
        self.fitintercept_optMenu = ctk.CTkOptionMenu(self, width=190, height=30,values=['True', 'False'],dynamic_resizing=True)
        self.fitintercept_optMenu.configure(fg_color="#200E3A")
        self.fitintercept_optMenu.place(relx=0.51, rely=0.41, anchor="center")
        
        self.intercept_scaling_label = ctk.CTkLabel(self,font=('Arial',17),text="intercept_scaling: ")
        self.intercept_scaling_label.place(anchor="center",relx=0.33, rely=0.6)
        self.intercept_scaling_entry = ctk.CTkEntry(self, width=190, height=30, placeholder_text="float, default=1")
        self.intercept_scaling_entry.place(relx=0.51, rely=0.61, anchor="center")
        
        self.multiclass_label = ctk.CTkLabel(self,font=('Arial',17),text="multi_class: ")
        self.multiclass_label.place(anchor="center",relx=0.315, rely=0.8)
        self.multiclass_optMenu = ctk.CTkOptionMenu(self, width=190, height=30,values=['auto', 'ovr','multinomial'],dynamic_resizing=True)
        self.multiclass_optMenu.configure(fg_color="#200E3A")
        self.multiclass_optMenu.place(relx=0.51, rely=0.81, anchor="center")
        
        self.class_weight_label = ctk.CTkLabel(self,font=('Arial',17),text="class_weight: ")
        self.class_weight_label.place(anchor="center",relx=0.642, rely=0.2)
        self.class_weight_optMenu = ctk.CTkOptionMenu(self, width=190, height=30,values=['None','balanced'],dynamic_resizing=True)
        self.class_weight_optMenu.configure(fg_color="#200E3A")
        self.class_weight_optMenu.place(relx=0.78, rely=0.21, anchor="center")
        
        self.solver_label = ctk.CTkLabel(self,font=('Arial',17),text="solver: ")
        self.solver_label.place(anchor="center",relx=0.625, rely=0.4)
        self.solver_optMenu = ctk.CTkOptionMenu(self, width=190, height=30,values=['lbfgs','liblinear','newton-cg','newton-cholesky','sag','saga'],dynamic_resizing=True)
        self.solver_optMenu.configure(fg_color="#200E3A")
        self.solver_optMenu.place(relx=0.78, rely=0.41, anchor="center")
        
        self.maxi_iter_label = ctk.CTkLabel(self,font=('Arial',17),text="max_iter: ")
        self.maxi_iter_label.place(anchor="center",relx=0.63, rely=0.6)
        self.maxi_iter_entry = ctk.CTkEntry(self, width=190, height=30, placeholder_text="int, default=100")
        self.maxi_iter_entry.place(relx=0.78, rely=0.61, anchor="center")
        
        self.warm_start_label = ctk.CTkLabel(self,font=('Arial',17),text="warm_start: ")
        self.warm_start_label.place(anchor="center",relx=0.635, rely=0.8)
        self.warm_start_optMenu = ctk.CTkOptionMenu(self, width=190, height=30,values=['False','True'],dynamic_resizing=True)
        self.warm_start_optMenu.configure(fg_color="#200E3A")
        self.warm_start_optMenu.place(relx=0.78, rely=0.81, anchor="center")
        
        self.train_button = ctk.CTkButton(master=self, text='Train', font=('Arial', 15), width=300, height=35,
                                          command=lambda:self.trainLR(str(self.penalty_optMenu.get()),
                                                                      str(self.dual_optMenu.get()),
                                                                      str(self.tol_entry.get()),
                                                                      str(self.c_entry.get()),
                                                                      str(self.fitintercept_optMenu.get()),
                                                                      str(self.intercept_scaling_entry.get()),
                                                                      str(self.class_weight_optMenu.get()),
                                                                      str(self.randomstate_entry.get()),
                                                                      str(self.solver_optMenu.get()),
                                                                      str(self.maxi_iter_entry.get()),
                                                                      str(self.multiclass_optMenu.get()),
                                                                      str(self.warm_start_optMenu.get())
                                                                      ))
        self.train_button.configure(fg_color="#200E3A")
        self.train_button.place(anchor="center", relx=0.5, rely=0.94)
        
        self.import_file_button = ctk.CTkButton(master=self, text='Import...', width=170, height=45,command=lambda:self.controller.frames[ppf.PrePFrame].getFile())
        self.import_file_button.configure(fg_color="#200E3A")
        self.import_file_button.place(anchor="center", relx=0.93, rely=0.42)
        
        self.evaluateModel_button = ctk.CTkButton(master=self,text='Evaluate Model',width=170,height=45,command=lambda:self.controller.frames[mf.ModelsFrame].evaluateModel())
        self.evaluateModel_button.configure(fg_color="#200E3A")
        self.evaluateModel_button.place(anchor="center",relx=0.93, rely=0.57)
        
        self.SaveChanges_button = ctk.CTkButton(master=self,text='Save Model',width=170,height=45,command=lambda:self.saveModel())
        self.SaveChanges_button.configure(fg_color="#200E3A")
        self.SaveChanges_button.place(anchor="center",relx=0.93, rely=0.72)
        
    def trainLR(self, penalty, dual, tol, c, fit_intercept, intercept_scaling, class_weight, random_state, solver, max_iter, multi_class, warm_start):
        if self.controller.frames[ppf.PrePFrame].df is None:
            tk.messagebox.showerror('Python Error', "Please import a file first.")
            return
        if self.controller.frames[ppf.PrePFrame].X_train is None or self.controller.frames[ppf.PrePFrame].y_train is None:
            tk.messagebox.showerror('Python Error', "Please run train test split first.")
            return
        
        if any(self.controller.frames[ppf.PrePFrame].X_test.dtypes == object):
            tk.messagebox.showerror('Python Error', "Categorical columns represented as strings are not supported. Please convert them to numerical values.")
            return
        if penalty == 'None':
            penalty = None
        if dual == 'False':
            dual = False
        elif dual == 'True':
            dual = True
        if fit_intercept == 'False':
            fit_intercept = False
        elif fit_intercept == 'True':
            fit_intercept = True
        if class_weight == 'None':
            class_weight = None
        if warm_start == 'False':
            warm_start = False
        elif warm_start == 'True':
            warm_start = True
            
        if tol == '':
            tol = 1e-4
        elif isinstance(tol, str):
            try:
                tol = float(tol)
            except:
                tk.messagebox.showerror('Python Error', "tol must be a float.")
                return
            
        if c == '':
            c = 1.0
        elif isinstance(c, str):
            try:
                c = float(c)
            except:
                tk.messagebox.showerror('Python Error', "C must be a float.")
                return
        if intercept_scaling == '':
            intercept_scaling = 1
        elif isinstance(intercept_scaling, str):
            try:
                intercept_scaling = float(intercept_scaling)
            except:
                tk.messagebox.showerror('Python Error', "intercept_scaling must be a float.")
                return
        if random_state == '':
            random_state = None
        elif random_state == 'None':
            random_state = None
        elif isinstance(random_state, str):
            try:
                random_state = int(random_state)
            except:
                tk.messagebox.showerror('Python Error', "random_state must be an integer.")
                return
        if max_iter == '':
            max_iter = 100
        elif isinstance(max_iter, str):
            try:
                max_iter = int(max_iter)
            except:
                tk.messagebox.showerror('Python Error', "max_iter must be an integer.")
                return
        
        if tol < 0:
            tk.messagebox.showerror('Python Error', "tol must be >= 0.")
            return
        if c <= 0:
            tk.messagebox.showerror('Python Error', "C must be > 0.")
            return
        if intercept_scaling <= 0:
            tk.messagebox.showerror('Python Error', "intercept_scaling must be > 0.")
            return
        if max_iter <= 0:
            tk.messagebox.showerror('Python Error', "max_iter must be > 0.")
            return
        
        
        self.controller.frames[mf.ModelsFrame].model = LogisticRegression(penalty=penalty, dual=dual, tol=tol, C=c, fit_intercept=fit_intercept, intercept_scaling=intercept_scaling, class_weight=class_weight, random_state=random_state,solver=solver,max_iter=max_iter,multi_class=multi_class,warm_start=warm_start,l1_ratio=None)
        
        try:
            self.controller.frames[mf.ModelsFrame].model.fit(self.controller.frames[ppf.PrePFrame].X_train, self.controller.frames[ppf.PrePFrame].y_train)
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