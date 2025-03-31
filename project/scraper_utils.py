import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

disallowed_paths = [
    '/basketball/', '/blazers/', '/dump/', '/fc/', '/my/', '/7103',
    '/play-index/*.cgi?*', '/play-index/plus/*.cgi?*', 
    '/gamelog/', '/splits/', '/on-off/', '/lineups/', '/shooting/',
    '/req/', '/short/', '/nocdn/'
]

def is_allowed(url):
    for path in disallowed_paths:
        if path in url:
            return False
    return True


def scrape_all_tables(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all tables in the HTML
        tables = soup.find_all('table')
        dataframes = []
        
        for i, table in enumerate(tables):
            # Attempt to get table caption if it exists
            caption = table.find('caption')
            table_name = caption.text.strip() if caption else None
            
            # If there's no caption, try to get the closest preceding heading (like h2, h3, etc.)
            if not table_name:
                previous_sibling = table.find_previous(['h2', 'h3', 'h4'])
                if previous_sibling:
                    table_name = previous_sibling.text.strip()
            
            print(f"Table {i + 1} Title: {table_name}")
            tables_to_skip = ["Advanced Stats Table", "Shooting Stats Table"]
            # Having trouble parsing tables with nested headers, skipping for now
            if table_name and table_name in tables_to_skip:
                print(f"Skipping table: {table_name}")
                continue
            
            # Extract the first header row
            first_header_row = table.find_all('tr')[0]
            headers = [th.text.strip() for th in first_header_row.find_all(['th', 'td'])]
            
            # Extract the data rows, skipping the first header row
            rows = []
            for tr in table.find_all('tr')[1:]:  # Skip the first header row
                cells = tr.find_all(['td', 'th'])
                row = [cell.text.strip() for cell in cells]
                
                # Adjust row length to match the headers length
                if len(row) > len(headers):
                    row = row[:len(headers)]  # Truncate extra cells
                elif len(row) < len(headers):
                    row.extend([None] * (len(headers) - len(row)))  # Pad with None
                
                rows.append(row)
            
            # Convert the rows to a DataFrame
            df = pd.DataFrame(rows, columns=headers[:len(headers)])
            
            # Remove columns where all values are empty
            df = df.dropna(how='all', axis=1)
            
            # add to list and save DataFrame to a CSV file
            dataframes.append(df)

            df.to_csv(f'scraped_table_{i + 1}.csv', index=False)
            print(f"Table {i + 1} scraped and saved to scraped_table_{i + 1}.csv")
            
            # crawl-delay
            time.sleep(3)
        
        return dataframes
    else:
        print(f"Failed to retrieve the page, status code: {response.status_code}")
    return None


def scrape_table(url, table_name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)  
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all tables in the HTML
        tables = soup.find_all('table')
        found_names = []  # To store all table names found on the page
        
        for table in tables:
            # Attempt to get table caption if it exists
            caption = table.find('caption')
            found_table_name = caption.text.strip() if caption else None
            
            # If no caption, try to get the closest preceding heading (like h2, h3, etc.)
            if not found_table_name:
                previous_sibling = table.find_previous(['h2', 'h3', 'h4'])
                if previous_sibling:
                    found_table_name = previous_sibling.text.strip()
            
            # Collect all found table names
            if found_table_name:
                found_names.append(found_table_name)
            
            # Check if this is the table we're looking for
            if found_table_name and table_name.lower() in found_table_name.lower():
                print(f"Found table: {found_table_name}")
                
                # Extract table headers
                headers = []
                for th in table.find_all('th'):
                    headers.append(th.text.strip())

                rows = []
                for tr in table.find_all('tr'):
                    cells = tr.find_all(['td', 'th'])  # Finds both <td> and <th>
                    row = [cell.text.strip() for cell in cells]
                    
                    # Append None for missing cells
                    if len(row) < len(headers):
                        row.extend([None] * (len(headers) - len(row)))
                    
                    rows.append(row)
                
                # Convert the rows to a DataFrame
                df = pd.DataFrame(rows[1:], columns=headers[:len(rows[0])])  # Ensure column length matches row length
                df = df.dropna(how='all', axis=1) # remove null columns 
                return df
        
        # If no table was found, output the available table names
        print(f"Table '{table_name}' not found.")
        if found_names:
            print("Available tables:")
            for name in found_names:
                print(f"- {name}")
        else:
            print("No table names were found on the page.")
    else:
        print(f"Failed to retrieve the page, status code: {response.status_code}")
    return None


def scrape_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    if not is_allowed(url):
        print(f"Skipping disallowed URL: {url}")
        return

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract here
        title = soup.title.text
        print(f"Page title: {title}")
        print(soup.prettify())
    else:
        print(f"Failed to retrieve {url}, status code: {response.status_code}")
    
    time.sleep(3)

if __name__ == "__main__":
    # usage
    # scrape_page("https://www.basketball-reference.com/leagues/NBA_2024.html#per_game-team")

    # url = "https://www.basketball-reference.com/leagues/NBA_2024.html#per_game-team"
    # tables = scrape_all_tables(url)

    # if tables is not None:
    #     for i, df in enumerate(tables):
    #         print(f"DataFrame for Table {i + 1}:")
    #         print(df.head())
    pass