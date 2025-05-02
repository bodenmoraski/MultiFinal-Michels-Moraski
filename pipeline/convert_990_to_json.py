
#!/usr/bin/env python3
"""
convert_990_to_json.py

A lightweight utility that converts a single IRS Form 990 PDF into a JSON
dictionary matching the field structure demonstrated in `episcopal_academy_metrics.json`.

Dependencies:
    pip install pymupdf==1.22.5
Usage:
    python convert_990_to_json.py /path/to/form990.pdf /path/to/output.json
"""

import sys
import json
import re
from datetime import datetime
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError as e:
    sys.exit(
        "PyMuPDF not found. Install it with: pip install pymupdf"
    )

NUM_PATTERN = re.compile(r"([-]?[\d,.]+)")

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _to_number(txt: str):
    """Convert a captured string with commas into int. Returns None if blank."""
    if txt is None:
        return None
    cleaned = txt.replace(",", "").strip()
    return int(cleaned) if cleaned not in {"", "-"} else None


def _search(pattern: str, text: str):
    """Utility for one-line numeric extraction."""
    match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
    return _to_number(match.group(1)) if match else None


# --------------------------------------------------------------------------- #
# Core extraction
# --------------------------------------------------------------------------- #

def parse_form_990(pdf_path: Path):
    doc = fitz.open(pdf_path)
    full_text = "\n".join(page.get_text() for page in doc)
    # Organization name & mission (quick ‑ may be refined)
    org_match = re.search(r"^\s*([A-Z][A-Z\s&',.-]+)\s*Name of organization", full_text, re.MULTILINE)
    mission_match = re.search(r"mission['’]s?[^:]*:[\s\n]*(.+?)\n", full_text, re.IGNORECASE)
    org_name = org_match.group(1).title().strip() if org_match else None
    mission = mission_match.group(1).strip().rstrip(".") if mission_match else None

    # Fiscal year (first line of Part I)
    fy_match = re.search(
        r"for the (\d{4}) calendar year, or tax year beginning (\d{2})-(\d{2})-(\d{4})[ ,]+and ending (\d{2})-(\d{2})-(\d{4})",
        full_text,
    )
    if fy_match:
        fy_start = f"{fy_match.group(4)}-{fy_match.group(2)}-{fy_match.group(3)}"
        fy_end = f"{fy_match.group(7)}-{fy_match.group(5)}-{fy_match.group(6)}"
        fiscal_year = f"{fy_start} to {fy_end}"
    else:
        fiscal_year = None

    data = {
        "organization_name": org_name,
        "fiscal_year": fiscal_year,
        "mission": mission,
        "website": _search(r"Website:\s*([\w.:-]+)", full_text),
        "gross_receipts": _search(r"Gross\s+receipts\s*\$?\s*([\d,]+)", full_text),
        "total_revenue": _search(r"Total\s+revenue[^\n]*\n[^\d-]*([\d,]+)", full_text),
        "total_expenses": _search(r"Total\s+expenses[^\n]*\n[^\d-]*([\d,]+)", full_text),
        "revenue_less_expenses": _search(r"Revenue\s+less\s+expenses[^\n]*\n[^\d-]*([\d,()-]+)", full_text),
        "contributions_and_grants": _search(r"Contributions\s+and\s+grants[^\n]*\n[^\d-]*([\d,]+)", full_text),
        "program_service_revenue": _search(r"Program\s+service\s+revenue[^\n]*\n[^\d-]*([\d,]+)", full_text),
        "investment_income": _search(r"Investment\s+income[^\n]*\n[^\d-]*([\d,]+)", full_text),
        "other_revenue": _search(r"Other\s+revenue[^\n]*\n[^\d-]*([-\d,]+)", full_text),
        "grants_and_similar_amounts_paid": _search(r"Grants\s+and\s+similar\s+amounts\s+paid[^\n]*\n[^\d-]*([\d,]+)", full_text),
        "salaries_and_employee_benefits": _search(r"Salaries.*?employee\s+benefits[^\n]*\n[^\d-]*([\d,]+)", full_text),
        "other_expenses": _search(r"Other\s+expenses[^\n]*\n[^\d-]*([\d,]+)", full_text),
        "fundraising_expenses": _search(r"fundraising\s+expenses[^\n]*\n[^\d-]*([\d,]+)", full_text),
        "total_assets_beginning": _search(r"Total\s+assets[^\n]*\n[^\d-]*([\d,]+)\s+\n+[^\n]*End", full_text),
        "total_assets_end": _search(r"Total\s+assets[^\n]*End[^\d-]*([\d,]+)", full_text),
        "total_liabilities_beginning": _search(r"Total\s+liabilities[^\n]*\n[^\d-]*([\d,]+)\s+\n+[^\n]*End", full_text),
        "total_liabilities_end": _search(r"Total\s+liabilities[^\n]*End[^\d-]*([\d,]+)", full_text),
        "net_assets_beginning": _search(r"Net\s+assets[^\n]*\n[^\d-]*([\d,]+)\s+\n+[^\n]*End", full_text),
        "net_assets_end": _search(r"Net\s+assets[^\n]*End[^\d-]*([\d,]+)", full_text),
        "number_of_employees": _search(r"individuals\s+employed[^\d]*([\d,]+)", full_text),
        "number_of_volunteers": _search(r"volunteers[^\d]*([\d,]+)", full_text),
        # Placeholders – refinements welcome
        "largest_program_expenses": {},
        "unrelated_business_income": _search(r"Total\s+unrelated\s+business\s+revenue[^\d]*([\d,]+)", full_text),
        "net_unrelated_business_income": _search(r"Net\s+unrelated\s+business\s+taxable\s+income[^\d]*([\d,]+)", full_text),
        "investment_in_securities": bool(re.search(r"investments—other\s+securities", full_text, re.IGNORECASE)),
        "land_buildings_and_equipment": bool(re.search(r"amount\s+for\s+land,\s+buildings,\s+and\s+equipment", full_text, re.IGNORECASE)),
        "policies": {
            "conflict_of_interest_policy": None,
            "whistleblower_policy": None,
            "document_retention_policy": None,
            "compensation_review_process": None
        },
        "audited_financials": bool(re.search(r"independent\s+audited\s+financial\s+statements", full_text, re.IGNORECASE)),
        "top_individual_salaries": {},
        "foreign_grants": None,
        "domestic_grants": None,
        # Ratios – to be populated downstream
        "program_expense_ratio": None,
        "fundraising_efficiency": None,
    }
    return data

# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: python convert_990_to_json.py input.pdf output.json")

    pdf_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])

    if not pdf_path.exists():
        sys.exit(f"Input file {pdf_path} does not exist.")

    data = parse_form_990(pdf_path)

    with open(out_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"✅ JSON saved to {out_path}")


if __name__ == "__main__":
    main()
