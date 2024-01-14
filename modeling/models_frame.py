import tkinter as tk
import customtkinter as ctk
from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_auc_score, roc_curve
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score, f1_score, precision_score, recall_score
import numpy as np
import modeling.subframes.dt_frame as dtf
import modeling.subframes.rf_frame as rff
import modeling.subframes.knn_frame as knnf
import modeling.subframes.svm_frame as svmf
import modeling.subframes.nb_frame as nbf
import modeling.subframes.lr_frame as lrf
import preprocessing.ppframe as ppf

class ModelsFrame(ctk.CTkFrame):
    """
    A class representing the models frame in the ML Toolkit Project.

    Attributes:
        controller: The controller object.
        TopFrame: The top frame.
        eval_frame: The frame to hold the evaluation results.
        plot_frame: The frame to hold the plots.
        classification_report_label: The label for the classification report.
        accuracy_label: The label for the accuracy.
        ac_label: The label for the accuracy value.
        f1_label: The label for the F1 score.
        fl_label: The label for the F1 score value.
        precision_label: The label for the precision.
        prec_label: The label for the precision value.
        recall_label: The label for the recall.
        rec_label: The label for the recall value.
        model: The model object.
        y_pred: The predicted labels.
        y_pred_proba: The predicted probabilities.
        dt_frame: The decision tree frame.
        rf_frame: The random forest frame.
        knn_frame: The K-nearest neighbors frame.
        svm_frame: The support vector machine frame.
        nb_frame: The naive Bayes frame.
        lr_frame: The logistic regression frame.
    """
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent)
        self.rowconfigure((0,1), weight=1)
        self.columnconfigure((0), weight=1)
        self.path = tk.StringVar()

        # Top Frame

        self.TopFrame = ctk.CTkFrame(self, width=self.winfo_width(), height=self.winfo_height()/2, corner_radius=20)
        self.TopFrame.grid(row=0,columnspan=4,padx=(10, 10), pady=(10, 10), sticky="nsew")

        # Frame to hold DataFrame
        self.eval_frame = ctk.CTkFrame(self, width=self.winfo_width(), height=self.winfo_height()/2, corner_radius=20)
        self.eval_frame.grid(row=1,columnspan=4,padx=(10, 10), pady=(0, 10), in_=self, sticky="nsew")
        
        self.plot_frame = ctk.CTkFrame(self, width=self.winfo_width()-200, height=400, corner_radius=20)
        self.plot_frame.place(relx=0.62, rely=0.5,anchor="center", in_=self.eval_frame, bordermode="outside",relwidth=0.7,relheight=0.95)
        
        self.classification_report_label = ctk.CTkLabel(self.eval_frame,font=('Arial',20),text="Classification Report: ")
        self.classification_report_label.place(anchor="center",relx=0.15, rely=0.08)
        self.accuracy_label = ctk.CTkLabel(self.eval_frame,font=('Arial',20),text="Accuracy: ")
        self.accuracy_label.place(anchor="center",relx=0.08, rely=0.2)
        self.ac_label = ctk.CTkLabel(self.eval_frame,font=('Arial',20),text=" 0,00%")
        self.ac_label.place(anchor="center",relx=0.2, rely=0.2)
        self.f1_label = ctk.CTkLabel(self.eval_frame,font=('Arial',20),text="F1 Score: ")
        self.f1_label.place(anchor="center",relx=0.08, rely=0.4)
        self.fl_label = ctk.CTkLabel(self.eval_frame,font=('Arial',20),text=" 0,00%")
        
        self.fl_label.place(anchor="center",relx=0.2, rely=0.4)
        self.precision_label = ctk.CTkLabel(self.eval_frame,font=('Arial',20),text="Precision: ")
        self.precision_label.place(anchor="center",relx=0.08, rely=0.6)
        self.prec_label = ctk.CTkLabel(self.eval_frame,font=('Arial',20),text=" 0,00%")
        self.prec_label.place(anchor="center",relx=0.2, rely=0.6)
        self.recall_label = ctk.CTkLabel(self.eval_frame,font=('Arial',20),text="Recall: ")
        self.recall_label.place(anchor="center",relx=0.07, rely=0.8)
        self.rec_label = ctk.CTkLabel(self.eval_frame,font=('Arial',20),text=" 0,00%")
        self.rec_label.place(anchor="center",relx=0.2, rely=0.8)
        
        self.model = None
        self.y_pred = None
        self.y_pred_proba = None
        self.dt_frame = dtf.DTFrame(self.TopFrame, self.controller)
        self.dt_frame.place(relx=0.01, rely=0, relwidth=0.97, relheight=0.97, in_=self.TopFrame,bordermode="outside")
        
        self.rf_frame = rff.RfFrame(self.TopFrame, self.controller)
        self.rf_frame.place(relx=0.01, rely=0, relwidth=0.97, relheight=0.97, in_=self.TopFrame,bordermode="outside")
        
        self.knn_frame = knnf.KnnFrame(self.TopFrame, self.controller)
        self.knn_frame.place(relx=0.01, rely=0, relwidth=0.97, relheight=0.97, in_=self.TopFrame,bordermode="outside")
        
        self.svm_frame = svmf.SvmFrame(self.TopFrame, self.controller)
        self.svm_frame.place(relx=0.01, rely=0, relwidth=0.97, relheight=0.97, in_=self.TopFrame,bordermode="outside")
        
        self.nb_frame = nbf.NbFrame(self.TopFrame, self.controller)
        self.nb_frame.place(relx=0.01, rely=0, relwidth=0.97, relheight=0.97, in_=self.TopFrame,bordermode="outside")
        
        self.lr_frame = lrf.LRFrame(self.TopFrame, self.controller)
        self.lr_frame.place(relx=0.01, rely=0, relwidth=0.97, relheight=0.97, in_=self.TopFrame,bordermode="outside")
        
        
    def evaluateModel(self):
        """
        Evaluates the trained model by generating and displaying evaluation metrics and plots.

        Raises:
            tk.messagebox.showerror: If the model is not trained or the number of columns in X_train and X_test are not the same.
            ValueError: If there is an error during evaluation.

        Returns:
            None
        """
        if self.model is None:
            tk.messagebox.showerror('Python Error', "Please train a model first.")
            return
        
        if self.controller.frames[ppf.PrePFrame].X_train.shape[1] != self.controller.frames[ppf.PrePFrame].X_test.shape[1]:
            tk.messagebox.showerror('Python Error', "Number of columns in X_train and X_test must be the same.")
            return
        
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        
        try:    
            self.y_pred = self.model.predict(self.controller.frames[ppf.PrePFrame].X_test)
            self.y_pred_proba = self.model.predict_proba(self.controller.frames[ppf.PrePFrame].X_test)
            disp = ConfusionMatrixDisplay.from_predictions(y_true=self.controller.frames[ppf.PrePFrame].y_test, y_pred=self.y_pred, display_labels=np.unique(self.controller.frames[ppf.PrePFrame].y_train), cmap='Blues')
            f, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))  # Create a Figure object with two subplots
            
            disp.plot(include_values=True, cmap='Blues', ax=ax1, xticks_rotation='horizontal')  # Plot confusion matrix on the first subplot
            ax1.set_title('Confusion Matrix')
            
            if self.controller.frames[ppf.PrePFrame].y_test.nunique() > 2:
                # Binarize the target labels for ROC curve computation
                y_test_bin = label_binarize(self.controller.frames[ppf.PrePFrame].y_test, classes=np.unique(self.controller.frames[ppf.PrePFrame].y_train))

                # Calculate false positive rate (fpr), true positive rate (tpr), thresholds for each class
                fpr = dict()
                tpr = dict()
                thresholds = dict()
                auc = dict()

                n_classes = len(np.unique(self.controller.frames[ppf.PrePFrame].y_train))
                for i in range(n_classes):
                    fpr[i], tpr[i], thresholds[i] = roc_curve(y_test_bin[:, i], self.y_pred_proba[:, i])
                    auc[i] = roc_auc_score(y_test_bin[:, i], self.y_pred_proba[:, i])

                for i in range(n_classes):
                    ax2.plot(fpr[i], tpr[i], lw=2, label=f'Class {i} (AUC = {auc[i]:.2f})')

                ax2.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
                ax2.set_xlabel('False Positive Rate')
                ax2.set_ylabel('True Positive Rate')
                ax2.set_title('Receiver Operating Characteristic (ROC) Curve for Each Class')
                ax2.legend(loc='lower right')
                ax2.grid(True)
            else:
                fpr, tpr, _ = roc_curve(self.controller.frames[ppf.PrePFrame].y_test, self.y_pred)
                roc_auc = roc_auc_score(self.controller.frames[ppf.PrePFrame].y_test, self.y_pred)
                ax2.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (AUC = %0.2f)' % roc_auc)
                ax2.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')  # Random guess line
                ax2.set_xlabel('False Positive Rate')
                ax2.set_ylabel('True Positive Rate')
                ax2.set_title('ROC Curve')
                ax2.legend(loc='lower right')
            canvas = FigureCanvasTkAgg(f, self.plot_frame)  # Use the Figure object instead of disp
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.BOTTOM, fill='both', expand=True)  # Use fill='both' and expand=True
            toolbar = VerticalNavigationToolbar2Tk(canvas,self.plot_frame)
            toolbar.update()
            toolbar.pack(side=tk.LEFT, fill=tk.Y, expand=True)  # Use fill='both' and expand=True
            
            self.ac_label.configure(text=str(np.round(accuracy_score(self.controller.frames[ppf.PrePFrame].y_test, self.y_pred)*100,2))+"%")
            self.fl_label.configure(text=str(np.round(f1_score(self.controller.frames[ppf.PrePFrame].y_test, self.y_pred,average='macro',zero_division=np.nan)*100,2))+"%")
            self.prec_label.configure(text=str(np.round(precision_score(self.controller.frames[ppf.PrePFrame].y_test, self.y_pred,average='macro',zero_division=np.nan)*100,2))+"%")
            self.rec_label.configure(text=str(np.round(recall_score(self.controller.frames[ppf.PrePFrame].y_test, self.y_pred,average='macro',zero_division=np.nan)*100,2))+"%")
        except ValueError as e:
            tk.messagebox.showerror('Python Error', str(e))
        
class VerticalNavigationToolbar2Tk(NavigationToolbar2Tk):
   def __init__(self, canvas, window):
      super().__init__(canvas, window, pack_toolbar=False)

   # override _Button() to re-pack the toolbar button in vertical direction
   def _Button(self, text, image_file, toggle, command):
      b = super()._Button(text, image_file, toggle, command)
      b.pack(side=tk.TOP) # re-pack button in vertical direction
      return b

   # override _Spacer() to create vertical separator
   def _Spacer(self):
      s = tk.Frame(self, width=26, relief=tk.RIDGE, bg="DarkGray", padx=2)
      s.pack(side=tk.TOP, pady=5) # pack in vertical direction
      return s
