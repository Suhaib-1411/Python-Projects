import csv
from typing import List, Dict, Any
import database

CSV_FILE = "attendance_records.csv"

def sync_database_to_csv(filename: str = CSV_FILE) -> bool:
    """
    Exports all current SQLite attendance records to a CSV file to maintain dual-system synchronization.
    """
    try:
        records = database.get_all_records()
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Person_ID", "Name", "Date", "Status"])
            for row in records:
                writer.writerow([row["person_id"], row["name"], row["date"], row["status"]])
        return True
    except IOError as e:
        print(f"\nError: Unable to synchronize CSV file - {e}")
        return False

def export_summary_report(report_rows: List[Dict[str, Any]], filename: str = "attendance_summary_report.csv") -> bool:
    """Exports calculated attendance summary metrics to a designated CSV report file."""
    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            fieldnames = ["Person_ID", "Name", "Total_Days", "Present", "Absent", "Late", "Attendance_Percentage"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in report_rows:
                writer.writerow(row)
        print(f"\nSuccess: Attendance report exported to '{filename}'.")
        return True
    except IOError as e:
        print(f"\nError exporting report: {e}")
        return False