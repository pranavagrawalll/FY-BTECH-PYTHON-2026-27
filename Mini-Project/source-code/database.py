
# ==========================================
# DEIVS - DATABASE MANAGEMENT MODULE
# ==========================================

import sqlite3
from datetime import datetime

from app_paths import get_database_path

DATABASE_NAME = get_database_path()


# ------------------------------------------
# 1. CONNECT TO DATABASE
# ------------------------------------------

def connect_database():

    connection = sqlite3.connect(str(DATABASE_NAME))
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


# ------------------------------------------
# 2. INITIALIZE DATABASE
# ------------------------------------------

def initialize_database():

    connection = connect_database()

    try:
        cursor = connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS evidence (
            evidence_id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            file_path TEXT NOT NULL,
            file_size INTEGER,
            original_hash TEXT NOT NULL,
            registration_date TEXT NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS verification_history (
            verification_id INTEGER PRIMARY KEY AUTOINCREMENT,
            evidence_id INTEGER NOT NULL,
            current_hash TEXT,
            verification_status TEXT NOT NULL,
            verification_date TEXT NOT NULL,
            FOREIGN KEY (evidence_id)
            REFERENCES evidence(evidence_id)
        )
        """)

        cursor.execute("PRAGMA table_info(evidence)")
        columns = [column[1] for column in cursor.fetchall()]

        if "status" not in columns:
            cursor.execute("""
            ALTER TABLE evidence
            ADD COLUMN status TEXT NOT NULL DEFAULT 'ACTIVE'
            """)

        if "deleted_at" not in columns:
            cursor.execute("""
            ALTER TABLE evidence
            ADD COLUMN deleted_at TEXT
            """)

        connection.commit()

        print("Database initialized successfully!")

    finally:
        connection.close()


# ------------------------------------------
# 3. ADD NEW EVIDENCE
# ------------------------------------------

def add_evidence(file_name, file_path, file_size, original_hash):

    connection = connect_database()

    try:
        cursor = connection.cursor()

        registration_date = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        cursor.execute("""
        INSERT INTO evidence
        (file_name, file_path, file_size,
         original_hash, registration_date)
        VALUES (?, ?, ?, ?, ?)
        """, (
            file_name,
            file_path,
            file_size,
            original_hash,
            registration_date
        ))

        evidence_id = cursor.lastrowid
        connection.commit()

        return evidence_id

    finally:
        connection.close()


# ------------------------------------------
# 4. GET EVIDENCE BY ID
# ------------------------------------------

def get_evidence_by_id(evidence_id):

    connection = connect_database()

    try:
        cursor = connection.cursor()

        cursor.execute("""
        SELECT * FROM evidence
        WHERE evidence_id = ?
        """, (evidence_id,))

        return cursor.fetchone()

    finally:
        connection.close()


# ------------------------------------------
# 5. GET ALL ACTIVE EVIDENCE
# ------------------------------------------

def get_all_evidence():

    connection = connect_database()

    try:
        cursor = connection.cursor()

        cursor.execute("""
        SELECT * FROM evidence
        WHERE status = 'ACTIVE'
        ORDER BY evidence_id
        """)

        return cursor.fetchall()

    finally:
        connection.close()


# ------------------------------------------
# 6. SAVE VERIFICATION HISTORY
# ------------------------------------------

def save_verification(evidence_id, current_hash, status):

    connection = connect_database()

    try:
        cursor = connection.cursor()

        verification_date = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        cursor.execute("""
        INSERT INTO verification_history
        (evidence_id, current_hash,
         verification_status, verification_date)
        VALUES (?, ?, ?, ?)
        """, (
            evidence_id,
            current_hash,
            status,
            verification_date
        ))

        connection.commit()

        print("Verification history saved successfully!")

    finally:
        connection.close()


# ------------------------------------------
# 7. GET VERIFICATION HISTORY
# ------------------------------------------

def get_verification_history(evidence_id):

    connection = connect_database()

    try:
        cursor = connection.cursor()

        cursor.execute("""
        SELECT * FROM verification_history
        WHERE evidence_id = ?
        ORDER BY verification_id DESC
        """, (evidence_id,))

        return cursor.fetchall()

    finally:
        connection.close()


# ------------------------------------------
# 8. SOFT DELETE EVIDENCE
# ------------------------------------------

def delete_evidence_record(evidence_id):

    connection = connect_database()

    try:
        cursor = connection.cursor()

        cursor.execute("""
        SELECT status FROM evidence
        WHERE evidence_id = ?
        """, (evidence_id,))

        record = cursor.fetchone()

        if record is None:
            return "NOT_FOUND"

        if record[0] == "DELETED":
            return "ALREADY_DELETED"

        deleted_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        cursor.execute("""
        UPDATE evidence
        SET status = 'DELETED',
            deleted_at = ?
        WHERE evidence_id = ?
        """, (deleted_time, evidence_id))

        connection.commit()

        return "DELETED"

    finally:
        connection.close()


# ------------------------------------------
# 9. VIEW DELETED EVIDENCE
# ------------------------------------------

def get_deleted_evidence():

    connection = connect_database()

    try:
        cursor = connection.cursor()

        cursor.execute("""
        SELECT * FROM evidence
        WHERE status = 'DELETED'
        ORDER BY evidence_id
        """)

        return cursor.fetchall()

    finally:
        connection.close()


# ------------------------------------------
# 10. RESTORE ARCHIVED EVIDENCE
# ------------------------------------------

def restore_evidence_record(evidence_id):

    connection = connect_database()

    try:
        cursor = connection.cursor()

        cursor.execute("""
        SELECT status FROM evidence
        WHERE evidence_id = ?
        """, (evidence_id,))

        record = cursor.fetchone()

        if record is None:
            return "NOT_FOUND"

        if record[0] == "ACTIVE":
            return "ALREADY_ACTIVE"

        cursor.execute("""
        UPDATE evidence
        SET status = 'ACTIVE',
            deleted_at = NULL
        WHERE evidence_id = ?
        """, (evidence_id,))

        connection.commit()

        return "RESTORED"

    finally:
        connection.close()


# ------------------------------------------
# 11. PERMANENTLY DELETE ARCHIVED EVIDENCE
# ------------------------------------------

def permanently_delete_evidence_record(evidence_id):

    connection = connect_database()

    try:
        cursor = connection.cursor()

        cursor.execute("""
        SELECT status FROM evidence
        WHERE evidence_id = ?
        """, (evidence_id,))

        record = cursor.fetchone()

        if record is None:
            return "NOT_FOUND"

        if record[0] != "DELETED":
            return "NOT_ARCHIVED"

        cursor.execute("""
        DELETE FROM verification_history
        WHERE evidence_id = ?
        """, (evidence_id,))

        cursor.execute("""
        DELETE FROM evidence
        WHERE evidence_id = ?
        """, (evidence_id,))

        connection.commit()

        return "PERMANENTLY_DELETED"

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


# ------------------------------------------
# TEST DATABASE MODULE
# ------------------------------------------

if __name__ == "__main__":

    print("\n===== DEIVS DATABASE SYSTEM =====")

    initialize_database()

    records = get_all_evidence()

    print("Total Active Evidence:", len(records))
    print("Database Location:", DATABASE_NAME)
    print("Database Module Working Successfully!")
