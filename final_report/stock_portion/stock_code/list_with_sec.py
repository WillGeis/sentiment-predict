import pandas as pd

master_df = pd.read_csv('master_stocks.csv')
stock_info_df = pd.read_csv('stock_data.csv')
master_df.columns = master_df.columns.str.strip()
stock_info_df.columns = stock_info_df.columns.str.strip()
unique_tickers = master_df['ticker'].unique()
filtered_stock_info = stock_info_df[stock_info_df['Symbol'].isin(unique_tickers)]
ticker_sector_df = filtered_stock_info[['Symbol', 'Sector']].drop_duplicates()
ticker_sector_df = ticker_sector_df.rename(columns={'Symbol': 'ticker', 'Sector': 'sector'})
ticker_sector_df.to_csv('tickers_with_sectors.csv', index=False)

print("Filtered ticker-sector pairs written to tickers_with_sectors.csv")
