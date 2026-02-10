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

## Technologies
- Python 3.10
- pandas

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
pip install Ctack14-practice-data-sets[dev]
```


## Steps

For module 4, I changed the loader.py file to include a generator function to go through the data one row at a time. 
There is also some error handling using the logger library to log any issues that arise during loading. In both the
loader.py and stats.py files, I also used the logger.info() method to log the progress of the loading and processing steps.
Simple configuration of the logger in app.py allows these changes to be reflected in the console output when running the application.
 ---

The init file for the package was updated to reflect the new structure.

### OOP Principles Applied
- Encapsulated data and behavior inside of classes.
- Used methods to operate on the data within the classes.
- Separated concerns by creating distinct classes for loading and processing data.
- Created an application class to manage the workflow. This replaces the old `main.py` script.

