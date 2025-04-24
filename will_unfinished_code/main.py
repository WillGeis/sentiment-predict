from programRunner import programRunner
from topStockDisplayer import display_top_stocks_by_volume
from stockCSVDownloader import stockCSVDownloader

def main():
    while True:
        try:
            count = int(input("How many times have you run the API? "))
            runner = programRunner(count)
            runner.run()
            display_top_stocks_by_volume()

            downloader = stockCSVDownloader()
            downloader.move_to_downloads("stocks.csv")
        except ValueError:
            print("Please enter a valid integer.")

if __name__ == "__main__":
    main()
