import os
import json
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Global data list
records = []

def add_data():
    """Menu 1: Manually append data entries through the console interface"""
    global records
    print("\n --- Enter Record Details ---")
    uid = input("Enter ID (Student/Employee ID): ").strip()
    name = input("Enter Full Name: ").strip()
    email = input("Enter Email Address: ").strip()
    dept = input("Enter Course/Department/Role: ").strip()
    perf = input("Enter Performance Status (e.g. Excellent/Good): ").strip()

    if not uid or not name or not email:
        print(" Error: ID, Name, and Email fields cannot be left empty.")
        return

    records.append({
        "id": uid,
        "name": name,
        "email": email,
        "department": dept,
        "performance": perf
    })
    print(f" Record for '{name}' appended successfully in memory buffer.")

def load_data():
    """Menu 2: Import multiple data objects safely from a local JSON dataset"""
    global records
    filename = input("\nEnter JSON data file name (e.g., data.json): ").strip()

    if not os.path.exists(filename):
        print(" Error: Target dataset file not found!")
        return

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            records = json.load(file)
        print(f" Success! Imported {len(records)} entries from '{filename}'.")
    except Exception as e:
        print(f" System failure loading file data records: {e}")

def generate_pdf():
    """Menu 3: Compiles stored data profiles cleanly into a structured PDF document"""
    global records
    if not records:
        print(" Data engine empty. Please add rows manually (Option 1) or load a file (Option 2) first.")
        return

    report_title = input("\nEnter Report Name Title (e.g., Student Performance Summary): ").strip()
    if not report_title:
        report_title = "Data Management Summary Report"

    pdf_filename = "generated_report.pdf"
    
    try:
        # Document Setup
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
        story = []
        
        # Styles Layout
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontSize=24,
            leading=28,
            textColor=colors.HexColor("#1A365D"), # Deep Corporate Navy Blue
            spaceAfter=12
        )
        meta_style = ParagraphStyle(
            'MetaText',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.gray,
            spaceAfter=20
        )
        
        # Adding Structural Elements to PDF
        story.append(Paragraph(report_title, title_style))
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        story.append(Paragraph(f"Generated On: {timestamp} | Total Item Metrics: {len(records)} Record Profiles", meta_style))
        story.append(Spacer(1, 10))

        # Build Table Matrix
        # Header Row
        table_data = [["ID", "Name", "Email Address", "Department/Role", "Performance"]]
        
        # Fill Rows dynamically from local record registry
        for row in records:
            table_data.append([row["id"], row["name"], row["email"], row["department"], row["performance"]])
        
        # Draw and Style the PDF Grid Layout
        pdf_table = Table(table_data, colWidths=[50, 100, 150, 120, 110])
        pdf_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1A365D")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F7FAFC")),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#E2E8F0")),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(pdf_table)
        
        # Build document pages
        doc.build(story)
        print(f" File successfully generated and locked to disk: '{pdf_filename}'!")

    except Exception as e:
        print(f" Failed to build or write target PDF output file layout structural grid: {e}")

def main():
    """App console structural routing framework loop"""
    while True:
        print("\n=========================================")
        print("     INSTITUTIONAL PDF REPORT GENERATOR  ")
        print("=========================================")
        print("1. Add Data Manually")
        print("2. Load Data from JSON File")
        print("3. Generate PDF Report")
        print("4. Exit")
        print("=========================================")
        
        choice = input("Select an option (1-4): ").strip()

        if choice == '1':
            add_data()
        elif choice == '2':
            load_data()
        elif choice == '3':
            generate_pdf()
        elif choice == '4':
            print("\n Closing generator engine sequence. Goodbye!")
            break
        else:
            print(" Selection key match fault. Choose digits 1-4.")

if __name__ == "__main__":
    main()