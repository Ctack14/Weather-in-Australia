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

For module 9, I made a flask web application to display the weather data and visualizations. The app.py file contains 
the code for the flask application, which reads the weather data and creates visualizations using seaborn and matplotlib. 
The application has a simple interface that allows users to select different types of visualizations to display.
The weather data CSV is loaded once and cached to improve performance. 
Graph generations are stored in a SQLite database to keep track of user interactions and previous queries.
### Endpoints

- `/`: The home page of the application, which displays a welcome message and links to the different visualizations.
- `/analyze`: This endpoint generates and displays a vizualization of data based on the user selection.
- `/history`: This endpoint displays previous queries and their results. Basic logging info is stored using SQLite. The graphs are also displayed here.



---
