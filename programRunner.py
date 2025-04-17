from stockAPIGetter import stockAPIGetter
from topStockDisplayer import display_top_stocks_by_volume

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

if __name__ == "__main__":
    main()