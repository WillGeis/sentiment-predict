import pandas as pd

# Replace these with the actual file paths
stock_data_csv = "master_stocks.csv"
sector_data_csv = "tickers_with_sectors.csv"
output_csv = "master_stock_sec.csv"

# Load the CSV files
stock_df = pd.read_csv(stock_data_csv)
sector_df = pd.read_csv(sector_data_csv)

# Drop rows with any missing values in either DataFrame
stock_df.dropna(inplace=True)
sector_df.dropna(inplace=True)

# Merge the cleaned DataFrames on 'ticker'
merged_df = pd.merge(stock_df, sector_df, on="ticker", how="left")

# Drop rows that still contain any missing values after merge (e.g., missing sector)
merged_df.dropna(inplace=True)

# Save the final cleaned and merged DataFrame
merged_df.to_csv(output_csv, index=False)

print(f"Cleaned and merged CSV saved as '{output_csv}'")
