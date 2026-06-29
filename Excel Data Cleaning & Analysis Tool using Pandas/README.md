# Task 7 - Excel Data Cleaning & Analysis Tool

**Python Developer Internship Program**  
Hasnain Karimain Educational Academy - Batch 7, Shift 2

---

## Overview

A professional CLI-based Python tool to **load, clean, analyze, filter, and export** Excel/CSV data using **Pandas**. Simulates real-world data analysis workflows used in companies.

---

## Features

| Feature | Details |
|---|---|
| Load File | `.xlsx` and `.csv` support |
| Remove Duplicates | Detects and drops duplicate rows |
| Handle Missing Values | Fill (mean/median/mode/custom) or drop |
| Drop Empty Columns | Removes columns with all nulls |
| Standardize Columns | Lowercase + underscore column names |
| Run All Cleaning | One-step full cleaning pipeline |
| Numeric Statistics | Mean, median, min, max, std per column |
| Group Analysis | Group by any categorical column |
| Keyword Search | Case-insensitive search across all columns |
| Column Filter | Filter rows by exact column value |
| Range Filter | Filter numeric columns by min-max range |
| Save as Excel | Export cleaned data as `.xlsx` |
| Save as CSV | Export cleaned data as `.csv` |
| Analysis Report | Generate `.txt` summary report |

---

## Project Structure

```
task7/
|
|-- excel_analyzer.py          # Main application (run this)
|-- generate_sample_data.py    # Script to create sample_data.xlsx
|-- sample_data.xlsx           # Sample dirty Excel file (50+ rows)
|-- cleaned_data_<ts>.xlsx     # Output: cleaned data
|-- analysis_report_<ts>.txt   # Output: analysis report
|-- README.md                  # This file
```

---

## Requirements

- Python 3.8+
- pandas
- openpyxl

### Install dependencies

```bash
pip install pandas openpyxl
```

---

## How to Run

```bash
python excel_analyzer.py
```

The interactive menu will appear:

```
============================================================
  Excel Data Cleaning & Analysis Tool  |  Task 7
============================================================
  Status: [No file loaded]

  1. [LOAD]    Load File
  2. [CLEAN]   Clean Data
  3. [ANALYZE] Analyze Data
  4. [FILTER]  Filter / Search
  5. [SAVE]    Save Output
  0. [EXIT]    Exit
```

---

## Quick Test with Sample Data

1. Generate the sample Excel file:
   ```bash
   python generate_sample_data.py
   ```

2. Run the tool:
   ```bash
   python excel_analyzer.py
   ```

3. Select **1** -> type `sample_data.xlsx` -> press Enter

4. Select **2** -> choose **6** (Run all cleaning steps)

5. Select **3** to view analysis

6. Select **5** -> choose **3** to generate report

---

## Sample Data Info

The `sample_data.xlsx` file contains **53 rows x 10 columns** with:
- Intentional **missing values** in Age, Salary, Performance columns
- **3 duplicate rows** included
- Columns: `Employee_ID`, `Name`, `Department`, `City`, `Gender`, `Age`, `Salary`, `Performance`, `Experience_Yrs`, `Email`

---

## Cleaning Pipeline (Option 6)

| Step | What It Does |
|---|---|
| Remove Duplicates | Drops 3 duplicate rows |
| Drop Empty Columns | Removes fully null columns |
| Fill Missing Values | Fills numeric nulls with column mean, text with mode |
| Standardize Columns | Converts all column names to snake_case |

---

## Output Files

| File | Description |
|---|---|
| `cleaned_data_<timestamp>.xlsx` | Cleaned version of the dataset |
| `analysis_report_<timestamp>.txt` | Full statistical summary report |

---
