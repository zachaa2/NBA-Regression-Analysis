import pandas as pd
import matplotlib.pyplot as plt
import os
import argparse


def plot_srs_vs_win_percentage(start_year, end_year, save=False):
    """
    Plots normalized SRS (SRS_norm) vs Win Percentage (W/L%) for a range of years.
    
    Args:
        start_year (int): Start year of the range.
        end_year (int): End year of the range.
        save (bool): Whether to save the plot as an image.
    """
    plt.figure(figsize=(10, 6))
    aggregated_data = []

    # read and combine data
    for year in range(start_year, end_year + 1):
        file_path = f"../data/{year}/srs_{year}.csv"
        if os.path.exists(file_path):
            # load data
            df = pd.read_csv(file_path)

            # check the cols
            if "SRS_norm" in df.columns and "W/L%" in df.columns:
                df["W/L%"] = df["W/L%"] * 100
                # aggregate
                aggregated_data.append(df[["SRS_norm", "W/L%"]])
            else:
                print(f"ERROR: Missing necessary columns in {file_path}.")
        else:
            print(f"ERROR: File {file_path} not found.")

    # plot
    if aggregated_data:
        # combine to one df
        aggregated_df = pd.concat(aggregated_data, ignore_index=True)

        # scatter plot
        plt.scatter(aggregated_df["SRS_norm"], aggregated_df["W/L%"], alpha=0.7, label="Aggregated Data")
        plt.title("Normalized SRS vs Win Percentage")
        plt.xlabel("Normalized SRS")
        plt.ylabel("W/L%")
        plt.axhline(50, color='gray', linestyle='--', alpha=0.7, label="50% Win Percentage")
        plt.grid(alpha=0.5)
        plt.legend(loc='best')

        # save
        if save:
            save_path = f"../images/srs_vs_win_percent.png"
            os.makedirs("../images", exist_ok=True)
            plt.savefig(save_path, dpi=300)
            print(f"Plot saved: {save_path}")
        else:
            plt.show()
    else:
        print("No data to plot.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start_year", type=int, default=2024, help="Start year to fetch data from")
    parser.add_argument("--end_year", type=int, default=2024, help="End year to fetch data from")
    parser.add_argument("--save", action='store_true', help="Save the plot instead of showing it")
    parser.add_argument("--year", type=int, default=None, help="Year to fetch data from (if no date range is needed). Leave blank if a range is needed")

    # Parse arguments
    args = parser.parse_args()
    start_year = args.start_year
    end_year = args.end_year
    if args.year is not None:
        start_yr = args.year
        end_yr = args.year

    save_plot = args.save

    # Plot the data
    plot_srs_vs_win_percentage(start_year, end_year, save=save_plot)