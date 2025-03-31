import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from scraper_utils import *

# scraper for https://www.basketball-reference.com/ 
# disallowed paths from their robots.txt
disallowed_paths = [
    '/basketball/', '/blazers/', '/dump/', '/fc/', '/my/', '/7103',
    '/play-index/*.cgi?*', '/play-index/plus/*.cgi?*', 
    '/gamelog/', '/splits/', '/on-off/', '/lineups/', '/shooting/',
    '/req/', '/short/', '/nocdn/'
]

def scrape_table_by_div_id(url, div_id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the div with the given id
        div = soup.find('div', id=div_id)
        
        if div:
            # Find the table within the div
            table = div.find('table')
            if table:
                return table
            else:
                print(f"No table found inside div with id: {div_id}")
        else:
            print(f"Div with id '{div_id}' not found.")
    else:
        print(f"Failed to retrieve the page, status code: {response.status_code}")
    return None

def parse_div_standings_table(url, div_id):
    table = scrape_table_by_div_id(url, div_id)
    if table is None: return None

    # table headers 
    headers = []
    for th in table.find_all('th'):
        headers.append(th.text.strip())
    
    # remove the division sub-headers, we dont need that
    substr = 'Division'
    headers = [item for item in headers if substr not in item]

    # table rows
    rows = []
    for tr in table.find_all('tr'):
        cells = tr.find_all(['td', 'th']) 
        row = [cell.text.strip() for cell in cells]  # Get the text from each cell
        if len(row) <= 1: # ignore 1 lengh row (subheader rows)
            continue

        if len(row) < len(headers):
            row.extend([None] * (len(headers) - len(row)))  # Fill missing cells w/ None
        
        rows.append(row)
    
    df = pd.DataFrame(rows[1:], columns=headers[:len(headers)])  # Use headers as column names
    return df

def get_div_standings(url, save=False):
    div_e = "all_divs_standings_E"
    div_w = "all_divs_standings_W"

    df_e = parse_div_standings_table(url, div_e)
    df_w = parse_div_standings_table(url, div_w)
    if df_e is None or df_w is None: return None

    # drop excess cols
    df_e = df_e.dropna(how='all', axis=1)
    df_w = df_w.dropna(how='all', axis=1)

    # rename conf columns
    df_e.rename(columns={"Eastern Conference": "Team"}, inplace=True)
    df_w.rename(columns={"Western Conference": "Team"}, inplace=True)

    df = pd.concat([df_e, df_w], axis=0, ignore_index=True)
    df['Team'] = df['Team'].str.replace('*', '', regex=False)
    
    # TODO: recalculate the GB column 
    df['W'] = pd.to_numeric(df['W'], errors='coerce')
    max_wins = df['W'].max()
    df['GB'] = (max_wins - df['W']) / 2

    if save:
        df.to_csv('./data/Standings_div.csv', index=False)

    return df

# Parse a conference standings table given a table object
def parse_conf_standings_table(url, div_id):
    # get bs4 table object
    table = scrape_table_by_div_id(url, div_id)
    if table is None: return None

    # Extract table headers
    headers = []
    for th in table.find_all('th'):
        headers.append(th.text.strip())
    
    # Extract table rows
    rows = []
    for tr in table.find_all('tr'):
        cells = tr.find_all(['td', 'th']) 
        row = [cell.text.strip() for cell in cells]  # Get the text from each cell

        if len(row) < len(headers):
            row.extend([None] * (len(headers) - len(row)))  # Fill missing cells w/ None
        rows.append(row)
    
    # Convert to DataFrame
    df = pd.DataFrame(rows[1:], columns=headers[:len(headers)])  # Use headers as column names
    df = df.dropna(how='all', axis=1)  # Drop empty columns

    return df

# Function to get the combined conference standings for east and west
def get_conf_standings(url, save=False):
    # Get df table for east and west conferences
    df_east = parse_conf_standings_table(url, "all_confs_standings_E")
    df_west = parse_conf_standings_table(url, "all_confs_standings_W")
    if df_east is None or df_west is None: return None

    # rename conference column title for concatenation
    df_east.rename(columns={"Eastern Conference": "Team"}, inplace=True)
    df_west.rename(columns={"Western Conference": "Team"}, inplace=True)

    df = pd.concat([df_east, df_west], axis=0, ignore_index=True)
    df['Team'] = df['Team'].str.replace('*', '', regex=False)

    # recalculate the GB column
    df['W'] = pd.to_numeric(df['W'], errors='coerce')
    max_wins = df['W'].max()
    df['GB'] = (max_wins - df['W']) / 2

    if save:
        df.to_csv('./data/Standings_conf.csv', index=False)

    return df

def get_per_game_stats(url, type="team", save=False):
    div_id = f"div_per_game-{type}"
    # scrape table
    table = scrape_table_by_div_id(url, div_id)
    if table is None: return None
    
    # table headers
    headers = []
    for th in table.find_all('th'):
        headers.append(th.text.strip())
    
    # table rows
    rows = []
    for tr in table.find_all('tr'):
        cells = tr.find_all(['td', 'th']) 
        row = [cell.text.strip() for cell in cells]  # Get the text from each cell

        if len(row) < len(headers):
            row.extend([None] * (len(headers) - len(row)))  # Fill missing cells w/ None
        rows.append(row)
    
    # to DataFrame
    df = pd.DataFrame(rows[1:], columns=headers[:len(headers)])  # Use headers as column names
    df = df.dropna(how='all', axis=1)  # Drop empty columns
    df['Team'] = df['Team'].str.replace('*', '', regex=False)

    if save:
        df.to_csv(f'./data/Per_Game_{type}.csv', index=False)

    return df

def get_per_100_stats(url, type="team", save=False):
    div_id = f"div_per_poss-{type}"
    # scrape table
    table = scrape_table_by_div_id(url, div_id)
    if table is None: return None

    # table headers
    headers = []
    for th in table.find_all('th'):
        headers.append(th.text.strip())

    # table rows
    rows = []
    for tr in table.find_all('tr'):
        cells = tr.find_all(['td', 'th']) 
        row = [cell.text.strip() for cell in cells]  # Get the text from each cell

        if len(row) < len(headers):
            row.extend([None] * (len(headers) - len(row)))  # Fill missing cells w/ None
        rows.append(row)
    
    # to DataFrame
    df = pd.DataFrame(rows[1:], columns=headers[:len(headers)])  # Use headers as column names
    df = df.dropna(how='all', axis=1)  # Drop empty columns
    df['Team'] = df['Team'].str.replace('*', '', regex=False)
    df = df.drop(columns=["MP"]) # drop the minutes played column

    if save:
        df.to_csv(f'./data/Per_100_{type}.csv', index=False)

    return df

def parse_adv_stats_table(url, div_id):
    table = scrape_table_by_div_id(url, div_id)
    if table is None: return None

    headers = []
    for th in table.find_all('th'):
        headers.append(th.text.strip())
    headers = headers[5:] # ignore the nested headers that show up first
    # label offensive and defensive four factors
    # ORB and DRB% don't need to be changed
    headers[headers.index("eFG%")] = "Off eFG%"
    headers[headers.index("TOV%")] = "Off TOV%"
    headers[headers.index("FT/FGA")] = "Off FT/FGA%"

    headers[headers.index("eFG%")] = "Def eFG%"
    headers[headers.index("TOV%")] = "Def TOV%"
    headers[headers.index("FT/FGA")] = "Def FT/FGA%"

    # table rows
    rows = []
    for tr in table.find_all('tr'):
        cells = tr.find_all(['td', 'th']) 
        row = [cell.text.strip() for cell in cells]
        if len(row) < len(headers):
            row.extend([None] * (len(headers) - len(row)))  # Fill missing cells w/ None
        rows.append(row)
    
    df = pd.DataFrame(rows[2:], columns=headers[:len(headers)]) # ignore first 2 rows b/c both are headers
    
    return df

def get_adv_stats(url, save=False):
    # final processing of the df
    df = parse_adv_stats_table(url, div_id="div_advanced-team")
    if df is None: return None
    
    df = df.dropna(how='all', axis=1) # drop empty cols
    df['Team'] = df['Team'].str.replace('*', '', regex=False)
    # drop columns with empty string
    df = df.drop(columns=[col for col in df.columns if col == ''])
    
    if save:
        df.to_csv('./data/Adv_Stats.csv', index=False)

    return df

def combine_headers(headers, parent_header, sub_header):
    for i, item in enumerate(headers):
        if item == sub_header:
            headers[i] = parent_header + " - " + sub_header
            break

def parse_headers(headers):
    # parse headers by combining the perent header into the sub headers and removing the parent headers
    # this must be done in order of appearance in the table to preserve the data
    
    # parse "% of FGA by distance" first
    p_header = "% of FGA By Distance"
    sub = ["2P", "0-3", "3-10", "10-16", "16-3P", "3P"]
    for s in sub:
        combine_headers(headers, p_header, s)
    
    # next parse "FG% By Distance"
    p_header = "FG% By Distance"
    sub = ["2P", "0-3", "3-10", "10-16", "16-3P", "3P"]
    for s in sub:
        combine_headers(headers, p_header, s)
    
    # next parse "% of FG Ast'd"
    p_header = "% of FG Ast'd"
    sub = ["2P", "3P"]
    for s in sub:
        combine_headers(headers, p_header, s)
    # parse "Dunks"
    p_header = "Dunks"
    sub = ["%FGA", "Md."]
    for s in sub:
        combine_headers(headers, p_header, s)
    # parse "Layups"
    p_header = "Layups"
    sub = ["%FGA", "Md."]
    for s in sub:
        combine_headers(headers, p_header, s)
    # parse "Corner"
    p_header = "Corner"
    sub = ["%3PA", "3P%"]
    for s in sub:
        combine_headers(headers, p_header, s)
    # parse "Heaves"
    p_header = "Heaves"
    sub = ["Att.", "Md."]
    for s in sub:
        combine_headers(headers, p_header, s)
    idx = headers.index("Rk")
    parsed_headers = headers[idx:] # slice headers arr to include only the ones we want (non-parent headers)
    
    return parsed_headers

def parse_shooting_stats_table(url, div_id):
    table = scrape_table_by_div_id(url, div_id)
    if table is None: return None

    headers = []
    for th in table.find_all('th'):
        headers.append(th.text.strip())
    headers = parse_headers(headers)

    # table rows
    rows = []
    for tr in table.find_all('tr'):
        cells = tr.find_all(['td', 'th']) 
        row = [cell.text.strip() for cell in cells]
        if len(row) < len(headers):
            row.extend([None] * (len(headers) - len(row)))  # Fill missing cells w/ None
        rows.append(row)

    df = pd.DataFrame(rows[2:], columns=headers[:len(headers)]) # ignore first 2 rows b/c both are headers
    return df

def get_shooting_stats(url, type="team", save=False):
    # type is either team or opponent
    div_id = f"div_shooting-{type}"
    df = parse_shooting_stats_table(url, div_id)
    if df is None: return None

    df = df.dropna(how='all', axis=1) # drop empty cols
    df['Team'] = df['Team'].str.replace('*', '', regex=False)
    # drop columns with empty string
    df = df.drop(columns=[col for col in df.columns if col == ''])

    if save:
        df.to_csv(f"./data/Shooting_Stats_{type}.csv", index=False)
    
    return df

if __name__ == "__main__":
    ### TEST USAGE - don't use this script. 
    # getting standings
    # df = get_conf_standings("https://www.basketball-reference.com/leagues/NBA_2024.html")

    # if df is not None:
    #     print(df.tail())

    # df = get_per_100_stats("https://www.basketball-reference.com/leagues/NBA_2024.html", type="team")
    # # print(df)
    # df = get_adv_stats("https://www.basketball-reference.com/leagues/NBA_2024.html", save=True)
    # # print(df.tail())
    # df = get_shooting_stats("https://www.basketball-reference.com/leagues/NBA_2024.html", save=True)
    # print(df.head())
    df = get_div_standings("https://www.basketball-reference.com/leagues/NBA_2024.html", save=True)
