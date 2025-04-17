from stockAPIGetter import stockAPIGetter
from topStockDisplayer import display_top_stocks_by_volume
from stockCSVDownloader import stockCSVDownloader

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
    user_input = input("Are you done looking at the trades [y]es/[n]o?\n\n\nInput> ")
    

if __name__ == "__main__":
    main()