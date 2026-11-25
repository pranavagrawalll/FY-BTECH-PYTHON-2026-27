
# ==========================================
# DEIVS - EVIDENCE MANAGEMENT MODULE
# ==========================================

import os
import tkinter as tk
from tkinter import filedialog

from hashing import calculate_sha256

from database import (
    add_evidence,
    get_all_evidence,
    get_evidence_by_id,
    delete_evidence_record,
    get_deleted_evidence
)


# ------------------------------------------
# 1. SELECT EVIDENCE FILE
# ------------------------------------------

def select_evidence_file():

    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Select Digital Evidence",
        filetypes=[
            ("All Files", "*.*"),
            ("Images", "*.jpg *.jpeg *.png"),
            ("Videos", "*.mp4 *.mkv *.avi"),
            ("Documents", "*.pdf *.docx *.txt")
        ]
    )

    root.destroy()

    return file_path


# ------------------------------------------
# 2. REGISTER NEW EVIDENCE
# ------------------------------------------

def register_evidence():

    print("\n===== REGISTER NEW EVIDENCE =====")

    file_path = select_evidence_file()

    if not file_path:
        print("No file selected!")
        return

    try:

        file_path = os.path.abspath(file_path)

        file_name = os.path.basename(file_path)

        file_size = os.path.getsize(file_path)

        file_hash = calculate_sha256(file_path)

        if file_hash is None:
            print("Unable to calculate file hash!")
            return

        evidence_id = add_evidence(
            file_name,
            file_path,
            file_size,
            file_hash
        )

        print("\nEvidence Registered Successfully!")
        print("-----------------------------------")

        print("Evidence ID:", evidence_id)
        print("File Name:", file_name)
        print("File Size:", file_size, "bytes")
        print("SHA-256:", file_hash)
        print("File Location:", file_path)

        print("-----------------------------------")

    except OSError as error:

        print("File operation failed:", error)


# ------------------------------------------
# 3. VIEW ALL ACTIVE EVIDENCE
# ------------------------------------------

def view_all_evidence():

    records = get_all_evidence()

    if not records:
        print("\nNo active evidence records found!")
        return

    print("\n========== REGISTERED EVIDENCE ==========")

    for record in records:

        print("\nEvidence ID:", record[0])
        print("File Name:", record[1])
        print("File Size:", record[3], "bytes")
        print("Original Hash:", record[4])
        print("Registration Date:", record[5])
        print("Status:", record[6])

        print("-----------------------------------------")


# ------------------------------------------
# 4. SEARCH EVIDENCE BY ID
# ------------------------------------------

def search_evidence():

    try:
        evidence_id = int(input("\nEnter Evidence ID: "))

    except ValueError:
        print("Please enter a valid numeric ID!")
        return

    record = get_evidence_by_id(evidence_id)

    if record is None:
        print("\nEvidence not found!")
        return

    print("\n========== EVIDENCE DETAILS ==========")

    print("Evidence ID:", record[0])
    print("File Name:", record[1])
    print("File Location:", record[2])
    print("File Size:", record[3], "bytes")
    print("Original SHA-256:", record[4])
    print("Registration Date:", record[5])
    print("Status:", record[6])

    if record[7]:
        print("Deleted At:", record[7])

    print("======================================")


# ------------------------------------------
# 5. DELETE / ARCHIVE EVIDENCE
# ------------------------------------------

def delete_evidence():

    print("\n===== DELETE EVIDENCE RECORD =====")

    try:
        evidence_id = int(input("Enter Evidence ID: "))

    except ValueError:
        print("Please enter a valid numeric ID!")
        return

    record = get_evidence_by_id(evidence_id)

    if record is None:
        print("\nEvidence ID not found!")
        return

    if record[6] == "DELETED":
        print("\nThis evidence is already deleted!")
        return

    print("\nEvidence Details")
    print("Evidence ID:", record[0])
    print("File Name:", record[1])
    print("Original SHA-256:", record[4])

    print("\nWARNING:")
    print("This will remove the record from active evidence.")
    print("The original file will NOT be deleted.")
    print("The database record and verification history will remain.")

    confirmation = input(
        "\nType YES to confirm deletion: "
    ).strip()

    if confirmation != "YES":
        print("\nDeletion cancelled.")
        return

    result = delete_evidence_record(evidence_id)

    if result == "DELETED":

        print("\nEvidence successfully archived!")
        print("Record status changed to DELETED.")

    elif result == "NOT_FOUND":

        print("\nEvidence record not found!")

    elif result == "ALREADY_DELETED":

        print("\nEvidence is already deleted!")


# ------------------------------------------
# 6. VIEW DELETED EVIDENCE
# ------------------------------------------

def view_deleted_evidence():

    records = get_deleted_evidence()

    if not records:
        print("\nNo deleted evidence records found!")
        return

    print("\n========== DELETED EVIDENCE ==========")

    for record in records:

        print("\nEvidence ID:", record[0])
        print("File Name:", record[1])
        print("Original Hash:", record[4])
        print("Registration Date:", record[5])
        print("Status:", record[6])
        print("Deleted At:", record[7])

        print("--------------------------------------")


# ------------------------------------------
# TEST EVIDENCE MANAGEMENT MODULE
# ------------------------------------------

if __name__ == "__main__":

    print("\n===== DEIVS EVIDENCE MANAGEMENT =====")

    print("1. Register New Evidence")
    print("2. View All Evidence")
    print("3. Search Evidence")
    print("4. Delete Evidence")
    print("5. View Deleted Evidence")

    choice = input("\nEnter your choice: ").strip()

    if choice == "1":
        register_evidence()

    elif choice == "2":
        view_all_evidence()

    elif choice == "3":
        search_evidence()

    elif choice == "4":
        delete_evidence()

    elif choice == "5":
        view_deleted_evidence()

    else:
        print("Invalid choice!")
