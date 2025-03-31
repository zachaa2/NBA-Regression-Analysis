import pandas as pd
import matplotlib.pyplot as plt

# Load the two CSV files
ff_df = pd.read_csv('../data/2024/four_factors_2024.csv')  # Replace with the actual path if necessary
srs_df = pd.read_csv('../data/2024/srs_2024.csv')    # Replace with the actual path if necessary

# Merge the two dataframes based on the 'Team' column
merged_df = pd.merge(ff_df, srs_df, on="Team")

# Plot NRtg_norm vs SRS_norm to illustrate multicollinearity
plt.figure(figsize=(10, 6))
plt.scatter(merged_df['Four-Factor Score'], merged_df['SRS_norm'], alpha=0.7)
plt.title("Four Factor Score vs SRS", fontsize=16)
plt.xlabel("4Factors", fontsize=14)
plt.ylabel("SRS", fontsize=14)
plt.grid(True)
plt.savefig("../images/4factor_vs_srs.png")
plt.close()
