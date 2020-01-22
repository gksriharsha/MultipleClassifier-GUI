# 1. RC Klassifier

This document explains the code in each file of the project. There are two components to the code. They are -

* UI Block
* Functionality Block

The overall functionality of the file is explained in this document.

## 1.1. Classifier tool

In this file, the root window of the application contains the basic options to select the classifier, select the location of dataset and to view the results. 

### 1.1.1. Classifier selection

In this section of the window, there are four options to choose from. 

* SVM classifier
* KNN classifier
* MLP classifier
* Auto classification

The first three options have additional settings button enabled. This button on being pressed will open a window where the classifier specific properties can be set.

### 1.1.2. File selection

In this section, there is an option to select to select if the data and labels are in a single file or in different files. 

* In the case of a single file, the labels button will be blocked. The location of the file should be selected from the Data + Labels button.

* In the case of two files, the files should be selected accordingly.

Once the data file is selected, the software checks for any instances which make is tough to classify the dataset such as non numeric fields, etc. 

#### 1.1.2.1. Non Numeric fields in dataset

If there is a presence of Non-numeric fields, a new window will be created automatically requesting the user to select the method to be used to convert them into numeric fields. There are three options available.

* _The text labels do not have a relationship._ - This option means that the labels in the column do not have any relationship between them. For example - A column named: Fruits which might have the values oranges, grapes and apples. For such categorical labels, this option must be selected. This setting is applied to all non-numeric labels in the data.

* _The text labels have a relationship._ - This option means that the labels are ordinal in nature. This should be used when the labels have an implicit order. For example, _Small_, _Medium_ and _Large_. This setting applies to all the non-numeric columns in the data

* _Choose for each column seperately_ - This option gives a fine control over the properties of each column. This option should be choosen when the dataset has both ordinal and categorical non-numeric features in the dataset.Once the option is pressed, each column name will appear in the box to which the user should select one of the two options and click on submit for each column. __This option is enabled only if the number of non-numeric columns are less than 20__. This is done to reduce the burden of selecting for many columns.

Once the methods are chosen, the button close window should be pressed. This will apply the required transformations and __modify__ the dataset and the corresponding file accordingly.

### 1.1.3. Dataset Properties

