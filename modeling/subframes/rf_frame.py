import pickle
import tkinter as tk
import customtkinter as ctk
import modeling.models_frame as mf
import preprocessing.ppframe as ppf
from sklearn.ensemble import RandomForestClassifier

class RfFrame(ctk.CTkFrame):
    """
    A custom frame for Random Forest model configuration and training.

    Args:
        parent: The parent widget.
        controller: The controller object.

    Attributes:
        controller: The controller object.
        rf: The label widget for displaying the title.
        Criterion_label: The label widget for displaying the criterion option.
        Criterion_optMenu: The option menu widget for selecting the criterion.
        RandS_label: The label widget for displaying the random state option.
        RandS_entry: The entry widget for entering the random state value.
        depth_label: The label widget for displaying the max depth option.
        depth_entry: The entry widget for entering the max depth value.
        ssplit_label: The label widget for displaying the min samples split option.
        ssplit_entry: The entry widget for entering the min samples split value.
        n_est_label: The label widget for displaying the number of estimators option.
        n_est_entry: The entry widget for entering the number of estimators value.
        bootstrap_label: The label widget for displaying the bootstrap option.
        bootstrap_optMenu: The option menu widget for selecting the bootstrap option.
        import_file_button: The button widget for importing a file.
        evaluateModel_button: The button widget for evaluating the model.
        SaveChanges_button: The button widget for saving the model.
        rf_button: The button widget for training the model.

    Methods:
        applyRf: Applies the Random Forest model with the specified parameters.
        saveModel: Saves the trained model to a file.
    """
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent, fg_color='transparent', corner_radius=20)

        self.rf = ctk.CTkLabel(self, font=('Arial', 30), text="Random Forest")
        self.rf.place(anchor="center", relx=0.5, rely=0.08)

        # k-means Frame

        self.Criterion_label = ctk.CTkLabel(self, font=('Arial', 17), text="Criterion : ")
        self.Criterion_label.place(anchor="center", relx=0.15, rely=0.25)
        self.Criterion_optMenu = ctk.CTkOptionMenu(self, width=190, height=30,values=["gini", "entropy", "log_loss"])
        self.Criterion_optMenu.configure(fg_color="#200E3A")
        self.Criterion_optMenu.place(relx=0.30, rely=0.26, anchor="center")

        self.RandS_label = ctk.CTkLabel(self, font=('Arial', 17), text="Random state : ")
        self.RandS_label.place(anchor="center", relx=0.15, rely=0.45)
        self.RandS_entry = ctk.CTkEntry(self, width=190, height=30, placeholder_text="int - default = None")
        self.RandS_entry.place(relx=0.30, rely=0.46, anchor="center")

        self.depth_label = ctk.CTkLabel(self, font=('Arial', 17), text="max_depth : ")
        self.depth_label.place(anchor="center", relx=0.15, rely=0.65)
        self.depth_entry = ctk.CTkEntry(self, width=190, height=30, placeholder_text="int - default = None")
        self.depth_entry.place(relx=0.30, rely=0.66, anchor="center")

        self.ssplit_label = ctk.CTkLabel(self, font=('Arial', 17), text="min_samples_split : ")
        self.ssplit_label.place(anchor="center", relx=0.51, rely=0.25)
        self.ssplit_entry = ctk.CTkEntry(self, width=190, height=30, placeholder_text="int/float - default = 2")
        self.ssplit_entry.place(relx=0.65, rely=0.26, anchor="center")

        self.n_est_label = ctk.CTkLabel(self, font=('Arial', 17), text="n_estimators : ")
        self.n_est_label.place(anchor="center", relx=0.51, rely=0.45)
        self.n_est_entry = ctk.CTkEntry(self, width=190, height=30, placeholder_text="int - default = 100")
        self.n_est_entry.place(relx=0.65, rely=0.46, anchor="center")

        self.bootstrap_label = ctk.CTkLabel(self, font=('Arial', 17), text="bootstrap : ")
        self.bootstrap_label.place(anchor="center", relx=0.51, rely=0.65)
        self.bootstrap_optMenu = ctk.CTkOptionMenu(self, width=190, height=30, values=["True", "False"])
        self.bootstrap_optMenu.configure(fg_color="#200E3A")
        self.bootstrap_optMenu.place(relx=0.65, rely=0.66, anchor="center")

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

        self.rf_button = ctk.CTkButton(master=self, text='Train', font=('Arial', 15), width=400,
                                             height=40,
                                             command=lambda: self.applyRf(str(self.Criterion_optMenu.get()),
                                                                                str(self.RandS_entry.get()),
                                                                                str(self.depth_entry.get()),
                                                                                str(self.ssplit_entry.get()),
                                                                                str(self.n_est_entry.get()),
                                                                                str(self.bootstrap_optMenu.get()),
                                                                                ))
        self.rf_button.configure(fg_color="#200E3A")
        self.rf_button.place(anchor="center", relx=0.5, rely=0.94)

    def applyRf(self,Crit="gini",random=None,depth=None,ssplit=8, est=100,boots="True"):
        """
        Applies the Random Forest model with the specified parameters.

        Args:
            Crit: The criterion for splitting nodes in the decision tree. Default is "gini".
            random: The random state for controlling the randomness of the bootstrapping. Default is None.
            depth: The maximum depth of the tree. Default is None.
            ssplit: The minimum number of samples required to split an internal node. Default is 8.
            est: The number of trees in the forest. Default is 100.
            boots: Whether bootstrap samples are used when building trees. Default is "True".

        Returns:
            None
        """
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
        if depth == '':
            depth = None
        if ssplit == '':
            ssplit = 2
        if est == '':
            est = 100

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

        if isinstance(depth, str) and depth != 'None':
            try:
                depth = int(depth)
                if depth<0:
                  tk.messagebox.showerror('Python Error', " max-depth must be positif. ")
                  return
            except:
                tk.messagebox.showerror('Python Error', "max-depth must be an int or None.")
                return
        elif random == 'None':
            random = None


        if isinstance(ssplit, str) :
            try:
                ssplit = float(ssplit)
                if ssplit<0:
                  tk.messagebox.showerror('Python Error', " samples_split must be positif. ")
                  return
            except:
                tk.messagebox.showerror('Python Error', "samples_split must be an int/float ")
                return

        if isinstance(est, str):
            try:
                est = int(est)
                if est < 0:
                    tk.messagebox.showerror('Python Error', " n_estimators must be positif. ")
                    return
            except:
                tk.messagebox.showerror('Python Error', "n_estimators must be an int, ")
                return

        boots= True if boots.lower() == 'true' else False

        self.controller.frames[mf.ModelsFrame].model  = RandomForestClassifier(criterion=Crit,n_estimators=est, random_state=random,max_depth=depth,min_samples_split=ssplit,bootstrap=boots,)
        try:
            # Entraîner le modèle
            self.controller.frames[mf.ModelsFrame].model.fit(self.controller.frames[ppf.PrePFrame].X_train,self.controller.frames[ppf.PrePFrame].y_train)
            tk.messagebox.showinfo('Info', 'Training successful')
            return
        except ValueError as e:
            tk.messagebox.showerror('Python Error', str(e))
            return

    def saveModel(self):
        """
        Saves the trained model to a file.

        Returns:
            None
        """
        if self.controller.frames[mf.ModelsFrame].model is None:
            tk.messagebox.showerror('Python Error', "Please train a model first.")
            return
        filename = tk.filedialog.asksaveasfilename(initialdir="/", title="Select file", filetypes=(("model files", "*.sav"), ("all files", "*.*")))
        if filename == '':
            return
        pickle.dump(self.controller.frames[mf.ModelsFrame].model, open(filename+'.sav', 'wb'))
        tk.messagebox.showinfo('Info', 'Model saved successfully')