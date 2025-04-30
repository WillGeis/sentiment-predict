import pandas as pd

# load files
master_df = pd.read_csv('master_stocks.csv')
stock_info_df = pd.read_csv('stock_data.csv')

master_df.columns = master_df.columns.str.strip()
stock_info_df.columns = stock_info_df.columns.str.strip()
symbol_to_sector = stock_info_df.set_index('Symbol')['Sector'].to_dict()
master_df['Sector'] = master_df['ticker'].map(symbol_to_sector)

# DataFrame to CSV
master_df.to_csv('master_stock_data_sectors.csv', index=False)

print("Output written to master_stock_data_sectors.csv")
