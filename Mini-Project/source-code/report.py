
# ==========================================
# DEIVS - INVESTIGATION REPORT GENERATOR
# ==========================================

from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from database import (
    get_evidence_by_id,
    get_verification_history
)

from app_paths import get_reports_dir


# ------------------------------------------
# 1. GENERATE PDF REPORT
# ------------------------------------------

def generate_report(evidence_id, output_path=None):

    # Retrieve evidence details
    record = get_evidence_by_id(evidence_id)

    if record is None:
        print("Evidence ID not found!")
        return

    # Retrieve verification history
    history = get_verification_history(evidence_id)

    # Get latest verification record
    latest_verification = history[0] if history else None

    # Generate a suggested filename and resolve the chosen save destination.
    report_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    suggested_name = f"DEIVS_Report_{evidence_id}_{report_time}.pdf"

    if output_path is None:
        report_path = get_reports_dir() / suggested_name
    else:
        report_path = Path(output_path).expanduser()
        if report_path.suffix.lower() != ".pdf":
            report_path = report_path.with_suffix(".pdf")

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_name = report_path.name
    report_path = report_path.resolve()

    # Create PDF document
    pdf = SimpleDocTemplate(
        str(report_path),
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontSize=17,
        textColor=colors.darkblue,
        alignment=1,
        spaceAfter=10
    )

    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        textColor=colors.darkblue,
        spaceBefore=12,
        spaceAfter=8
    )

    normal_style = styles["BodyText"]

    # Build report content
    content = []

    # Report heading
    content.append(
        Paragraph(
            "DIGITAL FORENSIC INVESTIGATION REPORT",
            title_style
        )
    )

    content.append(
        Paragraph(
            "Digital Evidence Integrity & Verification System",
            normal_style
        )
    )

    content.append(Spacer(1, 15))

    # Report information
    content.append(
        Paragraph("1. REPORT INFORMATION", heading_style)
    )

    report_data = [
        ["Report ID", f"DEIVS-{evidence_id}-{report_time}"],
        ["Generated On", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        ["Evidence ID", str(record[0])]
    ]

    report_table = Table(report_data, colWidths=[45 * mm, 110 * mm])

    report_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP")
    ]))

    content.append(report_table)

    # Evidence details
    content.append(
        Paragraph("2. EVIDENCE DETAILS", heading_style)
    )

    evidence_data = [
        ["File Name", record[1]],
        ["File Location", record[2]],
        ["File Size", f"{record[3]} bytes"],
        ["Registration Date", record[5]]
    ]

    safe_evidence_data = [
        [Paragraph(escape(str(k)), normal_style),
         Paragraph(escape(str(v)), normal_style)]
        for k, v in evidence_data
    ]

    evidence_table = Table(
        safe_evidence_data,
        colWidths=[45 * mm, 110 * mm]
    )

    evidence_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP")
    ]))

    content.append(evidence_table)

    # Original hash
    content.append(
        Paragraph("3. SHA-256 HASH INFORMATION", heading_style)
    )

    content.append(
        Paragraph(
            "<b>Original SHA-256 Hash:</b><br/>"
            + escape(str(record[4])),
            normal_style
        )
    )

    content.append(Spacer(1, 12))

    # Verification details
    content.append(
        Paragraph("4. VERIFICATION DETAILS", heading_style)
    )

    if latest_verification:

        verification_id = latest_verification[0]
        current_hash = latest_verification[2]
        status = latest_verification[3]
        verification_date = latest_verification[4]

        verification_data = [
            ["Verification ID", str(verification_id)],
            ["Current SHA-256 Hash", str(current_hash or "Not available")],
            ["Verification Status", str(status)],
            ["Verification Date", str(verification_date)]
        ]

    else:

        verification_data = [
            ["Verification Status", "Not verified yet"]
        ]

    safe_verification_data = [
        [Paragraph(escape(str(k)), normal_style),
         Paragraph(escape(str(v)), normal_style)]
        for k, v in verification_data
    ]

    verification_table = Table(
        safe_verification_data,
        colWidths=[45 * mm, 110 * mm]
    )

    verification_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP")
    ]))

    content.append(verification_table)

    # Verification history
    content.append(
        Paragraph("5. VERIFICATION HISTORY", heading_style)
    )

    if history:

        history_data = [
            ["ID", "Status", "Date"]
        ]

        for item in history:

            history_data.append([
                str(item[0]),
                str(item[3]),
                str(item[4])
            ])

        history_table = Table(
            history_data,
            colWidths=[20 * mm, 40 * mm, 95 * mm]
        )

        history_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("PADDING", (0, 0), (-1, -1), 7)
        ]))

        content.append(history_table)

    else:

        content.append(
            Paragraph(
                "No verification history available.",
                normal_style
            )
        )

    # Disclaimer
    content.append(Spacer(1, 25))

    content.append(
        Paragraph(
            "<b>Note:</b> This report is generated automatically "
            "by DEIVS. It records the evidence details and "
            "verification results available in the local database. "
            "It is not an independent certification of forensic "
            "authenticity or chain of custody.",
            normal_style
        )
    )

    # Generate PDF
    pdf.build(content)

    print("\n===================================")
    print("INVESTIGATION REPORT GENERATED!")
    print("===================================")
    print("Evidence ID:", evidence_id)
    print("Report Name:", report_name)
    print("Saved Location:", report_path)
    print("===================================")

    return str(report_path)


# ------------------------------------------
# TEST REPORT GENERATOR
# ------------------------------------------

if __name__ == "__main__":

    print("\n===== DEIVS REPORT GENERATOR =====")

    try:

        evidence_id = int(input("Enter Evidence ID: "))

        generate_report(evidence_id)

    except ValueError:

        print("Please enter a valid Evidence ID!")
