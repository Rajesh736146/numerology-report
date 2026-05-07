"""Chaldean numerology calculations for names."""

from ..constants.chaldean_chart import CHALDEAN_MAP
from ..utils.helper import reduce_number, reduce_to_compound


def calculate_chaldean(name: str) -> dict:
    """
    Calculate the Chaldean compound and final (single-digit) values for a name.

    Returns:
        dict with keys:
            - compound (int): raw Chaldean sum before final reduction
            - final (int): single-digit reduction of the compound
    """
    total = sum(
        CHALDEAN_MAP.get(ch.upper(), 0)
        for ch in name
        if ch.isalpha()
    )

    compound = reduce_to_compound(total)
    final = reduce_number(compound)

    return {
        "compound": compound,
        "final": final,
    }


def letter_values(name: str) -> dict[str, int]:
    """Return a mapping of each letter in the name to its Chaldean value."""
    return {
        ch: CHALDEAN_MAP.get(ch.upper(), 0)
        for ch in name
        if ch.isalpha()
    }
