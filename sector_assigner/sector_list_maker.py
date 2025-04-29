import pandas as pd

# Load the stock data
stock_df = pd.read_csv('stock_data.csv')
stock_df.columns = stock_df.columns.str.strip()
unique_sectors = stock_df['Sector'].dropna().unique()
sectors_df = pd.DataFrame(unique_sectors, columns=['sector'])
sectors_df.to_csv('unique_sectors.csv', index=False)

print("Unique sectors written to unique_sectors.csv")
