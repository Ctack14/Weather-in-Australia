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

For module 8, I migrated the project to a PySpark cluster simulated in Google Colab. The biggest mental shift I needed
to make was understanding that Spark would handle the parallelization and distribution of data across the cluster, so I 
needed to let go of my manual multiprocessing approach and instead focus on writing transformations that could be 
executed in a distributed manner. I also had to adjust my mindset to think in terms of Spark's lazy evaluation model, 
which meant that I needed to be more intentional about when and how I triggered the execution of my transformations.


### Environment Setup

This project was implemented using Google Colab as a virtual Spark cluster.

Steps:
1. Installed PySpark in Colab
2. Created a SparkSession
3. Uploaded dataset (Weather Training Data.csv)
4. Executed my transformations and analyses within the Spark environment

### Key Changes for PySpark Migration

#### 1. Data Loading
- Replaced pandas `read_csv()` with Spark `spark.read.csv()`

#### 2. Data Types and Cleaning
- Explicitly cast numeric columns using `try_cast`
- Converted the categorical columns (RainToday, RainTomorrow) into boolean values using Spark functions
(`col`, `when`, `lower`, `trim`) instead of pandas operations


#### 3. Replacing pandas Operations
- Replaced pandas `.groupby()` with Spark `.groupBy()`
- Replaced column operations with `.withColumn()`

#### 4. Removing Multiprocessing
- Removed Python multiprocessing
- Spark automatically handles parallel execution across partitions

#### 5. Spark is Lazy
- Threw in some `.show()` calls to trigger execution and view intermediate results

#### 6. Visualization Strategy
- Spark does not support direct plotting
- Used `.toPandas()` on sampled data for visualization
- Only used small subsets of the data for plotting to avoid memory issues

---
