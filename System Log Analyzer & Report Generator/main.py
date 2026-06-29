import os
import re

# Global variables to store data during runtime
loaded_lines = []
analysis_results = {}

def load_file():
    """Menu 1: Loads and reads the log file into memory with basic validation"""
    global loaded_lines, analysis_results
    filename = input("\nEnter the log file name (e.g., Sample_log.txt): ").strip()
    
    if not os.path.exists(filename):
        print("Error: File not found! Please check the name and try again.")
        return
        
    if os.path.getsize(filename) == 0:
        print("Warning: The file is completely empty.")
        return

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            # Using readlines() for efficient internal line-by-line management
            loaded_lines = file.readlines()
        print(f"Success! Loaded {len(loaded_lines)} lines from '{filename}'.")
        # Clear previous analysis data when a new file loads
        analysis_results.clear()
    except Exception as e:
        print(f" An error occurred while reading the file: {e}")

def analyze_logs():
    """Menu 2: Uses Regex to count log levels (INFO, WARNING, ERROR)"""
    global loaded_lines, analysis_results
    if not loaded_lines:
        print(" No log file loaded yet. Please choose Option 1 first.")
        return

    counts = {"INFO": 0, "WARNING": 0, "ERROR": 0}
    
    # Compile regex patterns for faster processing across large sets
    info_pattern = re.compile(r'\bINFO\b', re.IGNORECASE)
    warn_pattern = re.compile(r'\bWARNING\b', re.IGNORECASE)
    err_pattern = re.compile(r'\bERROR\b', re.IGNORECASE)

    for line in loaded_lines:
        if info_pattern.search(line):
            counts["INFO"] += 1
        elif warn_pattern.search(line):
            counts["WARNING"] += 1
        elif err_pattern.search(line):
            counts["ERROR"] += 1

    analysis_results = {
        "total_logs": len(loaded_lines),
        "info": counts["INFO"],
        "warning": counts["WARNING"],
        "error": counts["ERROR"]
    }

    print("\n --- ANALYSIS RESULTS ---")
    print(f"Total Log Entries: {analysis_results['total_logs']}")
    print(f"ℹ INFO Messages:   {analysis_results['info']}")
    print(f" WARNINGS:        {analysis_results['warning']}")
    print(f" ERRORS:          {analysis_results['error']}")

def search_logs():
    """Menu 3: Case-insensitive keyword search and log filtering"""
    global loaded_lines
    if not loaded_lines:
        print(" No log file loaded yet. Please choose Option 1 first.")
        return

    keyword = input("\nEnter keyword or log level to search for: ").strip()
    if not keyword:
        print(" Search term cannot be empty.")
        return

    print(f"\n Matching results for '{keyword}':")
    print("-" * 50)
    
    match_count = 0
    # Case-insensitive flag used for regex matching
    search_pattern = re.compile(re.escape(keyword), re.IGNORECASE)

    for line in loaded_lines:
        if search_pattern.search(line):
            print(line.strip())
            match_count += 1

    print("-" * 50)
    print(f"Found {match_count} matching line(s).")

def generate_report():
    """Menu 4: Writes the analysis data safely to a summary report text file"""
    global analysis_results
    if not analysis_results:
        print(" Logs haven't been analyzed yet. Please choose Option 2 first.")
        return

    report_filename = "report.txt"
    try:
        with open(report_filename, 'w', encoding='utf-8') as report:
            report.write("=========================================\n")
            report.write("        SYSTEM LOG ANALYSIS REPORT       \n")
            report.write("=========================================\n")
            report.write(f"Total Logs Processed : {analysis_results['total_logs']}\n")
            report.write(f"Total Info Messages  : {analysis_results['info']}\n")
            report.write(f"Total Warnings Found : {analysis_results['warning']}\n")
            report.write(f"Total Errors Found   : {analysis_results['error']}\n")
            report.write("=========================================\n")
            report.write("Report generated successfully.\n")
            
        print(f" Report successfully compiled and saved to '{report_filename}'!")
    except Exception as e:
        print(f" Failed to write report file: {e}")

def main():
    """The central CLI loop controlling the menu UI"""
    while True:
        print("\n=========================================")
        print("       SYSTEM LOG ANALYZER MENU         ")
        print("=========================================")
        print("1. Load Log File")
        print("2. Analyze Logs")
        print("3. Search Logs")
        print("4. Generate Report")
        print("5. Exit")
        print("=========================================")
        
        choice = input("Select an option (1-5): ").strip()

        if choice == '1':
            load_file()
        elif choice == '2':
            analyze_logs()
        elif choice == '3':
            search_logs()
        elif choice == '4':
            generate_report()
        elif choice == '5':
            print("\n👋 Exiting Program. Have a great day!")
            break
        else:
            print(" Invalid entry! Please type a number from 1 to 5.")

if __name__ == "__main__":
    main()