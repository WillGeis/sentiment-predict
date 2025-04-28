import csv

"""
Collect tickers for the stocks already sampled
"""
def extract_tickers(input_filename, output_filename="sample_tickers.csv"):
    try:
        with open(input_filename, mode="r", newline="") as infile:
            reader = csv.DictReader(infile)
            tickers = [row['ticker'] for row in reader]

        with open(output_filename, mode="w", newline="") as outfile:
            writer = csv.writer(outfile)
            writer.writerow(["tickers"])  # header
            for ticker in tickers:
                writer.writerow([ticker])

        print(f"Successfully wrote {len(tickers)} tickers to '{output_filename}'.")
    except FileNotFoundError:
        print(f"Error: File '{input_filename}' not found.")
    except KeyError:
        print(f"Error: 'ticker' column not found in '{input_filename}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    input_file = input("Enter the input CSV filename: ").strip()
    extract_tickers(input_file)