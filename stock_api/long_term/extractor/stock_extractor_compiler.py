import pandas as pd
import os

def main():
    # Read the tickers from sample_tickers.csv
    tickers_df = pd.read_csv('sample_tickers.csv')
    
    master_data = []

    for ticker in tickers_df['tickers']:
        ticker = ticker.upper()
        filename = f"{ticker}.csv"

        if not os.path.isfile(filename):
            print(f"Warning: File {filename} does not exist. Skipping.")
            continue

        # Read the individual ticker CSV
        df = pd.read_csv(filename)

        # Select and rename the columns
        df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].copy()
        df.rename(columns={
            'Date': 'timestamp',
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Volume': 'volume'
        }, inplace=True)

        # Add the ticker column
        df['ticker'] = ticker

        # Format timestamp to add '00:00:00'
        df['timestamp'] = df['timestamp'] + ' 00:00:00'

        # Reorder columns
        df = df[['ticker', 'timestamp', 'open', 'high', 'low', 'close', 'volume']]

        master_data.append(df)

    if master_data:
        # Concatenate all dataframes
        master_df = pd.concat(master_data, ignore_index=True)

        # Save to master_stock_old.csv
        master_df.to_csv('master_stock_old.csv', index=False)
        print("master_stock_old.csv has been created successfully.")
    else:
        print("No data to write.")

if __name__ == "__main__":
    main()
