To start, clone this branch of the repo into your local:

```bash
git clone -b main --single-branch [https://github.com/Samashi47/ML-Toolkit-Project]
```

After cloning the project, activate the env:

```bash
.venv\Scripts\activate
```

You can run the following command to install the dependencies:

```bash
pip3 install -r requirements.txt
```

Then run the main file with the following:

```bash
python main.py
```

> [!IMPORTANT]
> The workflow will be as follows:
>
> After starting the app:
>
> 1. Upload data (.csv/.xls/.xlsx/.xml/.json/.data)
> 2. Process and save changes to DataFrame.
> 3. Visualize your data.
> 4. Choose splitting ratio and random state.
> 5. Choose your target column and split your dataset into training & testing data.
> 1. Choose a ML algorithm.
> 6. Train & test your model and evaluate the results.
