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
pip install -e ".[dev]" 
```


## Steps

For module 5, I added unit tests. I have two modules I wanted to test, "loader.py" and "stats.py". I created a new tests
directory to put my tests into, complete with an __init__.py file to make it a package. I then created two test files, 
one for each module. In these files, I wrote unit tests to check the functionality of the methods in the loader and 
stats modules. I used the pytest framework, using the pytest--cov plugin to check the code coverage of my tests. 
I ran the tests to ensure that they were working correctly and that all important code was covered.

---

The init file for the package was updated to reflect the new structure.
