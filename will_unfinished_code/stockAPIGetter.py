import requests
import csv
import os
import time
from stockCSVDownloader import stockCSVDownloader
from lastStockPrinter import lastStockPrinter

class stockAPIGetter:
    def __init__(self, count, tickers_filename="stock-tickers.csv", output_filename="stocks.csv"):
        print("ApiGetter initialized")
        self.tickers_filename = tickers_filename
        self.output_filename = output_filename
        self.count = count
        self.header_written = os.path.exists(self.output_filename)

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
        keys = [
            'GKZD4Y2REDV5QML2', 'FGU2NZ3JIXC9N51I', 'RW09WWS3J0PXPMLJ',
            'OSGL3STEDHN3TZ7M', 'WKF2RX5IU1KSHCQN', 'AQD9B226KSTUFE0Z',
            'O9FV66INHEJGYUFB', 'SND0MRNKPX7TFFZY', 'EW4625MPD4TG50QI',
            'RXA8VR7MBAW63KOI'
        ]

        max_retries = 5
        retry_delay = 900  # 15 minutes

        for attempt in range(max_retries):
            for i, key in enumerate(keys):
                url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=30min&apikey={key}'
                response = requests.get(url)
                data = response.json()

                if "Meta Data" in data and "Time Series (30min)" in data:
                    print(f"[Key {i + 1}] Success for {symbol}.")
                    break
                else:
                    print(f"[Key {i + 1}] failed or rate-limited. Trying next key...")

            else:
                print(f"[Attempt {attempt + 1}] All keys failed. Waiting {retry_delay / 60} minutes...")
                if attempt == 3:
                    downloader = stockCSVDownloader()
                    downloader.move_to_downloads("stocks.csv")

                    printer = lastStockPrinter()
                    printer.move_last_stock_to_downloads(symbol, str(self.count))

                time.sleep(retry_delay)
                continue
            break
        else:
            print(f"Failed to fetch data for {symbol} after {max_retries} retries.")
            return

        print(f"Fetched data for: {data['Meta Data'].get('2. Symbol', 'UNKNOWN')}")
        time_series = data.get("Time Series (30min)", {})

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

        if os.path.exists(self.output_filename):
            os.remove(self.output_filename)
            self.header_written = False

        for symbol in tickers:
            print(f"Fetching data for {symbol}...")
            self.fetch_and_append_data(symbol)
