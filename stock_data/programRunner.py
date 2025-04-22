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

    optimize_stocks()

def optimize_stocks():
    while True:
        user_input1 = input("Would you like to optimize these stocks [y]es/[n]o?\n\n\nInput> ")
        
        if user_input1.lower() == "n":
            print("Goodbye.")
            return
        elif user_input1.lower() == "y":
            # Define output file
            output_file = "top_stocks.csv"
            container_name = "julia_optimizer"

            print("Running optimizer in Docker...")

            # Build and run the container, mounting current dir for file I/O
            subprocess.run([
                "docker", "run", "--rm",
                "-v", f"{os.getcwd()}:/app",
                "--name", container_name,
                "your-julia-image-tag"  # <- replace with your actual image tag
            ])

            # Move result to Downloads
            if os.path.exists(output_file):
                downloader = stockCSVDownloader()
                downloader.move_to_downloads(output_file)
                print(f"{output_file} moved to Downloads.")
            else:
                print(f"Optimization file {output_file} not found.")
            
            return
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

if __name__ == "__main__":
    main()
