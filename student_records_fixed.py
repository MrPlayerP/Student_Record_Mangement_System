# Assignment Information
# Author: Pedro Gonzalez San Martin
# Date: 10-17-2026
# Assignment: Programming Assignment - Student Record Management System

# =============================================================================
# Student Record Management System
# Programming Fundamentals with Python - Week 8 Debugging Exercise
#
# This program reads student data from a CSV file and provides a menu-driven
# interface to list all students and search for a student by ID.
# All 10 deliberate bugs from the original student_records.py have been fixed
# while preserving the original top-down, procedural structure.
# =============================================================================

import csv

# -----------------------------------------------------------------------------
# Global Variables
# -----------------------------------------------------------------------------
student_records = []        # Holds all student records loaded from the CSV
csv_filename = ""           # Stores the filename entered by the user
menu_choice = ""            # Stores the user's menu selection
csv_loaded = False          # Tracks whether a CSV file has been loaded

search_id = ""              # Stores the Student ID entered during a search
found_student = None        # Stores the matching student record, if found
search_index = 0            # Loop counter used during linear search

row_number = 0              # Loop counter used when printing student records
current_student = None      # Holds the current record during iteration

student_id = ""             # Fields parsed from each CSV row
student_name = ""
major = ""
gpa = ""
total_credits = ""

# =============================================================================
# Main Program Loop
# =============================================================================

print("=" * 60)
print("   Student Record Management System")
print("=" * 60)

while True:

    # -------------------------------------------------------------------------
    # Display Menu
    # -------------------------------------------------------------------------
    print()
    print("Please select an option:")
    print("  1. Read CSV")
    print("  2. List CSV Contents")
    print("  3. Search for Student by ID")
    print("  4. Exit")
    print()

    menu_choice = input("Enter your choice (1-4): ").strip()

    # =========================================================================
    # Option 1: Read CSV
    # =========================================================================
    if menu_choice == "1":

        csv_filename = input("Enter the CSV filename (e.g., students.csv): ").strip()

        # Bug 3 fix: clear any previously loaded records before reloading so
        # that rows do not accumulate (10 records stays 10, not 20).
        student_records = []

        # Bug 1 fix: keep the file open while csv.DictReader iterates by using
        # a context manager instead of closing the file before the loop.
        try:
            with open(csv_filename, newline="") as csv_file:
                csv_reader = csv.DictReader(csv_file)

                for row in csv_reader:
                    student_id     = row["StudentID"]
                    student_name   = row["StudentName"]
                    major          = row["Major"]
                    gpa            = row["GPA"]
                    total_credits  = row["TotalCredits"]

                    student_record = {
                        "StudentID"    : student_id,
                        "StudentName"  : student_name,
                        "Major"        : major,
                        "GPA"          : gpa,
                        "TotalCredits" : total_credits
                    }

                    student_records.append(student_record)

            # Bug 4 fix: mark the data as loaded so Options 2 and 3 work.
            csv_loaded = True

            print()
            print(f"Success! {len(student_records)} student record(s) loaded from '{csv_filename}'.")

        except FileNotFoundError:
            csv_loaded = False
            print()
            print(f"Error: The file '{csv_filename}' was not found. Please check the filename and try again.")

    # =========================================================================
    # Option 2: List CSV Contents
    # =========================================================================
    elif menu_choice == "2":

        if not csv_loaded:
            print()
            print("No data loaded. Please use Option 1 to read a CSV file first.")

        else:
            print()
            print("-" * 80)
            print(f"{'#':<5} {'Student ID':<12} {'Student Name':<22} {'Major':<24} {'GPA':<6} {'Credits'}")
            print("-" * 82)

            row_number = 1

            for current_student in student_records:
                print(
                    f"{row_number:<5}"
                    f"{current_student['StudentID']:<12}"
                    f"{current_student['StudentName']:<22}"
                    f"{current_student['Major']:<24}"
                    f"{current_student['GPA']:<6}"
                    f"{current_student['TotalCredits']}"
                )
                # Bug 5 fix: increment the row counter in the display loop.
                row_number += 1

            print("-" * 82)
            print(f"Total records: {len(student_records)}")

    # =========================================================================
    # Option 3: Search for Student by ID
    # =========================================================================
    elif menu_choice == "3":

        if not csv_loaded:
            print()
            print("No data loaded. Please use Option 1 to read a CSV file first.")

        else:
            # Bug 9 fix: normalize the search input (case-insensitive search).
            search_id = input("Enter the Student ID to search for: ").strip().upper()

            # Bug 6 fix: reset the previous match so a failed search does not
            # retain the student found by an earlier search.
            found_student = None

            search_index = 0

            # Bug 7 fix: use '<' instead of '<=' to avoid IndexError.
            while search_index < len(student_records):
                if student_records[search_index]["StudentID"].upper() == search_id:
                    found_student = student_records[search_index]
                    # Bug 10 fix: break out of the loop instead of setting the
                    # index to len(...) - 1, which looped forever on the last row.
                    break
                else:
                    search_index = search_index + 1

            print()

            if found_student is None:
                print(f"No student found with ID '{search_id}'.")
            else:
                print("Student found!")
                print("-" * 40)
                # Bug 2 fix: use the correct 'StudentID' key.
                print(f"  Student ID    : {found_student['StudentID']}")
                print(f"  Student Name  : {found_student['StudentName']}")
                print(f"  Major         : {found_student['Major']}")
                print(f"  GPA           : {found_student['GPA']}")
                print(f"  Total Credits : {found_student['TotalCredits']}")
                print("-" * 40)

    # =========================================================================
    # Option 4: Exit
    # =========================================================================
    # Bug 8 fix: compare against the string "4" because input() returns text.
    elif menu_choice == "4":
        print()
        print("Thank you for using the Student Record Management System. Goodbye!")
        break

    # =========================================================================
    # Invalid Input
    # =========================================================================
    else:
        print()
        print(f"'{menu_choice}' is not a valid option. Please enter 1, 2, 3, or 4.")