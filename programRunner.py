from stockAPIGetter import stockAPIGetter
from topStockDisplayer import display_top_stocks_by_volume
from stockCSVDownloader import stockCSVDownloader
import subprocess

class programRunner:
    def __init__(self):
        print("Program runner initialized")

    def run(self):
        getter = stockAPIGetter()
        getter.run()

def main():
    runner = programRunner()
    runner.run()
    display_top_stocks_by_volume()
    downloader = stockCSVDownloader()
    downloader.move_to_downloads("stocks.csv")
    userfinished = False
    optimize_stocks()

def optimize_stocks():
    while True:
        user_input1 = input("Would you like to optimize these stocks [y]es/[n]o?\n\n\nInput> ")
        
        if user_input1 == "n":
            print("Goodbye.")
            return
        elif user_input1 == "y":
            # Run the Julia script
            subprocess.run(["julia", "stock_optimizer.jl"])
            print("Optimization complete.")
            return
        else:
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")

if __name__ == "__main__":
    main()