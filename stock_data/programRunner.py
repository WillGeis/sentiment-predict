from stockAPIGetter import stockAPIGetter
from topStockDisplayer import display_top_stocks_by_volume
from stockCSVDownloader import stockCSVDownloader
import subprocess
import os
import shutil

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
    downloader.move_to_downloads("stocks.csv")  # moves original stock list

if __name__ == "__main__":
    main()
