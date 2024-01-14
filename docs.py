
import tkinter as tk
import customtkinter as ctk

class Docs(ctk.CTkFrame):
    def __init__(self, parent, controller):
        """
        Initialize the Docs object.

        Parameters:
        - parent: The parent widget.
        - controller: The controller object.

        Returns:
        None
        """
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent)
        self.docs_scframe = ctk.CTkScrollableFrame(self, width=self.winfo_width(), height=self.winfo_height(), corner_radius=20)
        self.docs_scframe.rowconfigure((0,1,2), weight=1)
        self.docs_scframe.columnconfigure((0,1,2), weight=1)
        self.docs_scframe.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.98, relheight=0.98)
        
        overview = ctk.CTkLabel(self.docs_scframe, text="I- Overview: ", font=("Arial", 30, "bold"))
        overview.grid(row=0, column=0, sticky="w")
        
        self.overview_textbox = ctk.CTkTextbox(self.docs_scframe, width=1250,height=40, font=("Arial", 15),fg_color='transparent')
        self.overview_textbox.grid(row=1,column=0, columnspan=3, sticky="sw")
        self.overview_textbox.insert(tk.END, "This is a machine learning application that allows you to import a dataset, preprocess it, train it and visualize it.")
        
        self.import_label = ctk.CTkLabel(self.docs_scframe, text="II- Import: ", font=("Arial", 30, "bold"))
        self.import_label.grid(row=2, column=0, sticky="w")
        
        self.import_textbox = ctk.CTkTextbox(self.docs_scframe, width=1250,height=100, font=("Arial", 15),fg_color='transparent')
        self.import_textbox.grid(row=3,column=0, columnspan=3, sticky="sw")
        self.import_textbox.insert(tk.END, "1. Click on the import button.\n2. Select a file.\n3. Click on the show file button."+
                                   "\nSupported file types: .csv, .data, .xlsx, .xls, .json, .xml")
        self.import_textbox.configure(state="disabled")
        
        self.prep_label = ctk.CTkLabel(self.docs_scframe, text="III- Preprocessing: ", font=("Arial", 30, "bold"))
        self.prep_label.grid(row=4, column=0, sticky="w")
        
        self.tts_label = ctk.CTkLabel(self.docs_scframe, text="III.1- Train Test Split: ", font=("Arial", 25, "bold"))
        self.tts_label.grid(row=5, column=0, sticky="w")
        
        self.tts_textbox = ctk.CTkTextbox(self.docs_scframe, width=1250, height=230, font=("Arial", 15),fg_color='transparent')
        self.tts_textbox.grid(row=6,column=0, columnspan=3, sticky="sw")
        self.tts_textbox.insert(tk.END, "test_size: float or int, default=None\n"+
                                "- If float, should be between 0.0 and 1.0 and represent the proportion of the dataset to include in the test split.\n- If int, represents the absolute number of test samples.\n- If None, the value is set to the complement of the train size.\n- If train_size is also None, it will be set to 0.25.\n"+
                                "train_size: float or int, default=None\n"+
                                "- If float, should be between 0.0 and 1.0 and represent the proportion of the dataset to include in the train split.\n- If int, represents the absolute number of train samples.\n- If None, the value is automatically set to the complement of the test size.\n"+
                                "random_state: int, RandomState instance or None, default=None\n"+
                                "- Controls the shuffling applied to the data before applying the split. Pass an int for reproducible output across multiple function calls. See Glossary."+
                                'shuffle: bool, default=True\n'+
                                '- Whether or not to shuffle the data before splitting. If shuffle=False then stratify must be None.')
        self.tts_textbox.configure(state="disabled")
        
        self.msv_label = ctk.CTkLabel(self.docs_scframe, text="III.2- Missing Values: ", font=("Arial", 25, "bold"))
        self.msv_label.grid(row=7, column=0, sticky="w")
        
        self.msv_textbox = ctk.CTkTextbox(self.docs_scframe, width=1250, height=140, font=("Arial", 15),fg_color='transparent')
        self.msv_textbox.grid(row=8,column=0, columnspan=3, sticky="sw")
        self.msv_textbox.insert(tk.END, "Choose imputation strategy:\n"+
                                "- If ‘replace with mean’, then replace missing values using the mean along each column. Can only be used with numerical columns.\n"+
                                "- If ‘replace with median’, then replace missing values using the median along each column. Can only be used with numerical columns.\n"+
                                "- If ‘replace with mode’, then replace missing using the most frequent value along each column. Can be used with categorical columns.\n"+
                                "- If replace with value, then replace missing values with fill_value. Can be used with categorical and numerical columns.\n"+
                                "- If ‘remove rows w/ Null values’, then drop rows with missing values.\n")
        self.msv_textbox.configure(state="disabled")
        
        self.nsc_label = ctk.CTkLabel(self.docs_scframe, text="III.3- Normalization and Scaling: ", font=("Arial", 25, "bold"))
        self.nsc_label.grid(row=9, column=0, sticky="w")
        
        self.nsc_textbox = ctk.CTkTextbox(self.docs_scframe, width=1250, height=387, font=("Arial", 15),fg_color='transparent')
        self.nsc_textbox.grid(row=10,column=0, columnspan=3, sticky="sw")
        self.nsc_textbox.insert(tk.END, "Choose normalization and scaling strategy:\n"+
                                "- If ‘Normalizer’, then normalize samples individually to unit norm.\n"+
                                "   - ‘norm’, ('l1','l2','max'), default=’l2’\n"+
                                "   The norm to use to normalize each non zero sample. If norm=’max’ is used, values will be rescaled by the maximum of the absolute values.\n"+
                                "   - ‘target’, target column\n"+
                                "- If ‘StandardScaler’, then standardize features by removing the mean and scaling to unit variance.\n"+
                                "   - ‘with_mean’ bool, default=True\n"+
                                "   If True, center the data before scaling. This does not work (and will raise an exception) when attempted on sparse matrices, because centering them entails building a dense matrix which in common use cases is likely to be too large to fit in memory.\n"+
                                "   - ‘with_std’ bool, default=True\n"+
                                "   If True, scale the data to unit variance (or equivalently, unit standard deviation).\n"+
                                "   - ‘target’, target column\n"+
                                "- If ‘MinMaxScaler’, then transform features by scaling each feature to a given range.\n"+
                                "   - ‘feature_range’ tuple (min, max), default=(0, 1)\n"+
                                "   Desired range of transformed data.\n"+
                                "   - ‘axis’ 0: column 1: row\n"+
                                "   - ‘target’, target column\n"+
                                "- If ‘MaxAbsScaler’, then scale each feature by its maximum absolute value.\n"+
                                "   - ‘axis’ 0: column 1: row\n"+
                                "   - ‘target’, target column\n")
        self.nsc_textbox.configure(state="disabled")
        
        self.enc_label = ctk.CTkLabel(self.docs_scframe, text="III.4- Encoding: ", font=("Arial", 25, "bold"))
        self.enc_label.grid(row=11, column=0, sticky="w")
        
        self.ohe_label = ctk.CTkLabel(self.docs_scframe, text="III.4.1- One-Hot Encoding: ", font=("Arial", 20))
        self.ohe_label.grid(row=12, column=0, sticky="w")
        
        self.ohe_textbox = ctk.CTkTextbox(self.docs_scframe, width=1250, height=475, font=("Arial", 15),fg_color='transparent')
        self.ohe_textbox.grid(row=13,column=0, columnspan=3, sticky="sw")
        self.ohe_textbox.insert(tk.END, "‘OneHotEncoder’, then encode categorical integer features using a one-hot aka one-of-K scheme.\n"+
                                "- ‘drop’ {‘first’, ‘if_binary’} or an array-like of shape (n_features,), default=None\n"+
                                "   Specifies a methodology to use to drop one of the categories per feature. This is useful in situations where perfectly collinear features cause problems, such as when feeding the resulting data into an unregularized linear regression model.\n"+
                                "   However, dropping one category breaks the symmetry of the original representation and can therefore induce a bias in downstream models, for instance for penalized linear classification or regression models.\n"
                                "- ‘sparse_output’ bool, default=True\n"+
                                "   Will return sparse matrix if set True else will return an array.\n"+
                                "- ‘dtype’ dtype, default=np.float64\n"+
                                "   Desired dtype of output.\n"+
                                "- ‘handle_unknown’ {‘error’, ‘ignore’, ‘infrequent_if_exist’}, default=’error’\n"+
                                "   Specifies the way unknown categories are handled during transform.\n"+
                                "   - ‘error’: Raise an error if an unknown category is present during transform.\n"+
                                "   - ‘ignore’: When an unknown category is encountered during transform, the resulting one-hot encoded columns for this feature will be all zeros. In the inverse transform, an unknown category will be denoted as None.\n"+
                                "   - ‘infrequent_if_exist’: When an unknown category is encountered during transform, the resulting one-hot encoded columns for this feature will map to the infrequent category if it exists. The infrequent category will be mapped to the last position in the encoding. During inverse transform, an unknown category will be mapped to the category denoted 'infrequent' if it exists. If the 'infrequent' category does not exist, then transform and inverse_transform will handle an unknown category as with handle_unknown='ignore'. Infrequent categories exist based on min_frequency and max_categories.\n"+
                                "- ‘min_frequency’ int, default=None\n"+
                                "   Specifies the minimum frequency below which a category will be considered infrequent.\n"+
                                "- ‘max_categories’ int, default=None\n"+
                                "   Specifies an upper limit to the number of output features for each input feature when considering infrequent categories. If there are infrequent categories, max_categories includes the category representing the infrequent categories along with the frequent categories. If None, there is no limit to the number of output features.\n"+
                                "- ‘column to encode’, target column default=col[-1]\n")
        self.ohe_textbox.configure(state="disabled")
        
        self.le_label = ctk.CTkLabel(self.docs_scframe, text="III.4.2- Label Encoding: ", font=("Arial", 20))
        self.le_label.grid(row=14, column=0, sticky="w")
        
        self.le_textbox = ctk.CTkTextbox(self.docs_scframe, width=1250, height=100, font=("Arial", 15),fg_color='transparent')
        self.le_textbox.grid(row=15,column=0, columnspan=3, sticky="sw")
        self.le_textbox.insert(tk.END, "‘LabelEncoder’, Encode target labels with value between 0 and n_classes-1.\n"+
                                "This transformer should be used to encode target values, i.e. y, and not the input X.\n"+
                                "- ‘column to encode’, target column default=col[-1]\n")
        self.le_textbox.configure(state="disabled")

        self.pca_label = ctk.CTkLabel(self.docs_scframe, text="III.5- Decomposition - PCA: ", font=("Arial", 25, "bold"))
        self.pca_label.grid(row=16, column=0, sticky="w")
        
        self.pca_textbox = ctk.CTkTextbox(self.docs_scframe, width=1250, height=320, font=("Arial", 15),fg_color='transparent')
        self.pca_textbox.grid(row=17,column=0, columnspan=3, sticky="sw")
        self.pca_textbox.insert(tk.END, "‘PCA’, Principal component analysis (PCA).\n"+
                                "- ‘n_components’ int, float, None or str\n"+
                                "   Number of components to keep. if n_components is not set all components are kept.\n"+
                                "- ‘whiten’ bool, default=False\n"+
                                "   When True (False by default) the components_ vectors are multiplied by the square root of n_samples and then divided by the singular values to ensure uncorrelated outputs with unit component-wise variances.\nWhitening will remove some information from the transformed signal (the relative variance scales of the components) but can sometime improve the predictive accuracy of the downstream estimators by making their data respect some hard-wired assumptions.\n"+
                                "- ‘svd_solver’ str {‘auto’, ‘full’, ‘arpack’, ‘randomized’}\n"+
                                "   - ‘auto’ chooses the solver automatically based on the type of data.\n"+
                                "   - ‘full’ run exact full SVD calling the standard LAPACK solver via scipy.linalg.svd and select the components by postprocessing\n"+
                                "   - ‘arpack’ run SVD truncated to n_components calling ARPACK solver via scipy.sparse.linalg.svds. It requires strictly 0 < n_components < n_features\n"+
                                "   - ‘randomized’ run randomized SVD by the method of Halko et al.\n"+
                                "- ‘random_state’: int, RandomState instance or None, default=None,\n"+
                                "   Used when the ‘arpack’ or ‘randomized’ solvers are used. Pass an int for reproducible results across multiple function calls.\n"+
                                "- ‘target’, target column\n")
        self.pca_textbox.configure(state="disabled")
        
        self.cnn_label = ctk.CTkLabel(self.docs_scframe, text="III.6- Undersampling - Condensed Nearest Neighbour: ", font=("Arial", 25, "bold"))
        self.cnn_label.grid(row=18, column=0, sticky="w")
        
        self.cnn_textbox = ctk.CTkTextbox(self.docs_scframe, width=1250, height=335, font=("Arial", 15),fg_color='transparent')
        self.cnn_textbox.grid(row=19,column=0, columnspan=3, sticky="sw")
        self.cnn_textbox.insert(tk.END, "‘CondensedNearestNeighbour’, Condensed Nearest Neighbour method.\n"+
                                "- ‘n_neighbors’ int, default=None\n"+
                                "   If int, size of the neighbourhood to consider to compute the nearest neighbors.\n"+
                                "   If None, a KNeighborsClassifier with a 1-NN rules will be used.\n"+
                                "- ‘sampling_strategy’ str default='auto'\n"+
                                "   If 'majority': resample only the majority class;\n"+
                                "   If 'not minority': resample all classes but the minority class;\n"+
                                "   If 'not majority': resample all classes but the majority class;\n"+
                                "   If 'all': resample all classes;\n"+
                                "   If 'auto': equivalent to 'not minority'.\n"+
                                "- ‘random_state’ int, default=None\n"+
                                "   Control the randomization of the algorithm.\n"+
                                "   If int, random_state is the seed used by the random number generator;\n"+
                                "   If None, the random number generator is the RandomState instance used by np.random.\n"+
                                "- ‘n_seeds_S’,int, default=1.\n"+
                                "   Number of samples to extract in order to build the set S.\n")
        self.cnn_textbox.configure(state="disabled")
        
        self.svmsmote_label = ctk.CTkLabel(self.docs_scframe, text="III.7- Oversampling - SVMSMOTE: ", font=("Arial", 25, "bold"))
        self.svmsmote_label.grid(row=20, column=0, sticky="w")
        
        self.svmsmote_textbox = ctk.CTkTextbox(self.docs_scframe, width=1250, height=335, font=("Arial", 15),fg_color='transparent')
        self.svmsmote_textbox.grid(row=21,column=0, columnspan=3, sticky="sw")
        self.svmsmote_textbox.insert(tk.END, "‘SVMSMOTE’, Support Vector Machines Synthetic Minority Oversampling Technique.\n"+
                                "- ‘sampling_strategy’ str default='auto'\n"+
                                "   If 'majority': resample only the majority class;\n"+
                                "   If 'not minority': resample all classes but the minority class;\n"+
                                "   If 'not majority': resample all classes but the majority class;\n"+
                                "   If 'all': resample all classes;\n"+
                                "   If 'auto': equivalent to 'not minority'.\n"+
                                "- ‘random_state’ int, default=None\n"+
                                "   Control the randomization of the algorithm.\n"+
                                "   If int, random_state is the seed used by the random number generator;\n"+
                                "   If None, the random number generator is the RandomState instance used by np.random.\n"+
                                "- ‘k_neighbors’ int or object, default=5\n"+
                                "   The nearest neighbors used to define the neighborhood of samples to use to generate the synthetic samples."
                                "- ‘m_neighbors’ int, default=10\n"+
                                "   The nearest neighbors used to determine if a minority sample is in “danger”. You can pass:\n"+
                                "- ‘out_step’ float, default=0.5\n"+
                                "   Step size when extrapolating.\n")
        self.svmsmote_textbox.configure(state="disabled")
        
        self.model_label = ctk.CTkLabel(self.docs_scframe, text="IV- Modeling: ", font=("Arial", 30, "bold"))
        self.model_label.grid(row=22, column=0, sticky="w")
        
        self.dt_label = ctk.CTkLabel(self.docs_scframe, text="IV.1- Decision Tree Classifier: ", font=("Arial", 25, "bold"))
        self.dt_label.grid(row=23, column=0, sticky="w")
        
        self.dt_textbox = ctk.CTkTextbox(self.docs_scframe, width=1250, height=670, font=("Arial", 15),fg_color='transparent')
        self.dt_textbox.grid(row=24,column=0, columnspan=3, sticky="sw")
        self.dt_textbox.insert(tk.END, "‘DecisionTreeClassifier’, A decision tree classifier.\n"+
                                "- ‘criterion’ {“gini”, “entropy”}, default=”gini”\n"+
                                "   The function to measure the quality of a split. Supported criteria are “gini” for the Gini impurity and “entropy” for the information gain.\n"+
                                "- ‘splitter’ {“best”, “random”}, default=”best”\n"+
                                "   The strategy used to choose the split at each node. Supported strategies are “best” to choose the best split and “random” to choose the best random split.\n"+
                                "- ‘max_depth’ int, default=None\n"+
                                "   The maximum depth of the tree. If None, then nodes are expanded until all leaves are pure or until all leaves contain less than min_samples_split samples.\n"+
                                "- ‘min_samples_split’ int or float, default=2\n"+
                                "   The minimum number of samples required to split an internal node:\n"+
                                "   - If int, then consider min_samples_split as the minimum number.\n"+
                                "   - If float, then min_samples_split is a fraction and ceil(min_samples_split * n_samples) are the minimum number of samples for each split.\n"+
                                "- ‘min_samples_leaf’ int or float, default=1\n"+
                                "   The minimum number of samples required to be at a leaf node:\n"+
                                "   - If int, then consider min_samples_leaf as the minimum number.\n"+
                                "   - If float, then min_samples_leaf is a fraction and ceil(min_samples_leaf * n_samples) are the minimum number of samples for each node.\n"+
                                "- ‘max_features’ int, float or {“auto”, “sqrt”, “log2”}, default=None\n"+
                                "   The number of features to consider when looking for the best split:\n"+
                                "   - If int, then consider max_features features at each split.\n"+
                                "   - If float, then max_features is a fraction and int(max_features * n_features) features are considered at each split.\n"+
                                "   - If “sqrt”, then max_features=sqrt(n_features) (same as “auto”).\n"+
                                "   - If “log2”, then max_features=log2(n_features).\n"+
                                "   - If None, then max_features=n_features.\n"+
                                "- ‘random_state’ int or None, default=None\n"+
                                "Controls the randomness of the estimator. The features are always randomly permuted at each split, even if splitter is set to 'best'. When max_features < n_features, the algorithm will select max_features at random at each split before finding the best split among them. But the best found split may vary across different runs, even if max_features=n_features. That is the case, if the improvement of the criterion is identical for several splits and one split has to be selected at random. To obtain a deterministic behaviour during fitting, random_state has to be fixed to an integer.\n"
                                "- ‘max_leaf_nodes’ int, default=None\n"+
                                "Grow a tree with max_leaf_nodes in best-first fashion. Best nodes are defined as relative reduction in impurity. If None then unlimited number of leaf nodes.\n"+
                                "- ‘min_impurity_decrease’ float, default=0.0\n"+
                                "A node will be split if this split induces a decrease of the impurity greater than or equal to this value.\n"+
                                "- ‘min_weight_fraction_leaf’ float, default=0.0\n"+
                                "The minimum weighted fraction of the sum total of weights (of all the input samples) required to be at a leaf node. Samples have equal weight when sample_weight is not provided.\n"+
                                "- ‘cc_alpha’ non-negative float, default=0.0\n"+
                                "Complexity parameter used for Minimal Cost-Complexity Pruning. The subtree with the largest cost complexity that is smaller than ccp_alpha will be chosen. By default, no pruning is performed.\n")
        self.dt_textbox.configure(state="disabled")
        
        self.rf_label = ctk.CTkLabel(self.docs_scframe, text="IV.2- Random Forest Classifier: ", font=("Arial", 25, "bold"))
        self.rf_label.grid(row=25, column=0, sticky="w")
        
        self.rf_textbox = ctk.CTkTextbox(self.docs_scframe, width=1250, height=315, font=("Arial", 15),fg_color='transparent')
        self.rf_textbox.grid(row=26,column=0, columnspan=3, sticky="sw")
        self.rf_textbox.insert(tk.END, "‘RandomForestClassifier’, A random forest classifier.\n"+
                               "- ‘criterion’ {“gini”, “entropy”}, default=”gini”\n"+
                                "   The function to measure the quality of a split. Supported criteria are “gini” for the Gini impurity and “entropy” for the information gain.\n"+
                                "- ‘n_estimators’ int, default=100\n"+
                                "   The number of trees in the forest.\n"+
                                "- ‘max_depth’ int, default=None\n"+
                                "   The maximum depth of the tree. If None, then nodes are expanded until all leaves are pure or until all leaves contain less than min_samples_split samples.\n"+
                                "- ‘min_samples_split’ int or float, default=2\n"+
                                "   The minimum number of samples required to split an internal node:\n"+
                                "   - If int, then consider min_samples_split as the minimum number.\n"+
                                "   - If float, then min_samples_split is a fraction and ceil(min_samples_split * n_samples) are the minimum number of samples for each split.\n"+
                                "- ‘random_state’ int or None, default=None\n"+
                                "   Controls both the randomness of the bootstrapping of the samples used when building trees (if bootstrap=True) and the sampling of the features to consider when looking for the best split at each node (if max_features < n_features).\n"+
                                "- ‘bootstrap’ bool, default=True \n"+
                                "   Whether bootstrap samples are used when building trees. If False, the whole dataset is used to build each tree.\n")
        self.rf_textbox.configure(state="disabled")
            
        self.knn_label = ctk.CTkLabel(self.docs_scframe, text="IV.3- KNN Classifier: ", font=("Arial", 25, "bold"))
        self.knn_label.grid(row=27, column=0, sticky="w")
        
        self.knn_textbox = ctk.CTkTextbox(self.docs_scframe, width=1250, height=405, font=("Arial", 15),fg_color='transparent') 
        self.knn_textbox.grid(row=28,column=0, columnspan=3, sticky="sw")
        self.knn_textbox.insert(tk.END, "‘KNeighborsClassifier’, Classifier implementing the k-nearest neighbors vote.\n"+
                                "- ‘n_neighbors’ int, default=5\n"+
                                "   Number of neighbors to use by default for kneighbors queries.\n"+
                                "- ‘weights’ {‘uniform’, ‘distance’}, default=’uniform’\n"+
                                "   weight function used in prediction. Possible values:\n"+
                                "   - ‘uniform’ : uniform weights. All points in each neighborhood are weighted equally.\n"+
                                "   - ‘distance’ : weight points by the inverse of their distance. in this case, closer neighbors of a query point will have a greater influence than neighbors which are further away.\n"+
                                "- ‘algorithm’ {‘auto’, ‘ball_tree’, ‘kd_tree’, ‘brute’}, default=’auto’\n"+
                                "   Algorithm used to compute the nearest neighbors:\n"+
                                "   - ‘ball_tree’ will use BallTree\n"+
                                "   - ‘kd_tree’ will use KDTree\n"+
                                "   - ‘brute’ will use a brute-force search.\n"+
                                "   - ‘auto’ will attempt to decide the most appropriate algorithm based on the values passed to fit method.\n"+
                                "- ‘leaf_size’ int, default=30\n"+
                                "   Leaf size passed to BallTree or KDTree. This can affect the speed of the construction and query, as well as the memory required to store the tree. The optimal value depends on the nature of the problem.\n"+
                                "- ‘p’ int, default=2\n"+
                                "   Power parameter for the Minkowski metric. When p = 1, this is equivalent to using manhattan_distance (l1), and euclidean_distance (l2) for p = 2. For arbitrary p, minkowski_distance (l_p) is used.\n"+
                                "- ‘n_jobs’ int, default=None\n"+
                                "   The number of parallel jobs to run for neighbors search. None means 1 unless in a joblib.parallel_backend context. -1 means using all processors.\n")
        self.knn_textbox.configure(state="disabled")
        
        self.svm_label = ctk.CTkLabel(self.docs_scframe, text="IV.4- SVM Classifier: ", font=("Arial", 25, "bold"))
        self.svm_label.grid(row=29, column=0, sticky="w")
        
        self.svm_textbox = ctk.CTkTextbox(self.docs_scframe, width=1250, height=315, font=("Arial", 15),fg_color='transparent')
        self.svm_textbox.grid(row=30,column=0, columnspan=3, sticky="sw")
        self.svm_textbox.insert(tk.END, "‘SVC’, C-Support Vector Classification.\n"+
                                "- ‘C’ float, default=1.0\n"+
                                "   Regularization parameter. The strength of the regularization is inversely proportional to C. Must be strictly positive. The penalty is a squared l2 penalty.\n"+
                                "- ‘kernel’ {‘linear’, ‘poly’, ‘rbf’, ‘sigmoid’, ‘precomputed’}, default=’rbf’\n"+
                                "   Specifies the kernel type to be used in the algorithm. It must be one of ‘linear’, ‘poly’, ‘rbf’, ‘sigmoid’, ‘precomputed’ or a callable.\n"+
                                "- ‘degree’ int, default=3\n"+
                                "   Degree of the polynomial kernel function (‘poly’). Ignored by all other kernels.\n"+
                                "- ‘gamma’ float, default=’scale’\n"+
                                "   Kernel coefficient for ‘rbf’, ‘poly’ and ‘sigmoid’.\n"+
                                "   - if float, must be non-negative.\n"+
                                "   - if ‘scale’, then gamma is set to 1 / (n_features * X.var())\n"+
                                "- ‘random_state’ int or None, default=None\n"+
                                "   Controls the pseudo random number generation for shuffling the data for probability estimates. Ignored when probability is False. Pass an int for reproducible output across multiple function calls.\n"+
                                "- ‘max_iter’ int, default=-1\n"+
                                "   Hard limit on iterations within solver, or -1 for no limit.\n")
        self.svm_textbox.configure(state="disabled")
        
        self.nb_label = ctk.CTkLabel(self.docs_scframe, text="IV.5- Naive Bayes Classifier: ", font=("Arial", 25, "bold"))
        self.nb_label.grid(row=31, column=0, sticky="w")
        
        self.gnb_label = ctk.CTkLabel(self.docs_scframe, text="IV.5.1- Gaussian Naive Bayes Classifier: ", font=("Arial", 20))
        self.gnb_label.grid(row=32, column=0, sticky="w")
        
        self.gnb_textbox = ctk.CTkTextbox(self.docs_scframe, width=1250, height=90, font=("Arial", 15),fg_color='transparent')
        self.gnb_textbox.grid(row=33,column=0, columnspan=3, sticky="sw")
        self.gnb_textbox.insert(tk.END, "‘GaussianNB’, Gaussian Naive Bayes (GaussianNB)\n"+
                                "- ‘var_smoothing’ float, default=1e-9\n"+
                                "   Portion of the largest variance of all features that is added to variances for calculation stability.\n")
        self.gnb_textbox.configure(state="disabled")
        
        self.mnb_label = ctk.CTkLabel(self.docs_scframe, text="IV.5.2- Multinomial Naive Bayes Classifier: ", font=("Arial", 20))
        self.mnb_label.grid(row=34, column=0, sticky="w")
        
        self.mnb_textbox = ctk.CTkTextbox(self.docs_scframe, width=1250, height=125, font=("Arial", 15),fg_color='transparent')
        self.mnb_textbox.grid(row=35,column=0, columnspan=3, sticky="sw")
        self.mnb_textbox.insert(tk.END, "‘MultinomialNB’, Multinomial Naive Bayes (MultinomialNB)\n"+
                                "- ‘alpha’ float, default=1.0\n"+
                                "   Additive (Laplace/Lidstone) smoothing parameter (0 for no smoothing).\n"+
                                "- ‘fit_prior’ bool, default=True\n"+
                                "   Whether to learn class prior probabilities or not. If false, a uniform prior will be used.\n")
        self.mnb_textbox.configure(state="disabled")
        
        self.lr_label = ctk.CTkLabel(self.docs_scframe, text="IV.6- Logistic Regression Classifier: ", font=("Arial", 25, "bold"))
        self.lr_label.grid(row=36, column=0, sticky="w")
        
        self.lr_textbox = ctk.CTkTextbox(self.docs_scframe, width=1250, height=820, font=("Arial", 15),fg_color='transparent')
        self.lr_textbox.grid(row=37,column=0, columnspan=3, sticky="sw")
        self.lr_textbox.insert(tk.END, "‘LogisticRegression’, Logistic Regression (aka logit, MaxEnt) classifier.\n"+
                                "- ‘penalty’ {‘l1’, ‘l2’, ‘elasticnet’, ‘none’}, default=’l2’\n"+
                                "   Used to specify the norm used in the penalization. The ‘newton-cg’, ‘sag’ and ‘lbfgs’ solvers support only l2 penalties.\n"+
                                "- ‘C’ float, default=1.0\n"+
                                "   Inverse of regularization strength; must be a positive float. Like in support vector machines, smaller values specify stronger regularization.\n"+
                                "- ‘solver’ {‘newton-cg’, ‘lbfgs’, ‘liblinear’, ‘sag’, ‘saga’}, default=’lbfgs’\n"+
                                "   Algorithm to use in the optimization problem.\n"+
                                "   - For small datasets, ‘liblinear’ is a good choice, whereas ‘sag’ and ‘saga’ are faster for large ones;\n"+
                                "   - For multiclass problems, only ‘newton-cg’, ‘sag’, ‘saga’ and ‘lbfgs’ handle multinomial loss;\n"+
                                "   - ‘liblinear’ is limited to one-versus-rest schemes.\n"+
                                "   - ‘newton-cholesky’ is a good choice for n_samples >> n_features, especially with one-hot encoded categorical features with rare categories. Note that it is limited to binary classification and the one-versus-rest reduction for multiclass classification. Be aware that the memory usage of this solver has a quadratic dependency on n_features because it explicitly computes the Hessian matrix.\n"+
                                "Warning The choice of the algorithm depends on the penalty chosen. Supported penalties by solver:\n"+
                                "   - ‘lbfgs’ - [‘l2’, None]\n"+
                                "   - ‘liblinear’ - [‘l1’, ‘l2’]\n"+
                                "   - ‘newton-cg’ - [‘l2’, None]\n"+
                                "   - ‘newton-cholesky’ - [‘l2’, None]\n"+
                                "   - ‘sag’ - [‘l2’, None]\n"+
                                "   - ‘saga’ - [‘elasticnet’, ‘l1’, ‘l2’, None]\n"+
                                "- ‘max_iter’ int, default=100\n"+
                                "   Maximum number of iterations taken for the solvers to converge.\n"+
                                "- ‘random_state’ int, default=None\n"+
                                "   Used when solver == ‘sag’, ‘saga’ or ‘liblinear’ to shuffle the data.\n"+
                                "- ‘tol’ float, default=1e-4\n"+
                                "   Tolerance for stopping criteria.\n"+
                                "- ‘multi_class’ {‘auto’, ‘ovr’, ‘multinomial’}, default=’auto’\n"+
                                "If the option chosen is ‘ovr’, then a binary problem is fit for each label. For ‘multinomial’ the loss minimised is the multinomial loss fit across the entire probability distribution, even when the data is binary. ‘multinomial’ is unavailable when solver=’liblinear’. ‘auto’ selects ‘ovr’ if the data is binary, or if solver=’liblinear’, and otherwise selects ‘multinomial’.\n"+
                                "- ‘intercept_scaling’ float, default=1\n"+
                                "   Useful only when the solver ‘liblinear’ is used and self.fit_intercept is set to True. In this case, x becomes [x, self.intercept_scaling], i.e. a “synthetic” feature with constant value equal to intercept_scaling is appended to the instance vector. The intercept becomes intercept_scaling * synthetic_feature_weight.\n"+
                                "   Note! the synthetic feature weight is subject to l1/l2 regularization as all other features. To lessen the effect of regularization on synthetic feature weight (and therefore on the intercept) intercept_scaling has to be increased.\n"+
                                "- ‘class_weight’ ‘balanced’, default=None\n"+
                                "   Weights associated with classes in the form (class_label: weight). If not given, all classes are supposed to have weight one.\n"+
                                "   The ‘balanced’ mode uses the values of y to automatically adjust weights inversely proportional to class frequencies in the input data as n_samples / (n_classes * np.bincount(y)).\n"+
                                "   Note that these weights will be multiplied with sample_weight (passed through the fit method) if sample_weight is specified.\n"+
                                "- ‘fit_intercept’ bool, default=True\n"+
                                "   Specifies if a constant (a.k.a. bias or intercept) should be added to the decision function.\n"+
                                "- ‘dual’ bool, default=False\n"+
                                "   Dual or primal formulation. Dual formulation is only implemented for l2 penalty with liblinear solver. Prefer dual=False when n_samples > n_features.\n"+
                                "- ‘warm_start’ bool, default=False\n"+
                                "   When set to True, reuse the solution of the previous call to fit as initialization, otherwise, just erase the previous solution.\n")
        self.lr_textbox.configure(state="disabled")
        
        self.mp_label = ctk.CTkLabel(self.docs_scframe, text="V- Model Performance: ", font=("Arial", 30, "bold"))
        self.mp_label.grid(row=38, column=0, sticky="w")
        
        self.mp_textbox = ctk.CTkTextbox(self.docs_scframe, width=1250, height=180, font=("Arial", 15),fg_color='transparent')
        self.mp_textbox.grid(row=39,column=0, columnspan=3, sticky="sw")
        self.mp_textbox.insert(tk.END, "‘Model Performance’, Model Performance.\n"+
                                "- ‘accuracy_score’\n"+
                                "- ‘precision_score’ (macro)\n"+
                                "- ‘recall_score’ (macro)\n"+
                                "- ‘f1_score’ (macro)\n"+
                                "- ‘roc_auc_score’ (supports multiclass)\n"+
                                "- ‘roc_curve_plot’ (supports multiclass)\n"+
                                "- ‘confusion_matrix_heatmap_plot’ (supports multiclass)\n")
        self.mp_textbox.configure(state="disabled")
        
        self.viz_label = ctk.CTkLabel(self.docs_scframe, text="VI- Visualization: ", font=("Arial", 30, "bold"))
        self.viz_label.grid(row=40, column=0, sticky="w")
        
        self.mpl_label = ctk.CTkLabel(self.docs_scframe, text="VI.1- Matplotlib: ", font=("Arial", 25, "bold"))
        self.mpl_label.grid(row=41, column=0, sticky="w")
        
        self.mpl_textbox = ctk.CTkTextbox(self.docs_scframe, width=1250, height=230, font=("Arial", 15),fg_color='transparent')
        self.mpl_textbox.grid(row=42,column=0, columnspan=3, sticky="sw")
        self.mpl_textbox.insert(tk.END, "‘Matplotlib’, Matplotlib is a comprehensive library for creating static, animated, and interactive visualizations in Python.\n"+
                                "- line\n"+
                                "- ‘scatter’\n"+
                                "- ‘bar’\n"+
                                "- ‘histogram’\n"+
                                "- ‘boxplot’\n"+
                                "- ‘pieplot’\n"+
                                "- ‘Areaplot’\n"+
                                "- ‘violinplot’\n"+
                                "- ‘3dplot’\n"+
                                "- ‘errorbar’\n")
        self.mpl_textbox.configure(state="disabled")
        
        self.sns_label = ctk.CTkLabel(self.docs_scframe, text="VI.2- Seaborn: ", font=("Arial", 25, "bold"))
        self.sns_label.grid(row=43, column=0, sticky="w")
        
        self.sns_textbox = ctk.CTkTextbox(self.docs_scframe, width=1250, height=150, font=("Arial", 15),fg_color='transparent')
        self.sns_textbox.grid(row=44,column=0, columnspan=3, sticky="sw")
        self.sns_textbox.insert(tk.END, "‘Seaborn’, Seaborn is a Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics.\n"+
                                "- ‘scatterplot’\n"+
                                "- ‘barplot’\n"+
                                "- ‘boxplot’\n"+
                                "- ‘violinplot’\n"+
                                "- ‘histogram’\n")
        self.sns_textbox.configure(state="disabled")