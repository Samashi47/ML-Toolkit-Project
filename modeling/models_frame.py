import tkinter as tk
import customtkinter as ctk
from sklearn.metrics import roc_auc_score, roc_curve
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score, f1_score, precision_score, recall_score
import numpy as np
import modeling.subframes.dt_frame as dtf
import preprocessing.ppframe as ppf

class ModelsFrame(ctk.CTkFrame):
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
        self.eval_frame.grid_propagate(False)  # Fix: Set grid_propagate to False
        
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

        self.dt_frame = dtf.DTFrame(self.TopFrame, self.controller)
        self.dt_frame.place(relx=0.01, rely=0, relwidth=0.98, relheight=0.98, in_=self.TopFrame,bordermode="outside")
        
        
    def evaluateModel(self):
        if self.model is None:
            tk.messagebox.showerror('Python Error', "Please train a model first.")
            return
        
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
            
        self.y_pred = self.model.predict(self.controller.frames[ppf.PrePFrame].X_test)
        disp = ConfusionMatrixDisplay.from_predictions(y_true=self.controller.frames[ppf.PrePFrame].y_test, y_pred=self.y_pred, display_labels=["False", "True"], cmap='Blues')
        f, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))  # Create a Figure object with two subplots
        
        disp.plot(include_values=True, cmap='Blues', ax=ax1, xticks_rotation='horizontal')  # Plot confusion matrix on the first subplot
        ax1.set_title('Confusion Matrix')
        
        # Calculate FP ratio, TP ratio
        fpr, tpr = roc_curve(self.controller.frames[ppf.PrePFrame].y_test, self.y_pred)[:2]
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
        canvas.get_tk_widget().pack_propagate(False)  # Disable widget propagation
        toolbar = VerticalNavigationToolbar2Tk(canvas, self.plot_frame)
        toolbar.update()
        toolbar.pack(side=tk.LEFT, fill=tk.Y)  # Align the toolbar on the right side vertically
        
        self.ac_label.configure(text=str(np.round(accuracy_score(self.controller.frames[ppf.PrePFrame].y_test, self.y_pred)*100,2))+"%")
        self.fl_label.configure(text=str(np.round(f1_score(self.controller.frames[ppf.PrePFrame].y_test, self.y_pred)*100,2))+"%")
        self.prec_label.configure(text=str(np.round(precision_score(self.controller.frames[ppf.PrePFrame].y_test, self.y_pred)*100,2))+"%")
        self.rec_label.configure(text=str(np.round(recall_score(self.controller.frames[ppf.PrePFrame].y_test, self.y_pred)*100,2))+"%")
        
        
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

   # disable showing mouse position in toolbar
   def set_message(self, s):
      pass