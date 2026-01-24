# Australian Weather Data Analysis

---
This project loads daily Australian weather data over 10 years
and stores it in a pandas DataFrame. It's likely that this 
project will expand to perform data analysis.

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

For module 2, I broke the project into modules and created a package. This included using a pyproject.toml file for configuration.
I also took the functions previously in main.py and moved them into their own module files within the package. 
main.py is now just an example usage script to run the package once installed. 
I then generated new documentation with:
- `pydoc -w practice_data_sets`
- `pydoc -w main`

__init__.py files were added to each package folder to make them recognizable as packages.

Uploading the package was done using twine. After creating my API key on PyPI, it was very straightforward to upload.

 --- 
For testing, I created a new empty directory, and created a new virtual environment inside it. I then ran:
```bash
pip install Ctack14-practice-data-sets
```
to install the package from pyPI.
I then created a new test script importing the package and running the main function to ensure everything worked as expected.