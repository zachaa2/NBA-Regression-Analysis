import pandas as pd
import numpy
import os
import argparse


def standardize_nrtg(year):
    """
    Standardize the NRtg for a given year. The standardization is done to adjust the different scales between years 
    to something more uniform (zscore normalization like)

    Args:
        year (int): Year for which the data will be processed.
    """
    csv_path = f"./data/{year}/adv_{year}.csv"
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)

        if "NRtg" in df.columns:
            nrtg_std = df['NRtg'].std()
            
            df['NRtg_norm'] = df['NRtg'] / nrtg_std
            df["W/L%"] = (df["W"] / (df["W"] + df["L"])).round(3)

            outcols = ["Team", "W", "L", "W/L%", "NRtg", "NRtg_norm"]
            outdf = df[outcols]

            outpath = f"./data/{year}/nrtg_{year}.csv"
            outdf.to_csv(outpath, index=False)
            print(f"Processed and saved to: {outpath}")
        else:
            print(f"ERROR: Skipped {csv_path}: 'NRtg' column not found.")
    else:
        print(f"ERROR: File {csv_path} not found.")


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

    for i in range(start_yr, end_yr + 1):
        standardize_nrtg(year=i)