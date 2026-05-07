"""Scoring service — ranks name suggestions by numerological compatibility."""

from ..constants.compounds import GOOD_COMPOUNDS, NEUTRAL_COMPOUNDS


# Weight constants
_GOOD_COMPOUND_SCORE = 10
_NEUTRAL_COMPOUND_SCORE = 4
_MOOLANK_MATCH_BONUS = 3
_BHAGYANK_MATCH_BONUS = 3
_NAMANK_MATCH_BONUS = 2


def score_suggestion(
    compound: int,
    final: int,
    moolank: int,
    bhagyank: int,
    namank: int,
) -> int:
    """
    Score a name suggestion based on:
    - Whether its compound number is auspicious or neutral
    - Alignment of the final number with moolank, bhagyank, or namank

    Higher score = better numerological fit.
    """
    score = 0

    if compound in GOOD_COMPOUNDS:
        score += _GOOD_COMPOUND_SCORE
    elif compound in NEUTRAL_COMPOUNDS:
        score += _NEUTRAL_COMPOUND_SCORE

    if final == moolank:
        score += _MOOLANK_MATCH_BONUS
    if final == bhagyank:
        score += _BHAGYANK_MATCH_BONUS
    if final == namank:
        score += _NAMANK_MATCH_BONUS

    return score


def rank_suggestions(suggestions: list[dict]) -> list[dict]:
    """
    Sort a list of suggestion dicts (each containing a 'score' key)
    in descending order of score.
    """
    return sorted(suggestions, key=lambda s: s.get("score", 0), reverse=True)
