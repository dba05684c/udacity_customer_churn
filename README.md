# Predict Customer Churn

- Project **Predict Customer Churn** of ML DevOps Engineer Nanodegree Udacity

## Project Description

In this project, we will  identify credit card customers that are most likely to churn.
The project is written in Python and making use of a GitHub repository in order to demonstrate what I learned in the course "Clean code principle".
The pyhton code must be written in a modular way.
Included is also a file/script which can be used to execute unit testing of the python code.
One component of the project is to demonstrate the ability to write proper/good documentation (amongst which is this file).

## Running Files
This is the list of scripts included:
```
udacity_customer_churn/
│   README.md
│   churn_library.py
│   churn_script_logging_and_tests.py
│   Guide.ipynb
|   churn_notebook.ipynb
│
├── data/
│   │   bank_data.csv
│
├── logs/
│   │   churn_results.log
│   │   unit_test_churn_library.log
│
├── models/
│   │   (Generated pkl files to storel/load ML models)
│
├── images/
├──── eda/
├──── results/
│     │   ...
│
└── .gitignore
```

Install the pylint and autopep8 tools:
pip install pylint
pip install autopep8

Run:  python churn_library.py
      python_script_logging_and_tests.py

check the pylint score using the below:
pylint churn_library.py
pylint churn_script_logging_and_tests.py

To assist with meeting pep 8 guidelines, use autopep8 via the command line commands below:
autopep8 --in-place --aggressive --aggressive churn_script_logging_and_tests.py
autopep8 --in-place --aggressive --aggressive churn_library.py
