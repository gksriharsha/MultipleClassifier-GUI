# RC Klassifier

This is a GUI tool to assist with machine learning task of classification.

## Usage

### Software

There are two ways of using this software -

* There is a .exe file in the repository which can be executed in any windows platform 

* Python 3.6.3 should be installed with all the packages in the txt file - requirements.txt
    * ```python --version``` should be greater than Python 3.6.3
    * ```pip install -r requirements.txt ``` to install all the required packages
    * ```python Class_GUI.py``` is the command to start the GUI tool 

As this GUI tool is intended for users with little/no programming knowledge, 1st method of usage is recommended.

The program is designed to perform certain checks on the dataset and modify the source file if necessary.__Therefore it is recommended that the user should perform his classification tasks on a copy of the original data only__
### Datset

The software only supports **\*.csv** files for datasets. In future, the support to excel,parquet will be implemented.

Although the tool can perform classification on large datasets, it is recommended that the classification file be less than 1 MB in size. The software will be  optimized to large datasets in future releases.

