# Assignment Information
# Author: Pedro Gonzalez San Martin
# Date: 10-17-2026
# Assignment: Programming Assignment - Student Record Management System

# =============================================================================
# Student Record Management System (Refactored)
# Programming Fundamentals with Python - Week 8 Refactoring Exercise
#
# This program reads student data from a CSV file and provides a menu-driven
# interface to list all students and search for a student by ID. It has been
# redesigned into a modular object-oriented architecture:
#   - Student / GraduateStudent : model a single student record
#   - StudentRoster             : owns all state and the menu loop
#
# Requirements satisfied: R-01 classes/OOP, R-02 encapsulation (no globals),
# R-03 methods, R-04 binary search, R-05 exception handling,
# R-06 string normalization, R-07 csv.DictReader, R-08 inheritance bonus.
# =============================================================================

import csv


# -----------------------------------------------------------------------------
# R-01: Student class
# -----------------------------------------------------------------------------
class Student:
    """Represents a single student record loaded from the CSV dataset."""

    def __init__(self, student_id, student_name, major, gpa, total_credits):
        # R-06: store identifiers and text fields normalized for comparisons.
        self.student_id = str(student_id).strip().upper()
        self.student_name = str(student_name).strip()
        self.major = str(major).strip()
        self.gpa = str(gpa).strip()
        self.total_credits = str(total_credits).strip()

    def __str__(self):
        # Returns the clean formatted multiline display block for a student.
        lines = [
            "Student found!",
            "-" * 40,
            f"  Student ID    : {self.student_id}",
            f"  Student Name  : {self.student_name}",
            f"  Major         : {self.major}",
            f"  GPA           : {self.gpa}",
            f"  Total Credits : {self.total_credits}",
            "-" * 40,
        ]
        return "\n".join(lines)

    def row_cells(self):
        # Returns the column values used by the table display in StudentRoster.
        return [
            self.student_id,
            self.student_name,
            self.major,
            self.gpa,
            self.total_credits,
        ]


# -----------------------------------------------------------------------------
# R-01 / R-08 (Bonus): GraduateStudent subclass
# -----------------------------------------------------------------------------
class GraduateStudent(Student):
    """A Student that additionally tracks a thesis topic (overrides __str__)."""

    def __init__(self, student_id, student_name, major, gpa,
                 total_credits, thesis_topic=""):
        # Reuse the parent constructor for the shared attributes.
        super().__init__(student_id, student_name, major, gpa, total_credits)
        self.thesis_topic = str(thesis_topic).strip()

    def __str__(self):
        # Reuse the parent display block and append the thesis information.
        base = super().__str__()
        if self.thesis_topic:
            extra = f"  Thesis Topic  : {self.thesis_topic}"
        else:
            extra = "  Thesis Topic  : (not set)"
        return f"{base}\n{extra}"


# -----------------------------------------------------------------------------
# R-01 / R-02: StudentRoster class (owns all state; no global variables)
# -----------------------------------------------------------------------------
class StudentRoster:
    """Manages the collection of student records and the menu interface."""

    def __init__(self):
        # R-02: all state lives inside the instance, replacing global variables.
        self.students = []
        self.csv_loaded = False
        self.filename = ""

    # -------------------------------------------------------------------------
    # R-03 / R-05 / R-06 / R-07: load_csv
    # -------------------------------------------------------------------------
    def load_csv(self, filename):
        """Reads the CSV file, creates Student objects, and resets the roster."""
        self.filename = str(filename).strip()

        # Bug 3 fix (logic): reset the roster so reloads never accumulate.
        self.students = []
        # Bug 4 fix (logic): default to False until a load fully succeeds.
        self.csv_loaded = False

        # R-05: no crashes on a missing file.
        try:
            with open(self.filename, newline="") as csv_file:
                csv_reader = csv.DictReader(csv_file)

                for row in csv_reader:
                    # R-05: skip malformed rows instead of crashing on KeyError.
                    try:
                        student = Student(
                            row["StudentID"],
                            row["StudentName"],
                            row["Major"],
                            row["GPA"],
                            row["TotalCredits"],
                        )
                    except KeyError:
                        print("Warning: Skipping a malformed row with missing columns.")
                        continue
                    self.students.append(student)

        except FileNotFoundError:
            print()
            print(f"Error: The file '{self.filename}' was not found. "
                  "Please check the filename and try again.")
            return False

        # R-04: sort by student_id so binary search is guaranteed correct.
        self.students.sort(key=lambda student: student.student_id)

        # Bug 4 fix (logic): flag the successful load so Options 2 and 3 work.
        self.csv_loaded = True

        print()
        print(f"Success! {len(self.students)} student record(s) loaded "
              f"from '{self.filename}'.")
        return True

    # -------------------------------------------------------------------------
    # R-03: list_students (aligned 6-column table with row numbers and totals)
    # -------------------------------------------------------------------------
    def list_students(self):
        """Prints all student records in an aligned table."""
        # R-05 style guard: friendly message when nothing has been loaded.
        if not self.csv_loaded:
            print()
            print("No data loaded. Please use Option 1 to read a CSV file first.")
            return

        print()
        print("-" * 80)
        print(f"{'#':<5} {'Student ID':<12} {'Student Name':<22} "
              f"{'Major':<24} {'GPA':<6} {'Credits'}")
        print("-" * 82)

        # Bug 5 fix (logic): increment the row number on every iteration.
        row_number = 1
        for student in self.students:
            cells = student.row_cells()
            print(
                f"{row_number:<5}"
                f"{cells[0]:<12}"
                f"{cells[1]:<22}"
                f"{cells[2]:<24}"
                f"{cells[3]:<6}"
                f"{cells[4]}"
            )
            row_number += 1

        print("-" * 82)
        print(f"Total records: {len(self.students)}")

    # -------------------------------------------------------------------------
    # R-03 / R-04 / R-06: search_by_id using explicit binary search
    # -------------------------------------------------------------------------
    def search_by_id(self, search_id):
        """Locates a student by ID using binary search and displays the record."""
        # R-05 style guard: friendly message when nothing has been loaded.
        if not self.csv_loaded:
            print()
            print("No data loaded. Please use Option 1 to read a CSV file first.")
            return None

        # Bug 9 fix (subtle logic) + R-06: normalize the search key.
        target = str(search_id).strip().upper()

        # R-04: explicit binary search. No list.index(), no 'in', no dict lookup.
        low = 0
        high = len(self.students) - 1
        found = None

        while low <= high:
            mid = (low + high) // 2
            current_id = self.students[mid].student_id

            if current_id == target:
                found = self.students[mid]
                break
            elif current_id < target:
                # Target is alphabetically after the middle record.
                low = mid + 1
            else:
                # Target is alphabetically before the middle record.
                high = mid - 1

        print()

        # Bug 6 fix (logic): 'found' starts as None on every call, so a failed
        # search never reuses the result of an earlier search.
        if found is None:
            print(f"No student found with ID '{target}'.")
        else:
            # Student.__str__ produces the formatted display block.
            print(found)

        return found

    # -------------------------------------------------------------------------
    # R-03: run (houses the menu loop)
    # -------------------------------------------------------------------------
    def run(self):
        """Displays the menu and dispatches each option until the user exits."""
        print("=" * 60)
        print("   Student Record Management System")
        print("=" * 60)

        while True:
            print()
            print("Please select an option:")
            print("  1. Read CSV")
            print("  2. List CSV Contents")
            print("  3. Search for Student by ID")
            print("  4. Exit")
            print()

            menu_choice = input("Enter your choice (1-4): ").strip()

            if menu_choice == "1":
                filename = input(
                    "Enter the CSV filename (e.g., students.csv): "
                ).strip()
                self.load_csv(filename)

            elif menu_choice == "2":
                self.list_students()

            elif menu_choice == "3":
                search_id = input("Enter the Student ID to search for: ")
                self.search_by_id(search_id)

            elif menu_choice == "4":
                print()
                print("Thank you for using the Student Record Management "
                      "System. Goodbye!")
                break

            else:
                print()
                print(f"'{menu_choice}' is not a valid option. "
                      "Please enter 1, 2, 3, or 4.")


# -----------------------------------------------------------------------------
# Main execution guard
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    roster = StudentRoster()
    roster.run()