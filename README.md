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
- Flask-SQLAlchemy
- SQLite
- Werkzeug
- JavaScript

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

Module 11 required a complete rework of a lot of things. I ended up using it as an opportunity to restructure some of 
the functions I was using to be slightly different. I included most functions right inside of app.py so changed them as
I moved them over. 
Instead of different endpoints, I created one singular dashboard. The user must first log in to gain access, 
authenticating against hashed credentials in SQLite. User IDs are saved in the Flask Session. Once logged in, the
user is prompted to upload a csv file, which is loaded once into a pandas DataFrame and stored in the session cache. 
The user is next taken to the dashboard, where they can select a category from the three buttons (Temperature trends,
Rainfall Patterns, and Rain Prediction). Each button has a dropdown to select a city, which triggers a fetch to the
Flask backend (`/api/analyze`) returning the graphs and summaries. The page updates in place.

---

### The app has a layered structure:
- **Data Layer**: `loader.py` handles CSV imports with async loading. `predictor.py` contains the scikit-learn model for
predictions. Currently only Random Forest is supported, but the file is built to add additional models. Both utilize a 
session cache so they only run once per session. Uploading a new CSV clears the cache to force a reload of the training.
- **Business Logic**: `app.py` contains the Flask app and its routes. All the analysis functions are contained here as 
well, a change from the previous structure to make things more simple and avoid circular imports. Each analysis category
  (temperature, rainfall, prediction) has its own function to build visualizations based on a city's data. It converts 
them to base64 strings so nothing has to be saved to a database or file system. They each have a text summary to 
accompany the graphs.
- **Presentation**: The dashboard is built with one HTML page `dashboard.html`. It uses JavaScript fetch calls to hit 
all the Flask endpoints. This allows the page to be dynamic and swap the charts and summaries without needing to reload
the page. 
- **Authentication**: `auth.py` hashes passwords and establishes default users. The `@login_required` decorator protects
the other endpoints in the app. 
- **Database**: Not used much in the project, but SQLite is used to store credentials and query history.



### Endpoints

- `/login`: GET shows login form. POST authenticates user against hashed credentials from SQLite and starts a session.
- `/logout`: Clears the session. Redirects user to the login page.
- `/upload`: GET shows the CSV upload page. POST takes a CSV file, saves to the server, and asynchronously loads it once
into a pandas DataFrame. Redirects to the dashboard.
- `/dashboard`: A single page interactive dashboard. It has three buttons to access all analysis categories through the
API endpoints below. 
- `/api/analyze`: POST accpets a JSON body with category, city, and an optional input_data parameter (predictions only).
It returns a JSON object with a base64 image and text summary. Supports temperature, rainfall, and prediction categories.
- `/api/cities`: Returns a JSON of unique city names from the CSV. Populates the city dropdown menus.
- `/api/prediction-defaults`: Accepts a JSON body with a city name and returns median values for each column. It's used
to populate the prediction input, allowing users to easily test the model without needing to know the data structure.


---
