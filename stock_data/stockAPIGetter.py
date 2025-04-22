import requests
import csv
import os
import time

class stockAPIGetter:
    def __init__(self, tickers_filename="stock-tickers.csv", output_filename="stocks.csv"):
        print("ApiGetter initialized")
        self.tickers_filename = tickers_filename
        self.output_filename = output_filename
        self.header_written = os.path.exists(self.output_filename)  # Check if file already exists

    def get_tickers_from_csv(self):
        tickers = []
        try:
            with open(self.tickers_filename, mode="r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    tickers.append(row['Symbol'])
        except FileNotFoundError:
            print(f"Error: File '{self.tickers_filename}' not found.")
        return tickers

    def fetch_and_append_data(self, symbol):
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=30min&apikey=GKZD4Y2REDV5QML2'

        max_retries = 5
        retry_delay = 5400  # seconds, 1.5 hours

        for attempt in range(max_retries):
            response = requests.get(url)
            data = response.json()

            # Check if we got rate-limited or there's some other error
            if "Meta Data" not in data or "Time Series (30min)" not in data:
                print(f"[Attempt {attempt + 1}] API limit hit or bad response. Waiting {retry_delay / 60} minutes...")
                time.sleep(retry_delay)
            else:
                break
        else:
            print(f"Failed to fetch data for {symbol} after {max_retries} retries.")
            return

        print(f"Fetched data for: {data['Meta Data'].get('2. Symbol', 'UNKNOWN')}")

        meta_data = data.get("Meta Data", {})
        symbol = meta_data.get("2. Symbol", "UNKNOWN")
        time_series = data.get("Time Series (30min)")

        if not time_series:
            print(f"No time series data found for {symbol}.")
            return

        write_header = not self.header_written
        with open(self.output_filename, mode="a", newline="") as csv_file:
            fieldnames = ["ticker", "timestamp", "open", "high", "low", "close", "volume"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            if write_header:
                writer.writeheader()
                self.header_written = True

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

        tickers = self.get_tickers_from_csv()
        if not tickers:
            print("No tickers to process.")
            return

        # Clear existing file if needed
        if os.path.exists(self.output_filename):
            os.remove(self.output_filename)
            self.header_written = False

        for symbol in tickers:
            print(f"Fetching data for {symbol}...")
            self.fetch_and_append_data(symbol)