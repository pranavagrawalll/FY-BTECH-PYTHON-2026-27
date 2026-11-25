# DEIVS – Digital Evidence Integrity & Verification System

**A Python-Based Digital Forensics Desktop Application**

DEIVS (Digital Evidence Integrity & Verification System) is a Python-based digital forensics academic project designed to register, manage, archive, restore, and verify the integrity of digital evidence using SHA-256 cryptographic hashing.

The application provides a graphical desktop interface for digital evidence management, integrity verification, verification history tracking, and PDF investigation report generation.

DEIVS is available as a desktop application for **macOS and Windows**, supporting multiple processor architectures.

---

## Project Team

| Name | PRN | Contribution |
|---|---|---|
| Pranav Mohan Agrawal | 1272260373 | Software Development & Code Implementation |
| Rujula Jadhav | 1272261758 | Presentation (PPT) Preparation |
| Swayam Dakare | 1272261583 | Project Poster Design |
| Samruddhi Salunke | 1272261145 | Project Presentation |

---

## Features

### 1. Digital Evidence Registration
- Register and manage digital evidence files.
- Generate SHA-256 cryptographic hashes during registration.
- Store evidence information in a local SQLite database.

### 2. SHA-256 Integrity Verification
- Generate and verify cryptographic hashes.
- Detect whether registered evidence has been modified.
- Identify missing or unchanged evidence files.

### 3. Evidence Management
- View, search, and manage registered evidence records.
- Access evidence details.
- Archive registered evidence.
- Restore archived evidence.
- Permanently delete archived evidence when required.

### 4. Verification History
- Maintain a record of previous integrity verification activities.
- Store verification results and timestamps.
- Review historical verification information.

### 5. PDF Investigation Reports
- Generate detailed PDF investigation reports.
- Include evidence information and verification results.
- Select a custom location to save generated reports.
- Open generated reports or their containing folder directly.

### 6. Database Management
- Store evidence records and verification history locally using SQLite.
- Maintain persistent application data across sessions.

### 7. User Interface
- Graphical desktop interface developed using Python Tkinter.
- Dashboard displaying evidence statistics.
- Navigation between different application modules.
- Automatic horizontal and vertical scrollbars.
- Scrollbars appear only when content exceeds the visible area.

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core application development |
| Tkinter | Graphical User Interface |
| SQLite | Local database management |
| SHA-256 | Cryptographic hashing |
| ReportLab | PDF report generation |
| PyInstaller | Desktop application packaging |
| Git & GitHub | Version control and project hosting |
| GitHub Actions | Automated cross-platform application builds |

---

## Application Release – v1.0.0

<badge>Latest Release</badge>

**DEIVS v1.0.0 – Desktop Application (macOS & Windows)**

Download the application from the official GitHub Releases page:

**[Download DEIVS v1.0.0](https://github.com/pranavagrawalll/DEIVS-Digital-Evidence-Integrity-System/releases/tag/v1.0.0)**

### Available Downloads

Choose the ZIP file matching the operating system and processor architecture.

**macOS**
- Apple Silicon (ARM64): `DEIVS-macOS.zip`
- Intel (x86_64): `DEIVS-macOS-Intel.zip`

**Windows**
- x64 (64-bit): `DEIVS-Windows-x64.zip`
- x86 (32-bit): `DEIVS-Windows-x86.zip`
- ARM64: `DEIVS-Windows-ARM64.zip`

All application ZIP files are available in the Assets section of the GitHub release.

---

## Installation Instructions

### macOS – Apple Silicon and Intel

1. Open the [DEIVS v1.0.0 Releases page](https://github.com/pranavagrawalll/DEIVS-Digital-Evidence-Integrity-System/releases/tag/v1.0.0).
2. Download the appropriate ZIP file:
   - Apple Silicon: `DEIVS-macOS.zip`
   - Intel: `DEIVS-macOS-Intel.zip`
3. Extract the downloaded ZIP file.
4. Locate `DEIVS.app`.
5. Open the application.

### macOS Security Notice

DEIVS is an academic project and is currently not signed with an Apple Developer ID certificate or notarized by Apple.

As a result, macOS Gatekeeper may display a security warning when launching the application for the first time.

If macOS displays a warning that the developer cannot be verified, follow these steps:

1. First, try opening `DEIVS.app`.
2. Open **Apple Menu → System Settings**.
3. Navigate to **Privacy & Security**.
4. Scroll down to the **Security** section.
5. Locate the message indicating that DEIVS was blocked.
6. Click **Open Anyway**.
7. Confirm by clicking **Open** when prompted.

Only follow these steps when the application has been downloaded from the official DEIVS GitHub repository and its release.

**Important:** Do not bypass warnings stating that an application will damage your Mac or that the application is damaged.

For additional information, refer to Apple's official support documentation:

[Safely open apps on your Mac – Apple Support](https://support.apple.com/en-in/102445)

### Windows – x64, x86 and ARM64

1. Open the [DEIVS v1.0.0 Releases page](https://github.com/pranavagrawalll/DEIVS-Digital-Evidence-Integrity-System/releases/tag/v1.0.0).
2. Download the ZIP file matching your Windows architecture:
   - `DEIVS-Windows-x64.zip`
   - `DEIVS-Windows-x86.zip`
   - `DEIVS-Windows-ARM64.zip`
3. Extract the downloaded ZIP file.
4. Open the extracted `DEIVS` folder.
5. Double-click `DEIVS.exe` to launch the application.

### Windows Security Notice

Windows SmartScreen or antivirus software may display a warning because the application is not digitally signed.

Only proceed if the application was downloaded from the official DEIVS GitHub Releases page and the source is trusted. Do not bypass malware or security warnings without verifying the file.

---

## Running from Source Code

To run DEIVS directly from the source code, follow these steps.

### Prerequisites

- Python 3.10 or later
- Git
- pip

### Step 1: Clone the Repository

```bash
git clone https://github.com/pranavagrawalll/DEIVS-Digital-Evidence-Integrity-System.git
```

### Step 2: Navigate to the Project Directory

```bash
cd DEIVS-Digital-Evidence-Integrity-System
```

### Step 3: Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment.

**macOS / Linux:**

```bash
source .venv/bin/activate
```

**Windows:**

```bash
.venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run the Application

```bash
python gui.py
```

---

## Project Structure

```text
DEIVS/
│
├── gui.py                 # Main graphical user interface
├── database.py            # SQLite database operations
├── hashing.py             # SHA-256 hashing functionality
├── report.py              # PDF report generation
├── app_paths.py           # Application data path management
├── main.py                # CLI application entry point
├── verification.py        # Verification functionality
├── evidence_manager.py    # Evidence management operations
├── reset_project.py       # Project reset utility
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
│
└── .gitignore             # Git ignored files
```

---

## Data Storage

DEIVS stores its application data locally on the user's computer.

- **Database:** SQLite database containing evidence records and verification history.
- **Reports:** PDF reports are saved at the location selected by the user.
- **Application Data:** Persistent application data is maintained in the operating system's application data directory.

The application does not require a cloud database for its core functionality.

**Important:** Keep backups of important evidence files and application database data. Avoid deleting the application data directory if existing records need to be preserved.

---

## Project Information

DEIVS is an academic project developed as part of a group project.

The application is intended for educational and demonstration purposes. It demonstrates digital evidence registration, cryptographic integrity verification, evidence management, and report generation.

It is not intended to replace professional digital forensic tools or certified forensic laboratory procedures.

---

## Release Information

- **Current Version:** v1.0.0
- **Release Title:** DEIVS v1.0.0 – Desktop Application (macOS & Windows)
- **Project:** Digital Evidence Integrity & Verification System (DEIVS)
- **Supported Platforms:** macOS and Windows
- **Architectures:** Apple Silicon, Intel x86_64, Windows x64, Windows x86 and Windows ARM64
- **Repository:** [DEIVS – GitHub](https://github.com/pranavagrawalll/DEIVS-Digital-Evidence-Integrity-System)
- **Releases:** [Download the latest release](https://github.com/pranavagrawalll/DEIVS-Digital-Evidence-Integrity-System/releases)

---

**Developed as an Academic Group Project**

**DEIVS – Digital Evidence Integrity & Verification System**
