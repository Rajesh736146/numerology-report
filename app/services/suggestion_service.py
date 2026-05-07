"""Name suggestion service — generates and ranks auspicious name variations."""

from ..constants.mutation_rules import CHAR_SUBSTITUTIONS, SUFFIX_SWAPS
from ..constants.compounds import GOOD_COMPOUNDS
from ..services.chaldean_service import calculate_chaldean
from ..services.scoring_service import score_suggestion, rank_suggestions

# Names shorter than this after mutation are discarded
_MIN_NAME_LENGTH = 3


def _is_natural(name: str) -> bool:
    """
    Basic sanity check — reject names that look unnatural:
    - Too short
    - More than 3 consecutive consonants
    - More than 3 consecutive identical characters
    """
    if len(name) < _MIN_NAME_LENGTH:
        return False

    consonants = set("bcdfghjklmnpqrstvwxyz")
    run = 0
    prev = ""
    repeat = 0

    for ch in name.lower():
        if not ch.isalpha():
            continue
        run = run + 1 if ch in consonants else 0
        repeat = repeat + 1 if ch == prev else 1
        if run > 3 or repeat > 2:
            return False
        prev = ch

    return True


def _char_variations(name: str) -> set[str]:
    """Substitute individual characters with natural alternates."""
    results: set[str] = set()
    for i, ch in enumerate(name):
        alts = CHAR_SUBSTITUTIONS.get(ch.lower(), [])
        for alt in alts:
            variant = name[:i] + alt + name[i + 1:]
            if _is_natural(variant):
                results.add(variant)
    return results


def _suffix_variations(name: str) -> set[str]:
    """Swap the ending of a name with common natural alternatives."""
    results: set[str] = set()
    lower = name.lower()
    for ending, replacements in SUFFIX_SWAPS.items():
        if lower.endswith(ending):
            base = name[: len(name) - len(ending)]
            for rep in replacements:
                variant = base + rep
                if _is_natural(variant):
                    results.add(variant)
    return results


def generate_variations(name: str) -> list[str]:
    """
    Generate natural-sounding spelling variations of a first name.
    Combines character-level substitutions and suffix swaps.
    The original name is always included.
    """
    variations: set[str] = {name}
    variations |= _char_variations(name)
    variations |= _suffix_variations(name)
    return list(variations)


def suggest_names(
    first_name: str,
    surname: str,
    moolank: int = 0,
    bhagyank: int = 0,
    namank: int = 0,
) -> list[dict]:
    """
    Generate and rank auspicious name suggestions for a given first name + surname.

    Only names whose full Chaldean compound falls in GOOD_COMPOUNDS are returned.
    Results are sorted by compatibility score (descending), capped at 20.
    """
    suggestions: list[dict] = []
    seen: set[str] = set()

    for var in generate_variations(first_name):
        full_name = f"{var} {surname}"
        if full_name in seen:
            continue
        seen.add(full_name)

        calc = calculate_chaldean(full_name)
        compound = calc["compound"]
        final = calc["final"]

        if compound not in GOOD_COMPOUNDS:
            continue

        suggestions.append({
            "first_name": var,
            "full_name": full_name,
            "compound": compound,
            "final": final,
            "meaning": GOOD_COMPOUNDS[compound],
            "score": score_suggestion(
                compound=compound,
                final=final,
                moolank=moolank,
                bhagyank=bhagyank,
                namank=namank,
            ),
        })

    return rank_suggestions(suggestions)[:20]
