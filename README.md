# NBA-Regression-Analysis

Final Project for ECSE-4840 Intro to Machine Learning

## Overview 

For my final project, I created a regression analysis on NBA win percentages. The goal of this 
project was to collect and curate my own basketball data from [basketball-reference](https://www.basketball-reference.com/) and use 
that data to fit various regression models, evaluate their performance and use them to make way-
too-early predictions for the final standings for this ('24-'25) NBA season. This project will be using data 
preprocessing techniques mentioned in class, like normalization. For this project, I will also be 
using three different regression models based on methods discussed in class – the standard
Ordinary Least Squares Regression, Support Vector Regression, and Random Forest Regression. 
This project will also require proper evaluation techniques, so we can interpret the results and understand 
the success and/or failures of the methods. All of these techniques have been introduced in class 
and will be applied during this project.

See the [Final Project Report](https://github.com/zachaa2/NBA-Regression-Analysis/blob/main/project/report/Final_Report.pdf) in the ```report``` folder for the full project analysis.

## Techniques used

This project uses various techniques related to collecting data and implementing machine learning algorithms. 

- web scraping/dataset compilation

- EDA (Exploratory Data Analysis)

- Feature Creation

- Normalization

- Linear Regression

- SVR (Support Vector Regression)

- Random Forest Regression

- Figure Creation (Visualizing Results)

## Source Code Overview

The scripts are ordered below based on their intended usage. Use the ```requirements.txt``` file to setup a virtual enviornment to run all the code. For info on how to setup a virtual enviornment, see [python's docs](https://docs.python.org/3/library/venv.html). 

### Scraper Tools / Data Collection

```scraper_utils.py```

This script contains a bunch of utility functions for the webscraping process. It includes the logic related to getting the page content 
and parsing the data into a raw dataframe, as well as adhering to the site's ```robots.txt``` policy. This script is not meant to be run on its own. 

```scraper.py```

This script contains the rest of the logic related to the data collection process. The script includes all the table specific logic needed to properly parse the scraped data into the necessary data tables. This script is not meant to be run on its own. 

```fetch_bballref_data.py --start_year <int> --end_year <int> --year <int> --table <str>```

This script is the driver for the data collection process. The script will fetch and parse all the given tables from [basketball-reference](https://www.basketball-reference.com/), 
and save them as csv's in the ```./data/{year}``` directory. The arguments are as follows:

1. --start_year (int): Start year to fetch data from

2. --end_year (int): End year to fetch data from

3. --year (int): Year to fetch data from (if no date range is needed). Leave blank if a range is needed

4. --table (str): Table(s) to fetch (if None, then fetch all)

### Feature Creation

The methods used in this project use three key features to represent each data point: Simple Rating System (SRS), Net Rating (NRtg), and Four Factors. The script below use the collected data to calculate and compite these metrics into csv files, so they can be used for the ML algorithms. 

```srs.py --start_year <int> --end_year <int> --year <int>```

This script is used to get the SRS metric for all teams for a given range of years. The SRS is also normalized (see the report for a full explanation). The usage is as follows:

1. --start_year (int): Start year to fetch data from

2. --end_year (int): End year to fetch data from

3. --year (int): Year to fetch data from (if no date range is needed). Leave blank if a range is needed

```nrtg.py --start_year <int> --end_year <int> --year <int>```

This script is used to get the Net Rating (NRtg) for all teams for a given range of years. The Net Rating is normalized (see the report for a full explanation). The usage is as follows: 

1. --start_year (int): Start year to fetch data from

2. --end_year (int): End year to fetch data from

3. --year (int): Year to fetch data from (if no date range is needed). Leave blank if a range is needed

```four_factors.py --start_year <int> --end_year <int> --year <int>```

This script is used to the the Four Factor Score for all teams for a given range of years. The four factor score is a combination between the offensive four factors and defensive four factors. The score is then normalized. The calculation for the four factor score is less straightforward than the other two metrics - view the "Data Collection and Preprocessing" section in the report for the full explanation for all the metrics. The usage is as follows:

1. --start_year (int): Start year to fetch data from

2. --end_year (int): End year to fetch data from

3. --year (int): Year to fetch data from (if no date range is needed). Leave blank if a range is needed

### Data Assembly

```assemble_data.py --train_years <str> --test_years <str> --start_year <int> --end_year <int> --write```

Once the data is fetched from [basketball-reference](https://www.basketball-reference.com/) and the features are created, we can now use this script to assemble the data in a format that can be used by our machine learning algorithms. This script is used to create the train/test split, as well as compiling a single large ```data.csv```. The split is done based off the years. All the output is saved into the ```./data``` directory. The script can also optionally save a yearly ```data.csv``` into each year's data folder (```./data/{year}```). 

The usage is as follows:

1. --train_years (str): Year range for training data (e.g., 2000-2015).

2. --test_years (str): Year range for testing data (e.g., 2016-2020).

3. --start_year (int): Start year for the dataset. Specify this and end year to compile one dataset for the given range

4. --end_year (int): End year for the dataset. Specify this and start year to compile one dataset for the given range

5. --write: Whether to write the yearly data as a csv to its respective data folder

### Machine Learning Methods

Once the dataset has been finalized, we can use the following scripts to fit various regression models. The goal is to predict the response variable (win%) based off the three advanced features calculated from our parsed data (SRS, NRtg, Four Factor). For each method, the error is calculated as the Root Mean Squared Error (RMSE), and the quality of fit on the test data is represented by the Coefficient of Determination (R^2). 

When using the scripts, we can either use the train test datasets (```train.csv``` and ```test.csv```), or we can evaluate on a specific year by first fitting the model on the compiled ```data.csv```. 

```linreg.py --eval_year <int>```

This script is used to fit a Linear Regression model on data and evaluate it. The implementation is Ordinary Least Squares (OLS) Linear Regression, provided by scikit-learn. The usage is as follows:

1. --eval_year (int): Evaluate the trained model on a specific year. If None, uses the train/test split. 

```rf.py --eval_year <int> --n_estomators <int> --max_depth <int>``` 

This script is used to fit a Random Forest Regression model on data and evaluate it. The random forest regressor differs from the other two methods, as it is an example of ensemble learning, and non-parametric learning. The implementation is provided by scikit-learn. The usage is as follows:

1. --eval_year (int): Evaluate the trained model on a specific year. If None, uses the train/test split. 

2. --n_estimators (int): Number of trees in the Random Forest

3. --max_depth (int): Maximum depth of the trees

```svr.py --eval_year <int> --kernel <str> --C <float> --epsilon <float>``` 

This script is used to fit a Support Vector Regressor model on data and evaluate it. The SVR is a max-margin regression method which famously uses the kernel trick (using kernel functions) to perform non-linear classification/regression. The kernel function transforms the data into higher dimensional feature space. The implementation is provided by scikit-learn. For info on the available kernel functions, visit their [docs](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVR.html). 

The usage is as follows:

1. --eval_year (int): Evaluate the trained model on a specific year. If None, uses the train/test split. 

2. --kernel (str): Kernel type for SVR (linear, poly, rbf, etc.)

3. --C (float): Regularization parameter for SVR

4. --epsilon (float): Epsilon in the epsilon-SVR model

## Results

Below are some results from running the experiments myself. 

### Experiments via train/test split

**Train Data: 2000-2020, Test Data: 2021-2024**

Linear Regression:
- MSE = 0.002
- R^2 = 0.902

SVR: 
- MSE = 0.002
- R^2 = 0.909

Random Forest Regressor:
- MSE = 0.002
- R^2 = 0.904

### Single Year Projections

**2025 Season win % Projections. Train Data: 2000-2024, Predictions: 2025 (as of 12/6)**

| Team | Actual W/L% | Predicted W/L% | Actual Wins | Predicted Wins | Projected Wins(82 games) |
| ---- | ----------- | -------------- | ----------- | -------------- | ------------------------ |
|Oklahoma City Thunder|0.773|0.741|17.0|16.31|60.762|
|Boston Celtics|0.826|0.705|19.0|16.22|57.810|
|Cleveland Cavaliers |0.870|0.701|20.0|16.12|57.482|
|Dallas Mavericks|0.652|0.653|15.0|15.03|53.546|
|New York Knicks|0.636|0.646|14.0|14.21|52.972|
