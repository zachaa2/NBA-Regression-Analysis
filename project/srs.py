import pandas as pd
import os
import numpy as np
import argparse

def standardize_srs(year):
    """
    Standardizes the Simple Rating system metric for a given year. The mean for a given year will always be 0, but
    the spread can vary a good amount from year to year. The standardization is done to adjust the different scales between years 
    to something more uniform (zscore normalization like)

    Args:
        year (int): Year for which the data will be processed.
    """
    csv_path = f"./data/{year}/standings_{year}.csv"
    df = pd.read_csv(csv_path)
    if "SRS" in df.columns:
        srs_std = df['SRS'].std()
        df['SRS_norm'] = df['SRS'] / srs_std

        # output cols
        output_cols = ['Team', 'W', 'L', "W/L%", 'SRS_norm']
        outdf = df[output_cols]
        outpath = f'./data/{year}/srs_{year}.csv'
        outdf.to_csv(outpath, index=False)
        print(f"Processed and saved: {outpath}")
    else:
        print(f"ERROR: Skipped {csv_path}: 'SRS' column not found.")




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start_year", type=int, default=2024, help="Start year to fetch data from")
    parser.add_argument("--end_year", type=int, default=2024, help="End year to fetch data from")
    parser.add_argument("--year", type=int, default=None, help="Year to fetch data from (if no date range is needed). Leave blank if a range is needed")

    # parse params
    args = parser.parse_args()

    start_yr = args.start_year
    end_yr = args.end_year
    if args.year is not None:
        start_yr = args.year
        end_yr = args.year

    for i in range(start_yr, end_yr+1):
        standardize_srs(year=i)