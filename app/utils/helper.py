"""Shared utility functions for numerology calculations."""

import re
from datetime import datetime


def reduce_number(num: int) -> int:
    """Reduce a number to a single digit (1–9) by summing its digits repeatedly."""
    while num > 9:
        num = sum(int(d) for d in str(num))
    return num


def reduce_to_compound(num: int) -> int:
    """Reduce a number until it is <= 52 (standard Chaldean compound range)."""
    while num > 52:
        num = sum(int(d) for d in str(num))
    return num


def parse_dob(dob: str) -> datetime:
    """
    Parse a date-of-birth string in DD/MM/YYYY or DD-MM-YYYY format.
    Raises ValueError for invalid formats.
    """
    for fmt in ("%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(dob, fmt)
        except ValueError:
            continue
    raise ValueError(f"Invalid date format '{dob}'. Expected DD/MM/YYYY or DD-MM-YYYY.")


def clean_name(name: str) -> str:
    """Strip non-alpha characters and normalise whitespace."""
    name = re.sub(r"[^a-zA-Z\s]", "", name)
    return " ".join(name.split())
