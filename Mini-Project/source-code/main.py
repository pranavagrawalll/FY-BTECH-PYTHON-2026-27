
# ==========================================
# DEIVS - DIGITAL EVIDENCE INTEGRITY SYSTEM
# MAIN APPLICATION
# ==========================================

from database import (
    initialize_database,
    get_verification_history
)

from evidence_manager import (
    register_evidence,
    view_all_evidence,
    search_evidence,
    delete_evidence,
    view_deleted_evidence
)

from verification import verify_evidence

from report import generate_report

from reset_project import reset_database


# ------------------------------------------
# 1. DISPLAY MAIN MENU
# ------------------------------------------

def display_menu():

    print("\n")
    print("=" * 60)
    print("          DIGITAL EVIDENCE INTEGRITY SYSTEM")
    print("=" * 60)

    print("\n--- EVIDENCE MANAGEMENT ---")

    print("1. Register New Evidence")
    print("2. View All Active Evidence")
    print("3. Search Evidence by ID")
    print("4. Verify Evidence Integrity")

    print("\n--- REPORTS & HISTORY ---")

    print("5. Generate Investigation PDF Report")
    print("6. View Verification History")

    print("\n--- RECORD MANAGEMENT ---")

    print("7. Delete Evidence")
    print("8. View Deleted Evidence")

    print("\n--- SYSTEM MANAGEMENT ---")

    print("9. Reset Database (Fresh Start)")
    print("10. Exit")

    print("\n" + "=" * 60)


# ------------------------------------------
# 2. VIEW VERIFICATION HISTORY
# ------------------------------------------

def display_verification_history():

    try:

        evidence_id = int(
            input("\nEnter Evidence ID: ")
        )

    except ValueError:

        print("Please enter a valid numeric ID!")
        return

    history = get_verification_history(evidence_id)

    if not history:

        print("\nNo verification history found!")
        return

    print("\n========== VERIFICATION HISTORY ==========")

    for record in history:

        print("\nVerification ID:", record[0])
        print("Evidence ID:", record[1])
        print("Current Hash:", record[2])
        print("Status:", record[3])
        print("Verification Date:", record[4])

        print("------------------------------------------")


# ------------------------------------------
# 3. MAIN APPLICATION
# ------------------------------------------

def main():

    # Initialize database
    initialize_database()

    print("\nWelcome to DEIVS!")
    print("Digital Forensic Evidence Management System")

    while True:

        display_menu()

        choice = input(
            "\nEnter your choice (1-10): "
        ).strip()

        # Register Evidence
        if choice == "1":

            register_evidence()

        # View Active Evidence
        elif choice == "2":

            view_all_evidence()

        # Search Evidence
        elif choice == "3":

            search_evidence()

        # Verify Evidence
        elif choice == "4":

            try:

                evidence_id = int(
                    input("\nEnter Evidence ID: ")
                )

                verify_evidence(evidence_id)

            except ValueError:

                print("Invalid Evidence ID!")

        # Generate PDF Report
        elif choice == "5":

            try:

                evidence_id = int(
                    input("\nEnter Evidence ID: ")
                )

                generate_report(evidence_id)

            except ValueError:

                print("Invalid Evidence ID!")

        # View Verification History
        elif choice == "6":

            display_verification_history()

        # Delete Evidence
        elif choice == "7":

            delete_evidence()

        # View Deleted Evidence
        elif choice == "8":

            view_deleted_evidence()

        # Reset Database
        elif choice == "9":

            reset_database()

        # Exit Application
        elif choice == "10":

            print("\nThank you for using DEIVS!")
            print("Application closed successfully.")

            break

        else:

            print("\nInvalid choice! Please select 1-10.")


# ------------------------------------------
# 4. PROGRAM ENTRY POINT
# ------------------------------------------

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print("\n\nApplication interrupted by user.")
