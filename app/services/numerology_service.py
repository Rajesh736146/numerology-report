"""Service functions for calculating core numerology numbers."""

from ..utils.helper import reduce_number, parse_dob
from ..constants.chaldean_chart import CHALDEAN_MAP


def calculate_moolank(dob: str) -> int:
    """
    Moolank (Psychic / Birth Number): single-digit reduction of the birth day.
    e.g. born on 29 → 2+9 = 11 → 1+1 = 2
    """
    dt = parse_dob(dob)
    return reduce_number(dt.day)


def calculate_bhagyank(dob: str) -> int:
    """
    Bhagyank (Destiny / Life Path Number): single-digit reduction of the full DOB.
    e.g. 15/08/1990 → 1+5+0+8+1+9+9+0 = 33 → 3+3 = 6
    """
    digits = [int(ch) for ch in dob if ch.isdigit()]
    return reduce_number(sum(digits))


def calculate_namank(full_name: str) -> int:
    """
    Namank (Name Number): Chaldean value of the full name reduced to a single digit.
    """
    total = sum(
        CHALDEAN_MAP.get(ch.upper(), 0)
        for ch in full_name
        if ch.isalpha()
    )
    return reduce_number(total)


def calculate_kua(dob: str, gender: str) -> int:
    """
    Kua Number (Feng Shui / Lo Shu): derived from birth year and gender.
    gender: 'M' for male, 'F' for female.
    """
    dt = parse_dob(dob)
    year_sum = reduce_number(sum(int(d) for d in str(dt.year)))

    if gender.upper() == "M":
        kua = reduce_number(10 - year_sum)
    else:
        kua = reduce_number(year_sum + 5)

    return kua if kua != 0 else 9
