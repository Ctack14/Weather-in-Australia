# Australian Weather Data Analysis

---
This project loads daily Australian weather data over 10 years
and stores it in a pandas DataFrame. It's likely that this 
project will expand to perform more advanced data analysis.

## Dataset
- Title: Australia Weather Data
- Source: Kaggle

## Usage
Run main.py to read and display weather data to the console.
Use the analysis notebook to test out various functions
Use app.py to launch the flask web application to display the weather data and visualizations. (run from within src)

## Technologies
- Python 3.10
- pandas
- pytest
- seaborn
- matplotlib
- scikit-learn
- Flask

## Installation
Make sure you have:
- Python 3.10 or higher installed
- Build installed: `pip install build`

To install the required dependencies, run the following command:
```bash 
pip install Ctack14-practice-data-sets
```
---
To Install as a developer:
```bash
pip install -e ".[dev]" 
```


## Steps

For module 10, I added a rain prediction feature. Scikit-learn's Random Forest Classifier is used to predict whether it
will rain the next day based on input fields. You access the fields through a link on the home page (index) of the 
application. The model is trained on the entire dataset (Weather Training Data.csv) in an 80/20 split for training and 
test sets, and uses stratified sampling to keep the balance even between trees. The model is trained on the first 
prediction request and is cached for future use. 

I used random forest because it is a powerful model that can handle the mixed-scale features with minimal preprocessing.
Feature importances are easily extracted from the model, so you can see which variables actually matter for the 
prediction. The model is also relatively fast to train, important for a web application. It's prediction speed is also
adequate for the application, although other models exist that are faster.

A new "/predict" endpoint was added, serving a form where you can enter in weather values and pick a location. The 
trained model runs the prediction and displays a results page. This page contains the prediction along with
feature importances and other interesting metrics. 



### Endpoints

- `/`: The home page of the application, which displays a welcome message and links to the different visualizations.
- `/analyze`: This endpoint generates and displays a vizualization of data based on the user selection.
- `/history`: This endpoint displays previous queries and their results. Basic logging info is stored using SQLite. The 
graphs are also displayed here.
- `'/predict`: Calling the GET method will display the prediction form, and POST runs the model and displays the result
page.


---
