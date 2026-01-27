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

For module 3, I restructured the project to use OOP principles while still maintaining the ability to be packaged and uploaded to PyPI.

- `DataLoader` class to handle loading and preprocessing the weather data.
- `DataProcessor` class to perform analysis on the loaded data. Description now returns basic statistics rather than displaying them. They can be displayed in the application logic.
- `app.py` to serve as the main entry point for running the application and composes the objects.

 ---

The init file for the package was updated to reflect the new structure.

### OOP Principles Applied
- Encapsulated data and behavior inside of classes.
- Used methods to operate on the data within the classes.
- Separated concerns by creating distinct classes for loading and processing data.
- Created an application class to manage the workflow. This replaces the old `main.py` script.

