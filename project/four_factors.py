import pandas as pd
import argparse
import os

def normalize_data(df, method, cols):
    """
    Normalize the specified columns in the DataFrame using the specified method.

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        method (str): Normalization method ('zscore', 'min-max', 'centered').
        cols (list): List of column names to normalize.

    Returns:
        pd.DataFrame: DataFrame with normalized columns.
    """
    if method == 'zscore':
        return df[cols].apply(lambda x: (x - x.mean()) / x.std())
    elif method == 'min-max':
        return df[cols].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
    elif method == 'centered':
        return df[cols].apply(lambda x: x - x.mean())
    else:
        raise ValueError(f"Normalization method {method} not supported")

def calculate_four_factor_score(df, weights, factors):
    """
    Calculate a weighted score for specified factors.

    Parameters:
        df (pd.DataFrame): DataFrame containing the factors.
        weights (dict): Dictionary mapping factors to their weights.
        factors (list): List of factor column names.

    Returns:
        pd.Series: Series of scores.
    """
    return sum(weights[factor] * df[factor] for factor in factors)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start_year", type=int, default=2024, help="Start year to fetch data from")
    parser.add_argument("--end_year", type=int, default=2024, help="End year to fetch data from")
    parser.add_argument("--year", type=int, default=None, help="Year to fetch data from (if no date range is needed). Leave blank if a range is needed")
    parser.add_argument("--norm", type=str, default="zscore", choices=["zscore", "min-max", "centered"],
                        help="Normalization method to use on the four factors")

    # parse params
    args = parser.parse_args()

    start_yr = args.start_year
    end_yr = args.end_year
    if args.year is not None:
        start_yr = args.year
        end_yr = args.year

    offensive_factors = ["Off eFG%", "Off TOV%", "ORB%", "Off FT/FGA%"]
    defensive_factors = ["Def eFG%", "Def TOV%", "DRB%", "Def FT/FGA%"]
    # weights for score calculation
    weights = {
        "Off eFG%": 0.40, "Off TOV%": -0.25, "ORB%": 0.20, "Off FT/FGA%": 0.15,
        "Def eFG%": -0.40, "Def TOV%": 0.25, "DRB%": 0.20, "Def FT/FGA%": -0.15
    }

    for i in range(start_yr, end_yr + 1):
        path = f"./data/{i}/adv_{i}.csv" # path of adv stats table
        # load csv and transform data
        if not os.path.exists(path=path):
            print(f"File not found: {path}")
            continue

        df = pd.read_csv(path)
        df = df.iloc[:-1] # ignore leageue avg row

        all_factors = offensive_factors + defensive_factors

        try:
            normalized_factors = normalize_data(df, args.norm, all_factors).round(6)

            # make new df and copy over cols
            normalized_df = pd.DataFrame()
            normalized_df['Team'] = df['Team']  
            normalized_df['W'] = df['W']
            normalized_df['L'] = df['L']
            normalized_df['W/L%'] = (df['W'] / (df['W'] + df['L'])).round(6)

            # add normalized off/def four factors
            for col in all_factors:
                normalized_df[col] = normalized_factors[col]

            # off/def four factor score calculation
            normalized_df['Offensive Score'] = calculate_four_factor_score(normalized_df, weights, offensive_factors).round(6)
            normalized_df['Defensive Score'] = calculate_four_factor_score(normalized_df, weights, defensive_factors).round(6)
            normalized_df['Four-Factor Score'] = (normalized_df['Offensive Score'] + normalized_df['Defensive Score']).round(6)
            

            # write to csv
            outpath = f"./data/{i}/four_factors_{i}.csv"
            normalized_df.to_csv(outpath, index=False)
            print(f"Four factors for year {i} saved to: {outpath}")
                
        except ValueError as e:
            print(e)
            continue
