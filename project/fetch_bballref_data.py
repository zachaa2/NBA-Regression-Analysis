import time
import pandas as pd
from scraper import *
import argparse
import os

def get_df(val, url):
    match val:
        case "standings":
            df = get_conf_standings(url)
            if df is not None:
                return df
            else:
                return get_div_standings(url)
        case "per_game_team":
            return get_per_game_stats(url, type="team")
        case "per_game_opp":
            return get_per_game_stats(url, type="opponent")
        case "per_100_team":
            return get_per_100_stats(url, type="team")
        case "per_100_opp":
            return get_per_100_stats(url, type="opponent")
        case "adv":
            # TODO: Add distinction between the off and def 4 factors columns, some have the same name
            return get_adv_stats(url)
        case "shooting":
            return get_shooting_stats(url, type="team")
        case _:
            return None

def fetch_season_data(start_year, end_year, tables):
    # fetch the csv data for the requested tables for each year
    for i in range(start_year, end_year + 1):
        url = f"https://www.basketball-reference.com/leagues/NBA_{i}.html" # url to parse
        # make folders if needed
        dir_path = f"./data/{i}"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        
        # fetch and save table data
        for j in range(len(tables)):
            # file name
            f_name= f"{tables[j]}_{i}.csv"
            f_path = os.path.join(dir_path, f_name)

            # get parsed data frame and save
            df = get_df(tables[j], url)
            if df is not None:
                print(f"Saving table {tables[j]} for year {i}.")
                df.to_csv(f_path, index=False)
            else:
                print(f"No table for {tables[j]} found for year {i}. Continuing...")

            time.sleep(3) # respect robots.txt crawl delay



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start_year", type=int, default=2024, help="Start year to fetch data from")
    parser.add_argument("--end_year", type=int, default=2024, help="End year to fetch data from")
    parser.add_argument("--year", type=int, default=None, help="Year to fetch data from (if no date range is needed). Leave blank if a range is needed")
    parser.add_argument("--table", type=str, default=None, help="Tables to fetch (if None, then fetch all)", 
                        choices=["per_100_team", "per_game_team", "standings", "adv", "shooting", "per_100_opp", "per_game_opp"])

    # parse params
    args = parser.parse_args()
    tables = None
    if args.table is None:
        tables = ["standings", "per_100_team", "per_100_opp", "adv", "shooting", "per_game_team", "per_game_opp"]
    else:
        tables = [args.table]

    start_yr = args.start_year
    end_yr = args.end_year
    if args.year is not None:
        start_yr = args.year
        end_yr = args.year
    
    fetch_season_data(start_year=start_yr, end_year=end_yr, tables=tables)