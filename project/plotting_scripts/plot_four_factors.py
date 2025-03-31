import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse
import os



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start_year", type=int, default=2024, help="Start year to fetch data from")
    parser.add_argument("--end_year", type=int, default=2024, help="End year to fetch data from")
    parser.add_argument("--year", type=int, default=None, help="Year to fetch data from (if no date range is needed). Leave blank if a range is needed")
    
    # parse arguments
    args = parser.parse_args()

    start_yr = args.start_year
    end_yr = args.end_year
    if args.year is not None:
        start_yr = args.year
        end_yr = args.year

    data_dir = "../data"
    output_dir = "../images"

    combined_df = pd.DataFrame()
    for year in range(start_yr, end_yr + 1):

        file_path = os.path.join(data_dir, str(year), f"four_factors_{year}.csv")
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue

        # add year's data to total data    
        year_df = pd.read_csv(file_path)
        year_df['Year'] = year
        combined_df = pd.concat([combined_df, year_df], ignore_index=True)

    if combined_df.empty:
        print("No data loaded. Exiting.")
        exit()

    # check for required columns
    required_columns = ['W/L%', 'Offensive Score', 'Defensive Score']
    if not all(col in combined_df.columns for col in required_columns):
        print(f"Required columns ({', '.join(required_columns)}) not found in the dataset. Exiting.")
        exit()
    
    # pairwise scatterplots: offensive/defensive four factors vs win%
    offensive_factors = ['Off eFG%', 'Off TOV%', 'ORB%', 'Off FT/FGA%']
    defensive_factors = ['Def eFG%', 'Def TOV%', 'DRB%', 'Def FT/FGA%']

    # off factors
    sns.pairplot(combined_df, x_vars=offensive_factors, y_vars='W/L%', kind='reg')
    plt.suptitle("Pairwise Scatterplots: Offensive Four Factors vs Win%", y=1.02)

    offensive_scatterplot_path = os.path.join(output_dir, "offensive_factors_scatterplots.png")
    plt.savefig(offensive_scatterplot_path, bbox_inches='tight')
    plt.show()
    print(f"Offensive factors scatterplots saved to: {offensive_scatterplot_path}")

    # def factors
    sns.pairplot(combined_df, x_vars=defensive_factors, y_vars='W/L%', kind='reg')
    plt.suptitle("Pairwise Scatterplots: Defensive Four Factors vs Win%", y=1.02)

    defensive_scatterplot_path = os.path.join(output_dir, "defensive_factors_scatterplots.png")
    plt.savefig(defensive_scatterplot_path, bbox_inches='tight')
    plt.show()
    print(f"Defensive factors scatterplots saved to: {defensive_scatterplot_path}")

    # correlation heatmap   
    relevant_columns = offensive_factors + defensive_factors + ['W/L%']
    correlation_matrix = combined_df[relevant_columns].corr()

    plt.figure(figsize=(12, 10))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title("Correlation Heatmap: Offensive, Defensive Factors and Win%")

    heatmap_path = os.path.join(output_dir, "4factors_correlation_heatmap.png")
    plt.savefig(heatmap_path, bbox_inches='tight')
    plt.show()
    print(f"Correlation heatmap saved to: {heatmap_path}")


    # offensive fouir factor score vs Win%
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=combined_df, x='Offensive Score', y='W/L%', edgecolor='k')
    plt.title("Offensive Four-Factor Score vs Win%")
    plt.xlabel("Offensive Four-Factor Score")
    plt.ylabel("Win%")

    offensive_score_path = os.path.join(output_dir, "offensive_score_vs_win_percent.png")
    plt.savefig(offensive_score_path, bbox_inches='tight')
    plt.show()
    print(f"Offensive score vs Win% plot saved to: {offensive_score_path}")

    # defensive four factor score vs Win%
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=combined_df, x='Defensive Score', y='W/L%', edgecolor='k')
    plt.title("Defensive Four-Factor Score vs Win%")
    plt.xlabel("Defensive Four-Factor Score")
    plt.ylabel("Win%")

    defensive_score_path = os.path.join(output_dir, "defensive_score_vs_win_percent.png")
    plt.savefig(defensive_score_path, bbox_inches='tight')
    plt.show()
    print(f"Defensive score vs Win% plot saved to: {defensive_score_path}")

    # tot four factor score vs win%
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=combined_df, x='Four-Factor Score', y='W/L%', edgecolor='k')
    plt.title("Four-Factor Score vs Win%")
    plt.xlabel("Four-Factor Score")
    plt.ylabel("Win%")

    overall_score_path = os.path.join(output_dir, "4factor_score_vs_win_percent.png")
    plt.savefig(overall_score_path, bbox_inches='tight')
    plt.show()
    print(f"Overall score vs Win% plot saved to: {overall_score_path}")