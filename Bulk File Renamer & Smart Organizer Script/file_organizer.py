"""
Bulk File Renamer & Smart Organizer
Task 8 - Python Developer Internship
Hasnain Karimain Educational Academy
"""

import os
import sys
import shutil
import csv
import json
from datetime import datetime

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    os.system("chcp 65001 > nul")


# ─────────────────────────── Globals ────────────────────────────
selected_folder = None
LOG_FILE = "operations_log.csv"

FILE_CATEGORIES = {
    "Images":     [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico"],
    "Videos":     [".mp4", ".avi", ".mov", ".mkv", ".wmv", ".flv", ".webm"],
    "Audio":      [".mp3", ".wav", ".aac", ".flac", ".ogg", ".wma"],
    "Documents":  [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".odt"],
    "Archives":   [".zip", ".rar", ".tar", ".gz", ".7z", ".bz2"],
    "Code":       [".py", ".js", ".ts", ".html", ".css", ".java", ".cpp", ".c", ".json", ".xml"],
    "Others":     [],
}


# ═══════════════════════════════════════════════════════════════
#  UTILITY
# ═══════════════════════════════════════════════════════════════

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def separator(char="=", width=60):
    print(char * width)

def header(title):
    separator()
    print(f"  {title}")
    separator()

def pause():
    input("\n  Press Enter to continue...")

def check_folder():
    if not selected_folder:
        print("\n  [WARN] No folder selected. Please select a folder first.")
        pause()
        return False
    if not os.path.isdir(selected_folder):
        print(f"\n  [ERR] Folder no longer exists: {selected_folder}")
        pause()
        return False
    return True

def get_files(folder):
    """Return list of files (not dirs) in folder."""
    try:
        return [f for f in os.listdir(folder)
                if os.path.isfile(os.path.join(folder, f))]
    except Exception as e:
        print(f"\n  [ERR] Cannot read folder: {e}")
        return []

def get_category(ext):
    ext = ext.lower()
    for cat, exts in FILE_CATEGORIES.items():
        if ext in exts:
            return cat
    return "Others"

def log_operation(old_name, new_name, operation):
    """Append a row to the CSV log file."""
    file_exists = os.path.isfile(LOG_FILE)
    try:
        with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Timestamp", "Operation", "Old Name", "New Name"])
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                operation,
                old_name,
                new_name
            ])
    except Exception as e:
        print(f"  [WARN] Could not write log: {e}")


# ═══════════════════════════════════════════════════════════════
#  1. SELECT FOLDER
# ═══════════════════════════════════════════════════════════════

def select_folder():
    global selected_folder
    header("SELECT FOLDER")

    path = input("  Enter folder path: ").strip().strip('"')

    if not path:
        print("  [ERR] No path entered.")
        pause()
        return

    if not os.path.isdir(path):
        print(f"  [ERR] Folder not found: {path}")
        pause()
        return

    selected_folder = path
    files = get_files(path)
    print(f"\n  [OK] Folder selected: {selected_folder}")
    print(f"       Files found    : {len(files)}")
    pause()


# ═══════════════════════════════════════════════════════════════
#  2. RENAME FILES
# ═══════════════════════════════════════════════════════════════

def rename_files():
    if not check_folder():
        return

    header("RENAME FILES")
    print("  Rename options:\n")
    print("  1. Add prefix  (e.g. HK_filename.txt)")
    print("  2. Add suffix  (e.g. filename_2026.txt)")
    print("  3. Replace word in filename")
    print("  4. Auto numbering  (file_1.txt, file_2.txt ...)")
    print("  0. Back")

    choice = input("\n  Choice: ").strip()

    if choice == "0":
        return

    files = get_files(selected_folder)
    if not files:
        print("  [WARN] No files in folder.")
        pause()
        return

    renames = []  # list of (old, new)

    if choice == "1":
        prefix = input("  Enter prefix: ").strip()
        for f in files:
            new_name = prefix + f
            renames.append((f, new_name))

    elif choice == "2":
        suffix = input("  Enter suffix (before extension): ").strip()
        for f in files:
            name, ext = os.path.splitext(f)
            new_name = name + suffix + ext
            renames.append((f, new_name))

    elif choice == "3":
        old_word = input("  Word to replace: ").strip()
        new_word = input("  Replace with   : ").strip()
        for f in files:
            if old_word in f:
                new_name = f.replace(old_word, new_word)
                renames.append((f, new_name))
            else:
                renames.append((f, f))

    elif choice == "4":
        base = input("  Base name (e.g. 'file'): ").strip()
        for i, f in enumerate(sorted(files), start=1):
            _, ext = os.path.splitext(f)
            new_name = f"{base}_{i}{ext}"
            renames.append((f, new_name))

    else:
        print("  [ERR] Invalid choice.")
        pause()
        return

    _preview_and_apply(renames, "Rename")


def _preview_and_apply(renames, operation):
    """Show preview, confirm, then apply."""
    changes = [(o, n) for o, n in renames if o != n]

    if not changes:
        print("\n  No changes to apply.")
        pause()
        return

    separator("-")
    print(f"  Preview ({len(changes)} changes):\n")
    for old, new in changes[:20]:
        print(f"    {old:<35} ->  {new}")
    if len(changes) > 20:
        print(f"    ... and {len(changes) - 20} more")
    separator("-")

    confirm = input("\n  Apply these changes? (y/n): ").strip().lower()
    if confirm != "y":
        print("  Cancelled.")
        pause()
        return

    applied = 0
    for old, new in changes:
        old_path = os.path.join(selected_folder, old)
        new_path = os.path.join(selected_folder, new)

        if os.path.exists(new_path) and old_path != new_path:
            print(f"  [SKIP] Already exists: {new}")
            continue

        try:
            os.rename(old_path, new_path)
            log_operation(old, new, operation)
            applied += 1
        except Exception as e:
            print(f"  [ERR] {old}: {e}")

    print(f"\n  [OK] Applied {applied} rename(s).")
    pause()


# ═══════════════════════════════════════════════════════════════
#  3. ORGANIZE FILES
# ═══════════════════════════════════════════════════════════════

def organize_files():
    if not check_folder():
        return

    header("ORGANIZE FILES")
    print("  Organize by:\n")
    print("  1. File type / extension category")
    print("  2. File extension (exact)")
    print("  3. Date modified (YYYY-MM)")
    print("  0. Back")

    choice = input("\n  Choice: ").strip()
    if choice == "0":
        return

    files = get_files(selected_folder)
    if not files:
        print("  [WARN] No files in folder.")
        pause()
        return

    moves = []  # list of (filename, subfolder)

    for f in files:
        _, ext = os.path.splitext(f)
        full_path = os.path.join(selected_folder, f)

        if choice == "1":
            subfolder = get_category(ext)

        elif choice == "2":
            subfolder = ext.lstrip(".").upper() if ext else "NO_EXT"

        elif choice == "3":
            try:
                mtime = os.path.getmtime(full_path)
                subfolder = datetime.fromtimestamp(mtime).strftime("%Y-%m")
            except Exception:
                subfolder = "Unknown"

        else:
            print("  [ERR] Invalid choice.")
            pause()
            return

        moves.append((f, subfolder))

    # Preview
    separator("-")
    print(f"  Preview ({len(moves)} files):\n")
    for fname, sub in moves[:20]:
        print(f"    {fname:<35} ->  {sub}/")
    if len(moves) > 20:
        print(f"    ... and {len(moves) - 20} more")
    separator("-")

    confirm = input("\n  Apply organization? (y/n): ").strip().lower()
    if confirm != "y":
        print("  Cancelled.")
        pause()
        return

    applied = 0
    for fname, sub in moves:
        src = os.path.join(selected_folder, fname)
        dest_dir = os.path.join(selected_folder, sub)
        dest = os.path.join(dest_dir, fname)

        try:
            os.makedirs(dest_dir, exist_ok=True)
            if os.path.exists(dest):
                print(f"  [SKIP] Already exists: {sub}/{fname}")
                continue
            shutil.move(src, dest)
            log_operation(fname, f"{sub}/{fname}", "Organize")
            applied += 1
        except Exception as e:
            print(f"  [ERR] {fname}: {e}")

    print(f"\n  [OK] Organized {applied} file(s).")
    pause()


# ═══════════════════════════════════════════════════════════════
#  4. PREVIEW CHANGES
# ═══════════════════════════════════════════════════════════════

def preview_changes():
    if not check_folder():
        return

    header("PREVIEW CHANGES")
    print("  Preview rename without applying:\n")
    print("  1. Prefix preview")
    print("  2. Suffix preview")
    print("  3. Auto-number preview")
    print("  0. Back")

    choice = input("\n  Choice: ").strip()
    if choice == "0":
        return

    files = sorted(get_files(selected_folder))
    if not files:
        print("  [WARN] No files in folder.")
        pause()
        return

    separator("-")
    print(f"  {'ORIGINAL':<35}  NEW NAME")
    separator("-")

    if choice == "1":
        prefix = input("  Enter prefix: ").strip()
        for f in files:
            print(f"  {f:<35}  {prefix + f}")

    elif choice == "2":
        suffix = input("  Enter suffix: ").strip()
        for f in files:
            name, ext = os.path.splitext(f)
            print(f"  {f:<35}  {name + suffix + ext}")

    elif choice == "3":
        base = input("  Base name: ").strip()
        for i, f in enumerate(files, start=1):
            _, ext = os.path.splitext(f)
            print(f"  {f:<35}  {base}_{i}{ext}")

    separator("-")
    print("  [INFO] Preview only - no changes made.")
    pause()


# ═══════════════════════════════════════════════════════════════
#  5. VIEW LOGS
# ═══════════════════════════════════════════════════════════════

def view_logs():
    header("OPERATION LOGS")

    if not os.path.isfile(LOG_FILE):
        print("  No log file found. No operations recorded yet.")
        pause()
        return

    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)

        if len(rows) <= 1:
            print("  Log is empty.")
            pause()
            return

        header_row = rows[0]
        separator("-")
        print(f"  {'#':<5} {'Timestamp':<22} {'Op':<10} {'Old Name':<30} New Name")
        separator("-")
        for i, row in enumerate(rows[1:], start=1):
            if len(row) >= 4:
                print(f"  {i:<5} {row[0]:<22} {row[1]:<10} {row[2]:<30} {row[3]}")
        separator("-")
        print(f"  Total records: {len(rows) - 1}")

    except Exception as e:
        print(f"  [ERR] Could not read log: {e}")

    pause()


# ═══════════════════════════════════════════════════════════════
#  MAIN MENU
# ═══════════════════════════════════════════════════════════════

def main():
    while True:
        clear()
        header("Bulk File Renamer & Smart Organizer  |  Task 8")
        status = f"[{selected_folder}]" if selected_folder else "[No folder selected]"
        print(f"  Folder: {status}\n")
        print("  1. Select Folder")
        print("  2. Rename Files")
        print("  3. Organize Files")
        print("  4. Preview Changes")
        print("  5. View Logs")
        print("  0. Exit")
        separator()

        choice = input("  Select option: ").strip()

        if choice == "1":
            select_folder()
        elif choice == "2":
            rename_files()
        elif choice == "3":
            organize_files()
        elif choice == "4":
            preview_changes()
        elif choice == "5":
            view_logs()
        elif choice == "0":
            print("\n  Goodbye!\n")
            sys.exit(0)
        else:
            print("  [ERR] Invalid option.")
            pause()


if __name__ == "__main__":
    main()
