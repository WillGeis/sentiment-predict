import csv

def display_top_stocks_by_volume(csv_filename="stock_data.csv", top_n=10):
    try:
        with open(csv_filename, mode="r") as csvfile:
            reader = csv.DictReader(csvfile)
            data = list(reader)

            # Convert volume to integer for sorting
            for row in data:
                row["volume"] = int(float(row["volume"]))  # handles string to int, in case of decimal

            # Sort by volume in descending order
            sorted_data = sorted(data, key=lambda x: x["volume"], reverse=True)

            print(f"\nTop {top_n} Stocks by Volume:\n")
            print(f"{'Ticker':<10} {'Timestamp':<22} {'Open':>8} {'High':>8} {'Low':>8} {'Close':>8} {'Volume':>10}")
            print("-" * 70)
            for row in sorted_data[:top_n]:
                print(f"{row['ticker']:<10} {row['timestamp']:<22} {row['open']:>8} {row['high']:>8} {row['low']:>8} {row['close']:>8} {row['volume']:>10}")

    except FileNotFoundError:
        print(f"Error: File '{csv_filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")   
