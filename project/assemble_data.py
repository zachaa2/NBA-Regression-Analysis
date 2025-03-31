import pandas as pd
import numpy as np
import os
import argparse

# config for getting features of interest and filepaths
# this config is applied to each years' data in a specified range, and that data is compiled into one dataset
CONFIG = {
    "files": {
        "four_factors": {
            "file_pattern": "four_factors_{year}.csv", # file path to the data
            "columns": ["Team", "Four-Factor Score"]   # columns to load (should include at least Team)
        },
        "nrtg": {
            "file_pattern": "nrtg_{year}.csv",
            "columns": ["Team", "W", "L", "W/L%", "NRtg_norm"]
        },
        "srs": {
            "file_pattern": "srs_{year}.csv",
            "columns": ["Team", "SRS_norm"]
        }
    },
    # column names of the final compiled dataset
    "response_vars": ["W", "L", "W/L%"],
    "features": ["Four-Factor Score", "NRtg_norm", "SRS_norm"]
}

def load_csv(file_path, cols):
    """
    Load a CSV file and select given columns.
    
    Args:
        file_path (str): Path to CSV file.
        columns (list): List of columns to select.
    Returns:
        pd.DataFrame: DataFrame with selected columns.
    """
    try:
        df = pd.read_csv(file_path)
        return df[cols]
    except Exception as e:
        print(f"ERROR: Unable to process file: {file_path}")
        return None


def assemble_data(year, config, write=False):
    """
    Assemble data for a given year based on the provided configuration.
    
    Args:
        year (int): Year for which the data will be processed.
        config (dict): Configuration for file patterns and columns.
    Returns:
        pd.DataFrame: Combined DataFrame for the given year.
    """
    base_path = f"./data/{year}/"
    merged_data = None

    for key, file_info in config['files'].items():
        filepath = os.path.join(base_path, file_info['file_pattern'].format(year=year))
        df = load_csv(file_path=filepath, cols=file_info['columns'])
        
        if df is not None:
            # merge data based on team
            if merged_data is None:
                merged_data = df
            else:
                merged_data = pd.merge(merged_data, df, on='Team', how='inner')
    # write merged data (including team names) into year folders
    if write == True:
        merged_data.to_csv(f"./data/{year}/data_{year}.csv", index=False)

    if merged_data is not None:
        selected_cols = config['features'] + config['response_vars']
        return merged_data[selected_cols]
    else:
        print(f"ERROR: Failed to assemble data for year {year}.")
        return None

def save_dataset(dataset, file_path):
    """
    Save a dataset to a CSV file.
    
    Args:
        dataset (pd.DataFrame): The dataset to save.
        file_path (str): File path for the output CSV.
    """
    dataset.to_csv(file_path, index=False)
    print(f"Data saved to: {file_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train_years", type=str, default="2000-2020", help="Year range for training data (e.g., 2000-2015).")
    parser.add_argument("--test_years", type=str, default="2021-2024", help="Year range for testing data (e.g., 2016-2020).")
    parser.add_argument("--start_year", type=int, default=None, help="Start year for the dataset. Specify this and end year to compile one dataset for the given range")
    parser.add_argument("--end_year", type=int, default=None, help="End year for the dataset. Specify this and start year to compile one dataset for the given range")
    parser.add_argument("--write", action="store_true", help="Whether to write the yearly data as a csv to its respective data folder.")

    # parse params
    args = parser.parse_args()

    train_start, train_end = map(int, args.train_years.split("-"))
    test_start, test_end = map(int, args.test_years.split("-"))

    if not args.start_year and not args.end_year:

        # process train data
        train_data = []
        for year in range(train_start, train_end + 1):
            year_data = assemble_data(year=year, config=CONFIG, write=args.write)
            if year_data is not None:
                train_data.append(year_data)

        # process testing data
        test_data = []
        for year in range(test_start, test_end + 1):
            year_data = assemble_data(year=year, config=CONFIG, write=args.write)
            if year_data is not None:
                test_data.append(year_data)
    
        # save datasets
        if train_data:
            train_dataset = pd.concat(train_data, ignore_index=True)
            save_dataset(train_dataset, "./data/train_data.csv")
        else:
            print("No training data to save.")

        if test_data:
            test_dataset = pd.concat(test_data, ignore_index=True)
            save_dataset(test_dataset, "./data/test_data.csv")
        else:
            print("No testing data to save.")

    # process data from [start_year, end_year] as one dataset
    else:
        all_data = []
        for i in range(args.start_year, args.end_year+1):
            year_data = assemble_data(year=i, config=CONFIG, write=args.write)
            if year_data is not None:
                all_data.append(year_data)
        
        if all_data:
            all_dataset = pd.concat(all_data, ignore_index=True)
            save_dataset(all_dataset, "./data/data.csv")
        else:
            print("No data to save.")