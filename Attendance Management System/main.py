import sys
from datetime import datetime
import database
import attendance
import csv_sync

def print_menu():
    print("\n--- ATTENDANCE MANAGEMENT SYSTEM ---")
    print("1. Mark Daily Attendance")
    print("2. View Attendance Records")
    print("3. Update Attendance Record")
    print("4. Delete Attendance Record")
    print("5. Generate & Export Summary Report")
    print("6. Exit")

def handle_mark_attendance():
    print("\n--- MARK ATTENDANCE ---")
    person_id = input("Enter Student/Employee ID: ").strip()
    name = input("Enter Full Name: ").strip()
    date_str = input("Enter Date (YYYY-MM-DD) [Default Today]: ").strip()
    
    if not date_str:
        date_str = datetime.today().strftime("%Y-%m-%d")
        
    status = input("Enter Status (Present / Absent / Late): ").strip()
    attendance.mark_attendance(person_id, name, date_str, status)

def handle_view_records():
    print("\n--- VIEW ATTENDANCE RECORDS ---")
    print("1. View All Records")
    print("2. View by Specific Date")
    print("3. View by Person ID")
    sub_choice = input("Select filter option (1-3): ").strip()

    if sub_choice == "1":
        records = database.get_all_records()
    elif sub_choice == "2":
        date_str = input("Enter Date (YYYY-MM-DD): ").strip()
        records = database.get_records_by_date(date_str)
    elif sub_choice == "3":
        person_id = input("Enter Person ID: ").strip()
        records = database.get_records_by_person(person_id)
    else:
        print("Invalid selection.")
        return

    if not records:
        print("\nInformation: No matching attendance records found.")
        return

    print("\n" + "="*55)
    print(f"{'ID':<12} | {'Name':<20} | {'Date':<12} | {'Status':<8}")
    print("-" * 55)
    for r in records:
        print(f"{r['person_id']:<12} | {r['name']:<20} | {r['date']:<12} | {r['status']:<8}")
    print("="*55)

def handle_update_record():
    print("\n--- UPDATE ATTENDANCE RECORD ---")
    person_id = input("Enter Person ID: ").strip()
    date_str = input("Enter Date of Record (YYYY-MM-DD): ").strip()
    new_status = input("Enter New Status (Present / Absent / Late): ").strip()
    attendance.modify_attendance(person_id, date_str, new_status)

def handle_delete_record():
    print("\n--- DELETE ATTENDANCE RECORD ---")
    person_id = input("Enter Person ID: ").strip()
    date_str = input("Enter Date of Record (YYYY-MM-DD): ").strip()
    confirm = input(f"Confirm deletion for ID {person_id.upper()} on {date_str}? (y/n): ").strip().lower()
    if confirm == 'y':
        attendance.remove_attendance(person_id, date_str)

def handle_generate_report():
    summary = attendance.generate_attendance_summary()
    if not summary:
        print("\nInformation: No data available to generate a report.")
        return

    print("\n" + "="*75)
    print(" ATTENDANCE SUMMARY REPORT")
    print("="*75)
    print(f"{'ID':<10} | {'Name':<18} | {'Total':<6} | {'Present':<7} | {'Absent':<6} | {'Late':<5} | {'Att. %':<7}")
    print("-" * 75)
    for s in summary:
        print(f"{s['Person_ID']:<10} | {s['Name']:<18} | {s['Total_Days']:<6} | {s['Present']:<7} | {s['Absent']:<6} | {s['Late']:<5} | {s['Attendance_Percentage']:<7.1f}%")
    print("="*75)

    export_choice = input("\nExport report to 'attendance_summary_report.csv'? (y/n): ").strip().lower()
    if export_choice == 'y':
        csv_sync.export_summary_report(summary)

def run_app():
    database.init_db()
    csv_sync.sync_database_to_csv()

    while True:
        print_menu()
        choice = input("\nSelect option (1-6): ").strip()

        if choice == "1":
            handle_mark_attendance()
        elif choice == "2":
            handle_view_records()
        elif choice == "3":
            handle_update_record()
        elif choice == "4":
            handle_delete_record()
        elif choice == "5":
            handle_generate_report()
        elif choice == "6":
            print("\nExiting Attendance Management System.")
            sys.exit()
        else:
            print("\nInvalid choice. Select an option between 1 and 6.")

if __name__ == "__main__":
    run_app()