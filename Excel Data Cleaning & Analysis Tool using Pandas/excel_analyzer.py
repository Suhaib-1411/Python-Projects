"""
Excel Data Cleaning & Analysis Tool
Task 7 - Python Developer Internship
Hasnain Karimain Educational Academy
"""

import pandas as pd
import os
import sys
from datetime import datetime

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    os.system("chcp 65001 > nul")


#  Globals 
df = None
current_file = None


# 
#  UTILITY
# 

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def separator(char="-", width=60):
    print(char * width)

def header(title):
    separator("=")
    print(f"  {title}")
    separator("=")

def pause():
    input("\n  Press Enter to continue...")

def check_data_loaded():
    if df is None:
        print("\n  [WARN]  No file loaded. Please load a file first.")
        pause()
        return False
    return True


# 
#  1. LOAD FILE
# 

def load_file():
    global df, current_file
    header("[LOAD]  Load Excel / CSV File")

    path = input("  Enter file path (.xlsx / .csv): ").strip()

    if not os.path.exists(path):
        print(f"\n  [ERR] File not found: {path}")
        pause()
        return

    try:
        ext = os.path.splitext(path)[1].lower()
        if ext == ".xlsx" or ext == ".xls":
            df = pd.read_excel(path)
        elif ext == ".csv":
            df = pd.read_csv(path)
        else:
            print("  [ERR] Unsupported format. Use .xlsx or .csv")
            pause()
            return

        current_file = path
        print(f"\n  [OK] Loaded successfully!")
        print(f"     Rows    : {df.shape[0]}")
        print(f"     Columns : {df.shape[1]}")
        print(f"     Columns : {list(df.columns)}")
        pause()

    except Exception as e:
        print(f"\n  [ERR] Error loading file: {e}")
        pause()


# 
#  2. CLEAN DATA
# 

def clean_data():
    global df
    if not check_data_loaded():
        return

    header("[CLEAN]  Clean Data")
    print("  Choose cleaning option:\n")
    print("  1. Remove duplicate rows")
    print("  2. Handle missing values  fill with mean/median/mode")
    print("  3. Handle missing values  drop rows with nulls")
    print("  4. Drop columns that are entirely empty")
    print("  5. Standardize column names (lowercase + underscores)")
    print("  6. Run all cleaning steps")
    print("  0. Back")

    choice = input("\n  Choice: ").strip()

    if choice == "1":
        _remove_duplicates()
    elif choice == "2":
        _fill_missing()
    elif choice == "3":
        _drop_null_rows()
    elif choice == "4":
        _drop_empty_columns()
    elif choice == "5":
        _standardize_columns()
    elif choice == "6":
        _remove_duplicates(silent=True)
        _drop_empty_columns(silent=True)
        _fill_missing(silent=True)
        _standardize_columns(silent=True)
        print("\n  [OK] All cleaning steps applied.")
        pause()
    elif choice == "0":
        return
    else:
        print("  Invalid choice.")
        pause()


def _remove_duplicates(silent=False):
    global df
    before = len(df)
    df = df.drop_duplicates()
    removed = before - len(df)
    if not silent:
        print(f"\n  [OK] Removed {removed} duplicate row(s). Remaining: {len(df)}")
        pause()
    else:
        print(f"     Duplicates removed  : {removed}")


def _fill_missing(silent=False):
    global df
    if not silent:
        print("\n  Fill strategy: 1-Mean  2-Median  3-Mode  4-Custom value")
        strategy = input("  Choice: ").strip()
    else:
        strategy = "1"  # default for bulk run

    filled = 0
    for col in df.columns:
        if df[col].isnull().any():
            if df[col].dtype in ["float64", "int64"]:
                if strategy == "1":
                    val = df[col].mean()
                elif strategy == "2":
                    val = df[col].median()
                elif strategy == "3":
                    val = df[col].mode()[0] if not df[col].mode().empty else 0
                elif strategy == "4":
                    val = input(f"  Value for '{col}': ").strip()
                else:
                    val = df[col].mean()
                df[col] = df[col].fillna(val)
            else:
                mode_val = df[col].mode()[0] if not df[col].mode().empty else "Unknown"
                df[col] = df[col].fillna(mode_val)
            filled += 1

    if not silent:
        print(f"\n  [OK] Filled missing values in {filled} column(s).")
        pause()
    else:
        print(f"     Columns filled      : {filled}")


def _drop_null_rows(silent=False):
    global df
    before = len(df)
    df = df.dropna()
    removed = before - len(df)
    if not silent:
        print(f"\n  [OK] Dropped {removed} row(s) with nulls. Remaining: {len(df)}")
        pause()
    else:
        print(f"     Null rows dropped   : {removed}")


def _drop_empty_columns(silent=False):
    global df
    before = len(df.columns)
    df = df.dropna(axis=1, how="all")
    removed = before - len(df.columns)
    if not silent:
        print(f"\n  [OK] Dropped {removed} empty column(s).")
        pause()
    else:
        print(f"     Empty cols removed  : {removed}")


def _standardize_columns(silent=False):
    global df
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    if not silent:
        print(f"\n  [OK] Columns standardized: {list(df.columns)}")
        pause()
    else:
        print(f"     Columns standardized: {list(df.columns)}")


# 
#  3. ANALYZE DATA
# 

def analyze_data():
    if not check_data_loaded():
        return

    header("[ANALYZE]  Analyze Data")
    print(f"  File    : {current_file}")
    print(f"  Shape   : {df.shape[0]} rows  {df.shape[1]} columns")
    separator()

    print("\n  [INFO] Column-wise Summary:\n")
    for col in df.columns:
        dtype = str(df[col].dtype)
        nulls = df[col].isnull().sum()
        unique = df[col].nunique()
        print(f"  {col:<25} dtype={dtype:<10}  nulls={nulls:<5}  unique={unique}")

    separator()

    numeric_cols = df.select_dtypes(include=["number"]).columns
    if len(numeric_cols):
        print("\n  [STATS] Numeric Statistics:\n")
        stats = df[numeric_cols].agg(["mean", "median", "min", "max", "std"]).round(2)
        print(stats.to_string())

    separator()

    print("\n  [GROUP] Group Analysis (by categorical column)")
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    if cat_cols:
        print(f"  Categorical columns: {cat_cols}")
        col = input("  Group by column (or Enter to skip): ").strip()
        if col in df.columns and len(numeric_cols):
            num_col = input(f"  Aggregate column (numeric) [{list(numeric_cols)[0]}]: ").strip()
            if num_col not in numeric_cols:
                num_col = list(numeric_cols)[0]
            grouped = df.groupby(col)[num_col].agg(["mean", "sum", "count"]).round(2)
            print(f"\n  Grouped by '{col}'  '{num_col}':\n")
            print(grouped.to_string())
    else:
        print("  No categorical columns found.")

    pause()


# 
#  4. FILTER / SEARCH
# 

def filter_search():
    if not check_data_loaded():
        return

    header("[FILTER]  Filter / Search Data")
    print("  1. Search by keyword (any column)")
    print("  2. Filter by column value")
    print("  3. Filter numeric column by range")
    print("  0. Back")

    choice = input("\n  Choice: ").strip()

    if choice == "1":
        keyword = input("  Keyword: ").strip().lower()
        mask = df.apply(lambda col: col.astype(str).str.lower().str.contains(keyword, na=False))
        result = df[mask.any(axis=1)]
        _show_result(result, f"Keyword '{keyword}'")

    elif choice == "2":
        print(f"  Columns: {list(df.columns)}")
        col = input("  Column name: ").strip()
        if col not in df.columns:
            print("  [ERR] Column not found.")
            pause()
            return
        val = input("  Value to filter: ").strip().lower()
        result = df[df[col].astype(str).str.lower() == val]
        _show_result(result, f"{col} = {val}")

    elif choice == "3":
        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        print(f"  Numeric columns: {numeric_cols}")
        col = input("  Column name: ").strip()
        if col not in numeric_cols:
            print("  [ERR] Not a numeric column.")
            pause()
            return
        try:
            lo = float(input("  Min value: "))
            hi = float(input("  Max value: "))
            result = df[(df[col] >= lo) & (df[col] <= hi)]
            _show_result(result, f"{lo}  {col}  {hi}")
        except ValueError:
            print("  [ERR] Invalid numbers.")
            pause()

    elif choice == "0":
        return


def _show_result(result, label):
    separator()
    print(f"  Results for: {label}    {len(result)} row(s) found\n")
    if result.empty:
        print("  No matching records.")
    else:
        print(result.to_string(index=False))
    pause()


# 
#  5. SAVE OUTPUT
# 

def save_output():
    if not check_data_loaded():
        return

    header("[SAVE]  Save Output")
    print("  1. Save cleaned data as Excel (.xlsx)")
    print("  2. Save cleaned data as CSV (.csv)")
    print("  3. Generate analysis report (.txt)")
    print("  0. Back")

    choice = input("\n  Choice: ").strip()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if choice == "1":
        fname = f"cleaned_data_{timestamp}.xlsx"
        try:
            df.to_excel(fname, index=False)
            print(f"\n  [OK] Saved: {fname}")
        except Exception as e:
            print(f"\n  [ERR] Error: {e}")
        pause()

    elif choice == "2":
        fname = f"cleaned_data_{timestamp}.csv"
        try:
            df.to_csv(fname, index=False)
            print(f"\n  [OK] Saved: {fname}")
        except Exception as e:
            print(f"\n  [ERR] Error: {e}")
        pause()

    elif choice == "3":
        fname = f"analysis_report_{timestamp}.txt"
        _generate_report(fname)

    elif choice == "0":
        return


def _generate_report(fname):
    try:
        numeric_cols = df.select_dtypes(include=["number"]).columns
        lines = []
        lines.append("=" * 60)
        lines.append("  EXCEL DATA ANALYSIS REPORT")
        lines.append(f"  Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"  Source    : {current_file}")
        lines.append("=" * 60)
        lines.append(f"\n  Total Records : {len(df)}")
        lines.append(f"  Total Columns : {len(df.columns)}")
        lines.append(f"  Missing Values: {df.isnull().sum().sum()}")
        lines.append(f"  Duplicate Rows: {df.duplicated().sum()}")

        lines.append("\n" + "-" * 60)
        lines.append("  COLUMN DETAILS")
        lines.append("-" * 60)
        for col in df.columns:
            lines.append(f"  {col}")
            lines.append(f"    dtype  : {df[col].dtype}")
            lines.append(f"    nulls  : {df[col].isnull().sum()}")
            lines.append(f"    unique : {df[col].nunique()}")

        if len(numeric_cols):
            lines.append("\n" + "-" * 60)
            lines.append("  NUMERIC STATISTICS")
            lines.append("-" * 60)
            stats = df[numeric_cols].agg(["mean", "median", "min", "max", "std"]).round(2)
            lines.append(stats.to_string())

        lines.append("\n" + "=" * 60)
        lines.append("  END OF REPORT")
        lines.append("=" * 60)

        with open(fname, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print(f"\n  [OK] Report saved: {fname}")
        pause()

    except Exception as e:
        print(f"\n  [ERR] Error generating report: {e}")
        pause()


# 
#  MAIN MENU
# 

def main():
    while True:
        clear()
        header("  Excel Data Cleaning & Analysis Tool  |  Task 7")
        status = f"[{os.path.basename(current_file)}  {df.shape[0]}{df.shape[1]}]" if df is not None else "[No file loaded]"
        print(f"  Status: {status}\n")
        print("  1. [LOAD]  Load File")
        print("  2. [CLEAN]  Clean Data")
        print("  3. [ANALYZE]  Analyze Data")
        print("  4. [FILTER]  Filter / Search")
        print("  5. [SAVE]  Save Output")
        print("  0. [EXIT]  Exit")
        separator()

        choice = input("  Select option: ").strip()

        if choice == "1":
            load_file()
        elif choice == "2":
            clean_data()
        elif choice == "3":
            analyze_data()
        elif choice == "4":
            filter_search()
        elif choice == "5":
            save_output()
        elif choice == "0":
            print("\n  Goodbye! \n")
            sys.exit(0)
        else:
            print("  [ERR] Invalid option.")
            pause()


if __name__ == "__main__":
    main()
