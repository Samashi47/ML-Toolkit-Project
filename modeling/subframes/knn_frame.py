import pickle
import tkinter as tk
import customtkinter as ctk
from sklearn.neighbors import KNeighborsClassifier
import  modeling.models_frame as mf
import preprocessing.ppframe as ppf

class KnnFrame(ctk.CTkFrame):
    """
    A custom frame for KNN (K-Nearest Neighbors) model configuration.

    Args:
        parent: The parent widget.
        controller: The controller object.

    Attributes:
        knn: The label widget displaying "KNN".
        weights_label: The label widget for selecting the weight type.
        weights_optMenu: The option menu widget for selecting the weight type.
        neighbors_label: The label widget for entering the number of neighbors.
        neighbors_entry: The entry widget for entering the number of neighbors.
        algorithm_label: The label widget for selecting the algorithm.
        algorithm_optMenu: The option menu widget for selecting the algorithm.
        p_label: The label widget for entering the p value.
        p_entry: The entry widget for entering the p value.
        leaf_label: The label widget for entering the leaf size.
        leaf_entry: The entry widget for entering the leaf size.
        jobs_label: The label widget for entering the number of jobs.
        jobs_entry: The entry widget for entering the number of jobs.
        import_file_button: The button widget for importing a file.
        evaluateModel_button: The button widget for evaluating the model.
        SaveChanges_button: The button widget for saving the model.
        knn_button: The button widget for training the model.

    Methods:
        applyKnn: Applies the KNN algorithm with the specified parameters.
        saveModel: Saves the trained model to a file.
    """
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent, fg_color='transparent', corner_radius=20)

        self.knn = ctk.CTkLabel(self, font=('Arial', 30), text="KNN")
        self.knn.place(anchor="center", relx=0.5, rely=0.08)

        # KNN Frame

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
                                                      mf.ModelsFrame].evaluateModel())
        self.evaluateModel_button.configure(fg_color="#200E3A")
        self.evaluateModel_button.place(anchor="center", relx=0.93, rely=0.57)

        self.SaveChanges_button = ctk.CTkButton(master=self, text='Save Model', width=170, height=45,
                                                command=lambda: self.saveModel())
        self.SaveChanges_button.configure(fg_color="#200E3A")
        self.SaveChanges_button.place(anchor="center", relx=0.93, rely=0.72)

        self.knn_button = ctk.CTkButton(master=self, text='Train', font=('Arial', 15), width=400,
                                             height=40,
                                             command=lambda: self.applyKnn(str(self.weights_optMenu.get()),
                                                                            str(self.neighbors_entry.get()),
                                                                            str(self.algorithm_optMenu.get()),
                                                                            str(self.p_entry.get()),
                                                                            str(self.leaf_entry.get()),
                                                                            str(self.jobs_entry.get())
                                                                           ))
        self.knn_button.configure(fg_color="#200E3A")
        self.knn_button.place(anchor="center", relx=0.5, rely=0.94)


    def applyKnn(self,weig="uniform",neigh=5,algo="auto",p=2,leaf=30,jobs=None):
        """
        Applies the K-nearest neighbors algorithm to the data.

        Args:
            weig (str, optional): Weight function used in prediction. Defaults to "uniform".
            neigh (int, optional): Number of neighbors to use. Defaults to 5.
            algo (str, optional): Algorithm used to compute the nearest neighbors. Defaults to "auto".
            p (int, optional): Power parameter for the Minkowski metric. Defaults to 2.
            leaf (int, optional): Leaf size passed to BallTree or KDTree. Defaults to 30.
            jobs (int or None, optional): Number of parallel jobs to run for neighbors search. Defaults to None.

        Returns:
            None
        """
        if self.controller.frames[ppf.PrePFrame].df is None:
            tk.messagebox.showerror('Python Error', "Please import a file first.")
            return
        
        if self.controller.frames[ppf.PrePFrame].X_train is None or self.controller.frames[ppf.PrePFrame].y_train is None:
            tk.messagebox.showerror('Python Error', "Split the data first.")
            return

        if any(self.controller.frames[ppf.PrePFrame].X_test.dtypes == object):
            tk.messagebox.showerror('Python Error', "Categorical columns represented as strings are not supported. Please convert them to numerical values.")
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
        self.controller.frames[mf.ModelsFrame].model = KNeighborsClassifier(n_neighbors=neigh,algorithm=algo,p=p,n_jobs=jobs,leaf_size=leaf)
        try:
            self.controller.frames[mf.ModelsFrame].model.fit(self.controller.frames[ppf.PrePFrame].X_train,
                                                      self.controller.frames[ppf.PrePFrame].y_train)
            tk.messagebox.showinfo('Info', 'Training successful')
            return
        except ValueError as e:
            tk.messagebox.showerror('Python Error', str(e))
            return
            

    def saveModel(self):
        if self.controller.frames[mf.ModelsFrame].model is None:
            tk.messagebox.showerror('Python Error', "Please train a model first.")
            return
        filename = tk.filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                                   filetypes=(("model files", "*.sav"), ("all files", "*.*")))
        if filename == '':
            return
        pickle.dump(self.controller.frames[mf.ModelsFrame].model, open(filename+'.sav', 'wb'))
        tk.messagebox.showinfo('Info', 'Model saved successfully')