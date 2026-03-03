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
Use app.py to describe and create visualizations of the data.

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

For module 7, I refactored my code to take advantage of asynchronous programming and multiprocessing.
Async changes:
- The loader.py file was modified to use asynchronous programming to read CSV files concurrently, improving the 
efficiency of data loading.
- The visualize.py file was updated to use multiprocessing to create visualizations in parallel, which can speed up the 
generation of multiple plots. Calculating the KDE of each plot is very CPU intensive, so this change should 
significantly reduce the time taken to create visualizations. Another potential optimization would be to compute these
separately in their own processes, then load the results back into the main process to create the final visualizations.
- The test_visuals.py file was updated to test the new asynchronous and multiprocessing code, ensuring that the changes 
do not break existing functionality. Tests were also updated/created to test added functionality such as the addition of
an output directory and the ability to specify which visualizations to create within one function.
- The app.py file was updated to use the new asynchronous and multiprocessing code, allowing for faster data loading and 
visualization when running the application.

---

The init file for the package was updated to reflect the new structure.
