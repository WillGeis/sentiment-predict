import os
import shutil

class stockCSVDownloader:
    def __init__(self):
        self.downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        os.makedirs(self.downloads_folder, exist_ok=True)

    def move_to_downloads(self, csv_filename):
        """Moves the given CSV file to the user's Downloads folder."""
        if not os.path.isfile(csv_filename):
            print(f"File '{csv_filename}' not found.")
            return

        dest_path = os.path.join(self.downloads_folder, os.path.basename(csv_filename))

        try:
            shutil.copy(csv_filename, dest_path)
            print(f"Moved '{csv_filename}' to: {dest_path}")
        except Exception as e:
            print(f"Failed to move file: {e}")
