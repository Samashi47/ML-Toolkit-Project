To start off, clone this branch of the repo into your local:

bash
git clone -b main --single-branch [https://github.com/Samashi47/ML-Toolkit-Project]


After cloning the project, activate the env:

bash
.venv\Scripts\activate


You can run the following command to install the dependencies:

bash
pip3 install -r requirements.txt


Then run the main file with:

bash
python main.py


2 sets of data are included, for users to test the app, first one is the titanic dataset to test all features of the app, second one is the same dataset but cleaned so the user can test training and testing the model directly.

> [!IMPORTANT]
> The work flow will be as follows:
>
> After starting the app:
>
> 1. Choose your wanted ML algorithm
> 2. Upload data
> 3. Process & visualize your data
> 4. Choose your target column
> 5. Split your dataset into training & testing data
> 6. Train & test your model, then see results
