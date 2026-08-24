#!/usr/bin/env python3
"""Validate local Markdown links and the offline PDF inventory."""

from __future__ import annotations

from collections import Counter
from datetime import date
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
TREND_REPORT = ROOT / "TRENDING_2026.md"
MAX_REVIEW_AGE_DAYS = 120
LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\((?P<target><[^>]+>|[^)\s]+)")
REVIEW_DATE_PATTERN = re.compile(
    r"(?:reviewed on|Last reviewed:)\s*\*\*(\d{4}-\d{2}-\d{2})\*\*",
    re.IGNORECASE,
)


def markdown_files() -> list[Path]:
    return sorted(path for path in ROOT.rglob("*.md") if ".git" not in path.parts)


def link_targets(path: Path) -> list[str]:
    return [
        match.group("target").strip("<>")
        for match in LINK_PATTERN.finditer(path.read_text(encoding="utf-8"))
    ]


def validate_local_links(files: list[Path]) -> list[str]:
    errors: list[str] = []
    for source in files:
        for target in link_targets(source):
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith("#"):
                continue

            relative_target = unquote(parsed.path)
            if not relative_target:
                continue

            resolved = (source.parent / relative_target).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                errors.append(f"{source.relative_to(ROOT)}: link escapes repository: {target}")
                continue

            if not resolved.exists():
                errors.append(f"{source.relative_to(ROOT)}: missing local target: {target}")
    return errors


def validate_pdf_inventory() -> list[str]:
    errors: list[str] = []
    disk_pdfs = {
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "cheat_sheets").glob("*.pdf")
    }
    linked_pdfs = Counter(
        urlsplit(target).path
        for target in link_targets(README)
        if urlsplit(target).path.startswith("cheat_sheets/")
        and urlsplit(target).path.endswith(".pdf")
    )

    missing = sorted(disk_pdfs - linked_pdfs.keys())
    unknown = sorted(linked_pdfs.keys() - disk_pdfs)
    duplicates = sorted(path for path, count in linked_pdfs.items() if count != 1)

    if missing:
        errors.append(f"PDFs not linked from README.md: {', '.join(missing)}")
    if unknown:
        errors.append(f"README.md links unknown PDFs: {', '.join(unknown)}")
    if duplicates:
        errors.append(f"PDFs must be linked exactly once: {', '.join(duplicates)}")
    return errors


def review_date(path: Path) -> str | None:
    match = REVIEW_DATE_PATTERN.search(path.read_text(encoding="utf-8"))
    return match.group(1) if match else None


def validate_review_dates() -> list[str]:
    readme_date = review_date(README)
    trend_date = review_date(TREND_REPORT)
    if not readme_date or not trend_date:
        return ["README.md and TRENDING_2026.md must each contain a review date"]
    if readme_date != trend_date:
        return [
            "Review dates differ: "
            f"README.md={readme_date}, TRENDING_2026.md={trend_date}"
        ]
    try:
        reviewed = date.fromisoformat(readme_date)
    except ValueError:
        return [f"Invalid review date: {readme_date}"]
    age_days = (date.today() - reviewed).days
    if age_days < 0:
        return [f"Review date is in the future: {readme_date}"]
    if age_days > MAX_REVIEW_AGE_DAYS:
        return [
            f"Resource review is {age_days} days old; "
            f"maximum is {MAX_REVIEW_AGE_DAYS} days"
        ]
    return []


def main() -> int:
    files = markdown_files()
    errors = (
        validate_local_links(files)
        + validate_pdf_inventory()
        + validate_review_dates()
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    pdf_count = len(list((ROOT / "cheat_sheets").glob("*.pdf")))
    print(f"Validated {len(files)} Markdown files and {pdf_count} offline PDFs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
