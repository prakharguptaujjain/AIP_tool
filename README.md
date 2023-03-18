# Tool for AIP Coding Challenge for GSoC

## About
This tool is created for the AIP Coding Challenge for GSoC. Its purpose is to retrieve the latest blocklists from the online sources and as well as latest created blocklists from the offline sources and save them to OUTPUT_DIR (Retrieved_blocklists).

## Files
The following files are included in this tool:

### blocklist_retrieve.json
This file contains a list of blocklists to retrieve. It includes online blocklists as well as offline blocklists.

### tool.py
This is the main script file that retrieves the blocklists and saves them to the OUTPUT_DIR. It includes the following functions:

* get_blocklists(): retrieves the blocklists and saves them to the OUTPUT_DIR
* delete_old_files(): deletes files in the OUTPUT_DIR that are older than the RETENTION_PERIOD_DAYS
The OUTPUT_DIR is set to "Retrieved_blocklists" and the RETENTION_PERIOD_DAYS is set to 30 days.

The script retrieves the blocklists by following the instructions in the blocklist_retrieve.json file. It loops over the online blocklists to retrieve and offline blocklists to copy. It creates the appropriate output folder for each blocklist and checks if the file already exists. If the file does not exist, it downloads it from the URL and saves it to the output file path. If the file already exists, it skips the download. The script also converts .csv.gz files to .csv files. After retrieving the blocklists, it deletes files in the OUTPUT_DIR that are older than the RETENTION_PERIOD_DAYS.

## Usage
To use this tool, clone this repository and run the tool.py file. The blocklists will be retrieved and saved to the OUTPUT_DIR. You can change the RETENTION_PERIOD_DAYS and the OUTPUT_DIR if desired.
