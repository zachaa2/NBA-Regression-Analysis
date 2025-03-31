import pandas as pd
import matplotlib.pyplot as plt

fp = "../data/2024/adv_2024.csv"
df = pd.read_csv(fp)

df['W'] = pd.to_numeric(df['W'], errors="coerce")
df['NRtg'] = pd.to_numeric(df['NRtg'], errors="coerce")

# Plot Net Rating (Nrtg) vs Wins (W)
plt.figure(figsize=(8, 6))
plt.scatter(df['NRtg'], df['W'], color='blue')
plt.title('Net Rating (Nrtg) vs Wins (W)')
plt.xlabel('Net Rating (Nrtg)')
plt.ylabel('wins (W)')
plt.grid(True)
plt.savefig('../images/net_rating_vs_wins.png', format='png')
plt.show()
plt.close()

# Plot Wins (W) vs Age (Age as the x-axis)
plt.figure(figsize=(8, 6))
plt.scatter(df['Age'], df['W'], color='purple')
plt.title('Wins (W) vs Average Age')
plt.xlabel('Average Age')
plt.ylabel('Wins (W)')
plt.grid(True)
plt.savefig('../images/age_vs_wins.png', format='png')
plt.show()
plt.close()