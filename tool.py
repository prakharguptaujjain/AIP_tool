#!/usr/bin/env python3
"""
This is a script to retrieve the latest blocklists from the online sources and as well as latest created blocklists from the offline sources and save it to OUTPUT_DIR (Retrieved_blocklists)
"""
import requests
import os
import json
import time
import gzip


RETRIEVE_FILE = "blocklist_retrieve.json"
OUTPUT_DIR = "Retrieved_blocklists"
OUTPUT_FOLDERS = ["Alpha", "Alpha7", "Prioritize_Consistent", "Prioritize_New", "random_forest"]
RETENTION_PERIOD_DAYS = 30  # Number of days to keep the files

def get_blocklists():
    # Load the JSON file with the list of blocklists to retrieve
    with open(RETRIEVE_FILE) as f:
        retrieve = json.load(f)

    # Loop over online blocklists to retrieve
    for url in retrieve["blocklists_online"]:
        # Get the filename from the URL
        filename = url.split("/")[-1]

        # Determine the output folder based on the filename
        if "Alpha7" in filename:
            output_folder = os.path.join(OUTPUT_DIR, "Alpha7")
        elif "Prioritize_Consistent" in filename:
            output_folder = os.path.join(OUTPUT_DIR, "Prioritize_Consistent")
        elif "Prioritize_New" in filename:
            output_folder = os.path.join(OUTPUT_DIR, "Prioritize_New")
        elif "random_forest" in filename:
            output_folder = os.path.join(OUTPUT_DIR, "random_forest")
        elif "Alpha" in filename:
            output_folder = os.path.join(OUTPUT_DIR, "Alpha")
        else:
            print(f"Unknown blocklist type: {filename}")
        
        # Create the output folder if it does not exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Define the output file path
        output_file = os.path.join(output_folder, filename)

        # Check if the file already exists
        if not os.path.exists(output_file):
            # If the file does not exist, download it from the URL and save it to the output file path
            response = requests.get(url)
            with open(output_file, "w") as f:
                f.write(response.text)
            print(f"Retrieved {filename} from {url}")
        else:
            print(f"{filename} already exists in {output_folder}")

    # Loop over offline blocklists to copy
    for folder in retrieve["blocklists_offline_folders"]:
        # Get the list of files in the folder
        files = os.listdir(folder)
        # Filter out non-CSV files
        files = [f for f in files if f.endswith(".csv.gz")]
        # Sort the files by modification time (newest first)
        files = sorted(files, key=lambda f: os.path.getmtime(os.path.join(folder, f)), reverse=True)
        # Get the newest file
        newest_file = files[0]  

        # Check the file name substring and put it in the appropriate folder
        if "Alpha7" in newest_file:
            output_folder = os.path.join(OUTPUT_DIR, "Alpha7")
        elif "Prioritize_Consistent" in newest_file:
            output_folder = os.path.join(OUTPUT_DIR, "Prioritize_Consistent")
        elif "Prioritize_New" in newest_file:
            output_folder = os.path.join(OUTPUT_DIR, "Prioritize_New")
        elif "random_forest" in newest_file:
            output_folder = os.path.join(OUTPUT_DIR, "random_forest")
        elif "Alpha" in newest_file:
            output_folder = os.path.join(OUTPUT_DIR, "Alpha")   

        # Create the output folder if it does not exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)  

        # Define the output file path
        output_file = os.path.join(output_folder, newest_file[:-3]) # Remove the .gz extension in the output file path
        input_file = os.path.join(folder, newest_file)  

        # Check if the file already exists
        if not os.path.exists(output_file):
            with gzip.open(input_file, "rb") as fin, open(output_file, "wb") as fout:
                fout.write(fin.read())
                print(f"Copied {newest_file} from {folder} to {output_folder} and converted .csv.gz to .csv")
        else:
            print(f"{newest_file} already exists in {output_folder}")

    for folder in retrieve["blocklists_offline_folders"]:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Created folder {folder}")

def delete_old_files():
    """
    Delete files in the OUTPUT_DIR that are older than the RETENTION_PERIOD_DAYS.
    """
    now = time.time()
    for folder in os.listdir(OUTPUT_DIR):
        for filename in os.listdir(os.path.join(OUTPUT_DIR,folder)):
            file_path = os.path.join(OUTPUT_DIR,folder, filename)
            if os.path.isfile(file_path):
                age_days = (now - os.path.getmtime(file_path)) / (24 * 3600)
                if age_days > RETENTION_PERIOD_DAYS:
                    os.remove(file_path)
                    print(f"Deleted {filename} from {folder}")

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    get_blocklists()
    delete_old_files()
