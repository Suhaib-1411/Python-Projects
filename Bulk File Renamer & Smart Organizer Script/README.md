# Task 8 - Bulk File Renamer & Smart Organizer

**Python Developer Internship Program**
Hasnain Karimain Educational Academy - Batch 7, Shift 2

---

## Overview

A professional CLI-based Python tool to rename multiple files in bulk and organize them
automatically into folders. Simulates real-world file management and automation systems.

---

## Features

| Feature | Details |
|---|---|
| Add Prefix | Prepend text to all filenames (e.g. HK_filename.txt) |
| Add Suffix | Append text before extension (e.g. filename_2026.txt) |
| Replace Word | Find and replace any word in filenames |
| Auto Numbering | Rename to base_1, base_2, base_3 ... |
| Organize by Type | Sort into Images, Videos, Audio, Documents, etc. |
| Organize by Extension | Sort into folders by exact extension |
| Organize by Date | Sort into YYYY-MM dated folders |
| Preview Mode | See changes before applying - no files touched |
| Logging | Every operation saved to operations_log.csv |
| Overwrite Protection | Skips files that would be overwritten |

---

## Project Structure

```
task8/
|
|-- file_organizer.py       # Main application (run this)
|-- sample_folder/          # Sample folder with 15 test files
|-- operations_log.csv      # Log of all rename/organize operations
|-- README.md               # This file
```

---

## Requirements

- Python 3.8+
- Standard library only (os, shutil, csv, datetime) - no pip install needed

---

## How to Run

Open Command Prompt (not VS Code terminal):

```
cd "path\to\task8"
python file_organizer.py
```

---

## Menu Options

```
============================================================
  Bulk File Renamer & Smart Organizer  |  Task 8
============================================================
  Folder: [No folder selected]

  1. Select Folder
  2. Rename Files
  3. Organize Files
  4. Preview Changes
  5. View Logs
  0. Exit
```

---

## Step-by-Step Example

1. Run the tool and select option **1**
2. Enter the path to `sample_folder`
3. Select **4** (Preview Changes) to see what a rename would look like
4. Select **2** (Rename Files) -> option **1** -> prefix: `HK_`
5. Confirm with `y` -> files are renamed
6. Select **3** (Organize Files) -> option **1** (by type)
7. Confirm with `y` -> files moved into subfolders
8. Select **5** (View Logs) -> see full operation history

---

## File Categories

| Folder | Extensions |
|---|---|
| Images | .jpg .jpeg .png .gif .bmp .svg .webp |
| Videos | .mp4 .avi .mov .mkv .wmv .flv |
| Audio | .mp3 .wav .aac .flac .ogg |
| Documents | .pdf .doc .docx .xls .xlsx .ppt .pptx .txt |
| Archives | .zip .rar .tar .gz .7z |
| Code | .py .js .html .css .java .cpp .json .xml |
| Others | Everything else |

---

## Log File Format

`operations_log.csv` is created automatically in the current directory:

```
Timestamp,Operation,Old Name,New Name
2026-06-22 10:01:00,Rename,photo_trip.jpg,HK_photo_trip.jpg
2026-06-22 10:05:00,Organize,HK_photo_trip.jpg,Images/HK_photo_trip.jpg
```

---

## Author

Muhammad Babar
Python Developer Intern - Batch 7
Hasnain Karimain Educational Academy
