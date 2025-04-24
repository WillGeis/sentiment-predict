import os

class lastStockPrinter:
    def __init__(self):
        self.downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        os.makedirs(self.downloads_folder, exist_ok=True)
    
    def move_last_stock_to_downloads(self, last_stock, number):
        filename = os.path.join(self.downloads_folder, f"last_stock_{number}.txt")
        with open(filename, 'w') as file:
            file.write(last_stock)
        print(f"Content written to {filename}")
