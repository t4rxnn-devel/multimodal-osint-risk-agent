
base = "/mnt/agents/output/osint-risk-analyst"

# Rewrite sec_parser with properly escaped backslashes for the file content
sec_parser_fixed2 = r'''"""
SEC EDGAR Parser

Extracts corporate hierarchy, risk factors, and supplier disclosures from
SEC filings (10-K, 10-Q, 8-K). Uses the SEC EDGAR Full-Text Search API
and CIK-based document retrieval.

Production Endpoints:
  - CIK Lookup: https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany
  - Full-Text Search: https://efts.sec.gov/LATEST/search-index
  - XBRL Viewer: https://www.sec.gov/cgi-bin/viewer
"""

from __future__ import annotations

import re
from datetime import datetime
from typing import Any

import requests


class SECParser:
    """
    Parser for SEC EDGAR filings.

    Handles CIK resolution, 10-K/10-Q text extraction, and structured
    risk-factor / subsidiary parsing via regex heuristics.
    """

    BASE_URL = "https://www.sec.gov"
    HEADERS = {
        "User-Agent": "OSINT-Risk-Analyst contact@example.com",
        "Accept": "application/json",
    }

    def __init__(self, rate_limit_delay: float = 0.1) -> None:
        self.rate_limit_delay = rate_limit_delay
        self._session = requests.Session()
        self._session.headers.update(self.HEADERS)

    def search_cik(self, company_name: str) -> str | None:
        """
        Resolve a company name to its SEC CIK identifier.

        Uses the SEC EDGAR company search endpoint.
        """
        url = f"{self.BASE_URL}/cgi-bin/browse-edgar"
        params = {
            "action": "getcompany",
            "company": company_name,
            "type": "10-K",
            "dateb": "",
            "owner": "include",
            "count": "1",
            "output": "json",
        }
        try:
            resp = self._session.get(url, params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            if data.get("hits", {}).get("hits"):
                return data["hits"]["hits"][0]["_source"]["ciks"][0]
        except Exception:
            pass
        return None

    def fetch_latest_10k(self, company_name: str) -> dict[str, Any] | None:
        """
        Fetch the most recent 10-K filing for a company.

        Returns structured data with risk factors and exhibit 21 references.
        """
        cik = self.search_cik(company_name)
        if not cik:
            return None

        # Normalize CIK to 10 digits
        cik_padded = cik.zfill(10)
        submissions_url = f"https://data.sec.gov/submissions/CIK{cik_padded}.json"

        try:
            resp = self._session.get(submissions_url, timeout=15)
            resp.raise_for_status()
            submissions = resp.json()
        except Exception:
            return None

        filings = submissions.get("filings", {}).get("recent", {})
        if not filings or not filings.get("accessionNumber"):
            return None

        # Get the most recent 10-K
        forms = filings.get("form", [])
        for idx, form in enumerate(forms):
            if form == "10-K":
                accession = filings["accessionNumber"][idx].replace("-", "")
                filing_date = filings["filingDate"][idx]
                primary_doc = filings.get("primaryDocument", [""])[idx]

                return {
                    "cik": cik,
                    "accession_number": filings["accessionNumber"][idx],
                    "filing_date": filing_date,
                    "primary_document": primary_doc,
                    "filing_url": (
                        f"{self.BASE_URL}/Archives/edgar/data/"
                        f"{int(cik)}/{accession}/{primary_doc}"
                    ),
                    "risk_factors": "[PARSING_NOT_IMPLEMENTED]",
                    "exhibit_21": "[PARSING_NOT_IMPLEMENTED]",
                }
        return None

    def parse_risk_factors(self, filing_text: str) -> list[str]:
        """
        Extract risk factor items from 10-K Item 1A.

        Uses regex heuristics to split on standard SEC section headers.
        """
        pattern = re.compile(
            r"Item\s+1A\.\s*Risk\s*Factors.*?"
            r"(Item\s+1B\.|Item\s+2\.|PART\s+II)",
            re.IGNORECASE | re.DOTALL,
        )
        match = pattern.search(filing_text)
        if not match:
            return []

        risk_section = match.group(0)
        # Split on bullet points or numbered headers
        risks = re.split(r"\n\s*\u2022\s*|\n\s*\d+\.\s*", risk_section)
        return [r.strip() for r in risks if len(r.strip()) > 20]

    def parse_exhibit_21_subsidiaries(self, exhibit_text: str) -> list[dict[str, str]]:
        """
        Extract subsidiary list from Exhibit 21.

        Returns list of dicts with keys: name, jurisdiction.
        """
        subsidiaries = []
        lines = exhibit_text.split("\n")
        for line in lines:
            # Heuristic: lines with " Inc.", " Ltd.", " Corp." followed by state/country
            match = re.match(r"^(.+?)\s+([A-Z]{2}|\w+)$", line.strip())
            if match:
                subsidiaries.append({
                    "name": match.group(1).strip(),
                    "jurisdiction": match.group(2).strip(),
                })
        return subsidiaries
'''

with open(f"{base}/src/osint_risk_analyst/tools/sec_parser.py", "w") as f:
    f.write(sec_parser_fixed2)

print("sec_parser.py fixed with raw string prefix.")
