
# ==========================================
# DEIVS - SHA-256 HASHING MODULE
# ==========================================

import hashlib
import os


def calculate_sha256(file_path):

    sha256_hash = hashlib.sha256()

    try:
        with open(file_path, "rb") as file:

            while True:

                data = file.read(4096)

                if not data:
                    break

                sha256_hash.update(data)

        return sha256_hash.hexdigest()

    except OSError as error:

        print("Error reading file:", error)
        return None


# ==========================================
# TESTING THE HASHING MODULE
# ==========================================

if __name__ == "__main__":

    print("\n===== DEIVS SHA-256 HASHING =====")

    file_path = "test_evidence.txt"

    if os.path.isfile(file_path):

        file_hash = calculate_sha256(file_path)

        if file_hash:

            print("File Name:", os.path.basename(file_path))
            print("SHA-256 Hash:", file_hash)
            print("Hash Generated Successfully!")

    else:

        print("Test evidence file not found!")
