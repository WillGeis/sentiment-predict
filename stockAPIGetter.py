import requests
import csv

class stockAPIGetter:
    def __init__(self, tickers_filename="stock-tickers.csv"):
        print("ApiGetter initialized")
        self.tickers_filename = tickers_filename  # CSV file with stock symbols

    def get_tickers_from_csv(self):
        """Read ticker symbols from CSV."""
        tickers = []
        try:
            with open(self.tickers_filename, mode="r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    tickers.append(row['Symbol'])  # Assuming the column name is 'Symbol'
        except FileNotFoundError:
            print(f"Error: File '{self.tickers_filename}' not found.")
        return tickers

    def fetch_and_save_data(self, symbol):
        """Fetch stock data for a specific symbol and save it to CSV."""
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey=GKZD4Y2REDV5QML2'

        # Make the API call
        response = requests.get(url)
        data = response.json()

        # Get the symbol from metadata
        meta_data = data.get("Meta Data", {})
        symbol = meta_data.get("2. Symbol", "UNKNOWN")

        # Parse and extract time series data
        time_series = data.get("Time Series (5min)")
        if not time_series:
            print(f"Error: No time series data found for {symbol}. Skipping...")
            return

        # Write to CSV for each symbol
        with open(f"{symbol}_stock_data.csv", mode="w", newline="") as csv_file:
            fieldnames = ["ticker", "timestamp", "open", "high", "low", "close", "volume"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            for timestamp, values in time_series.items():
                writer.writerow({
                    "ticker": symbol,
                    "timestamp": timestamp,
                    "open": values["1. open"],
                    "high": values["2. high"],
                    "low": values["3. low"],
                    "close": values["4. close"],
                    "volume": values["5. volume"]
                })

    def run(self):
        print("Running ApiGetter...")

        # Get list of tickers from CSV
        tickers = self.get_tickers_from_csv()

        # For each ticker, fetch and save the stock data
        for symbol in tickers:
            print(f"Fetching data for {symbol}...")
            self.fetch_and_save_data(symbol)
