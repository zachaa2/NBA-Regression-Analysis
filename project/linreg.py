import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import argparse
import numpy as np

def load_data(train_path, test_path):
    """
    Load training and testing data from CSV files.

    Args:
        train_path (str): Path to the training CSV file.
        test_path (str): Path to the testing CSV file.
    Returns:
        tuple: training and testing data as Pandas DataFrames.
    """
    train_data = pd.read_csv(train_path)
    test_data = pd.read_csv(test_path)
    return train_data, test_data


def train_linear_regression(train_data, features, response_var):
    """
    Train a linear regression model.

    Args:
        train_data (pd.DataFrame): Training dataset.
        features (list): List of feature column names.
        response_var (str): Name of the response variable column.
    Returns:
        LinearRegression: Trained linear regression model.
    """
    X_train = train_data[features]
    y_train = train_data[response_var]

    model = LinearRegression()
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, test_data, features, response_var):
    """
    Evaluate the linear regression model on the testing data.

    Args:
        model (LinearRegression): Trained linear regression model.
        test_data (pd.DataFrame): Testing dataset.
        features (list): List of feature column names.
        response_var (str): Name of the response variable column.
    Returns:
        dict: Evaluation metrics including MSE and R^2 score.
    """
    X_test = test_data[features]
    y_test = test_data[response_var]

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse) 
    r2 = r2_score(y_test, y_pred)

    return {"RMSE": rmse, "R2": r2}


def evaluate_specific_year(year, model, features, response_var):
    """
    Evaluate the model on a specific year's data and keep team names for comparison.

    Args:
        year (int): Year for evaluation.
        model (LinearRegression): Trained linear regression model.
        features (list): List of feature column names.
        response_var (str): Name of the response variable column.
    Returns:
        pd.DataFrame: DataFrame with team names, actual values, and predicted values.
    """
    file_path = f"./data/{year}/data_{year}.csv"

    try:
        # Load the data for the specific year
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"ERROR: File not found: {file_path}")
        return None

    # prepare data
    X = df[features]
    y_actual = df[response_var]
    team_names = df["Team"]
    actual_wins = df['W']
    tot_games = df['W'] + df['L']

    # make predictions
    y_pred = model.predict(X)

    # get predicted wins
    pred_wins = tot_games * y_pred

    # other metrics
    mse = mean_squared_error(y_actual, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_actual, y_pred)
    metrics = {
        "RMSE": rmse,
        "R2": r2
    }

    # combine results into a DataFrame
    results = pd.DataFrame({
        "Team": team_names,
        "Actual Win%": y_actual,
        "Predicted Win%": y_pred,
        "Actual Wins": actual_wins,
        "Predicted Wins": pred_wins.round(2)
    })
    return results, metrics


if __name__ == "__main__":
    # args
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval_year", type=int, default=None, help="Evaluate the trained model on a specific year")
    args = parser.parse_args()

    # load train and test data
    train_path = "./data/train_data.csv"
    test_path = "./data/test_data.csv"
    train_data, test_data = load_data(train_path, test_path)

    # features and response variable
    FEATURES = ["Four-Factor Score", "NRtg_norm", "SRS_norm"]
    RESPONSE_VAR = "W/L%"  # Using Win% as the response variable

    if args.eval_year is not None:
        # use single compiled set for training when evaluating on one year
        full_data = pd.read_csv("./data/data.csv")

        # Train the model on the entire dataset
        model = train_linear_regression(full_data, FEATURES, RESPONSE_VAR)

        # Evaluate the model on the specific year
        year_res, year_metrics = evaluate_specific_year(args.eval_year, model, FEATURES, RESPONSE_VAR)
        if year_res is not None:
                print(f"\nEvaluation Results for {args.eval_year}:")
                print(year_res)
                print(f"\nMetrics for {args.eval_year}:")
                print(f"Root Mean Squared Error (RMSE): {year_metrics['RMSE']:.3f}")
                print(f"R^2 Score: {year_metrics['R2']:.3f}")
    else:
        # use train/test sets when not evaluating for a specific year
        train_path = "./data/train_data.csv"
        test_path = "./data/test_data.csv"

        # Load training and testing data
        train_data, test_data = load_data(train_path, test_path)

        # Train the model on the training dataset
        model = train_linear_regression(train_data, FEATURES, RESPONSE_VAR)

        # Evaluate the model on the testing dataset
        metrics = evaluate_model(model, test_data, FEATURES, RESPONSE_VAR)

        # Print evaluation results
        print("Model Evaluation on Test Set:")
        print(f"Root Mean Squared Error (RMSE): {metrics['RMSE']:.3f}")
        print(f"R^2 Score: {metrics['R2']:.3f}")