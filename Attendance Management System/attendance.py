from datetime import datetime
import database
import csv_sync

VALID_STATUSES = ["Present", "Absent", "Late"]

def validate_date(date_str: str) -> bool:
    """Validates if a string adheres to YYYY-MM-DD format."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def mark_attendance(person_id: str, name: str, date_str: str, status: str) -> bool:
    """Validates inputs and records daily attendance."""
    if not person_id.strip() or not name.strip():
        print("\nError: ID and Name fields cannot be blank.")
        return False

    if not validate_date(date_str):
        print("\nError: Invalid date format. Use YYYY-MM-DD.")
        return False

    status_fmt = status.strip().title()
    if status_fmt not in VALID_STATUSES:
        print(f"\nError: Invalid status '{status}'. Must be Present, Absent, or Late.")
        return False

    success = database.insert_attendance(person_id, name, date_str, status_fmt)
    if success:
        csv_sync.sync_database_to_csv()
        print(f"\nSuccess: Marked '{status_fmt}' for ID {person_id.upper()} on {date_str}.")
        return True
    return False

def modify_attendance(person_id: str, date_str: str, new_status: str) -> bool:
    """Modifies an existing attendance status."""
    if not validate_date(date_str):
        print("\nError: Invalid date format. Use YYYY-MM-DD.")
        return False

    status_fmt = new_status.strip().title()
    if status_fmt not in VALID_STATUSES:
        print(f"\nError: Invalid status '{new_status}'. Must be Present, Absent, or Late.")
        return False

    success = database.update_attendance_status(person_id, date_str, status_fmt)
    if success:
        csv_sync.sync_database_to_csv()
        print(f"\nSuccess: Updated status to '{status_fmt}' for ID {person_id.upper()} on {date_str}.")
        return True
    else:
        print(f"\nError: No record found for ID '{person_id}' on date '{date_str}'.")
        return False

def remove_attendance(person_id: str, date_str: str) -> bool:
    """Deletes an attendance record."""
    if not validate_date(date_str):
        print("\nError: Invalid date format. Use YYYY-MM-DD.")
        return False

    success = database.delete_attendance_record(person_id, date_str)
    if success:
        csv_sync.sync_database_to_csv()
        print(f"\nSuccess: Deleted record for ID {person_id.upper()} on {date_str}.")
        return True
    else:
        print(f"\nError: No record found for ID '{person_id}' on date '{date_str}'.")
        return False

def generate_attendance_summary() -> list:
    """Calculates attendance summary metrics including totals and percentages."""
    records = database.get_all_records()
    summary_dict = {}

    for r in records:
        pid = r["person_id"]
        name = r["name"]
        status = r["status"]

        if pid not in summary_dict:
            summary_dict[pid] = {
                "Person_ID": pid,
                "Name": name,
                "Total_Days": 0,
                "Present": 0,
                "Absent": 0,
                "Late": 0,
                "Attendance_Percentage": 0.0
            }

        summary_dict[pid]["Total_Days"] += 1
        if status == "Present":
            summary_dict[pid]["Present"] += 1
        elif status == "Absent":
            summary_dict[pid]["Absent"] += 1
        elif status == "Late":
            summary_dict[pid]["Late"] += 1

    summary_list = []
    for pid, stats in summary_dict.items():
        total = stats["Total_Days"]
        # Present and Late count toward attendance calculation
        attended = stats["Present"] + stats["Late"]
        pct = round((attended / total) * 100, 2) if total > 0 else 0.0
        stats["Attendance_Percentage"] = pct
        summary_list.append(stats)

    return summary_list