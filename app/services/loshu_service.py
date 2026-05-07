"""Lo Shu Grid service — builds and analyses the 3×3 magic square from a DOB."""

from ..utils.helper import parse_dob

# Lo Shu grid positions (row, col) for digits 1–9
_GRID_POSITION: dict[int, tuple[int, int]] = {
    4: (0, 0), 9: (0, 1), 2: (0, 2),
    3: (1, 0), 5: (1, 1), 7: (1, 2),
    8: (2, 0), 1: (2, 1), 6: (2, 2),
}

# Planes and their associated traits
_PLANES: dict[str, dict] = {
    "thought":   {"digits": [4, 9, 2], "trait": "Mental / intellectual ability"},
    "will":      {"digits": [3, 5, 7], "trait": "Emotional / willpower"},
    "action":    {"digits": [8, 1, 6], "trait": "Practical / physical energy"},
    "silver":    {"digits": [4, 3, 8], "trait": "Determination and persistence"},
    "gold":      {"digits": [9, 5, 1], "trait": "Spiritual and material balance"},
    "copper":    {"digits": [2, 7, 6], "trait": "Compassion and creativity"},
    "diagonal1": {"digits": [4, 5, 6], "trait": "Frustration or fulfilment axis"},
    "diagonal2": {"digits": [2, 5, 8], "trait": "Sensitivity axis"},
}


def build_loshu_grid(dob: str) -> dict:
    """
    Build the Lo Shu Grid from a date of birth.

    Returns:
        dict with:
            - grid: 3×3 list of lists, each cell contains a list of digit occurrences
            - digit_counts: how many times each digit 1–9 appears in the DOB
            - missing_digits: digits absent from the DOB
            - repeated_digits: digits that appear more than once
            - planes: which planes are complete (all three digits present)
    """
    parse_dob(dob)  # validate format
    dob_digits = [int(ch) for ch in dob if ch.isdigit() and ch != "0"]

    # Count occurrences of each digit 1–9
    digit_counts: dict[int, int] = {d: 0 for d in range(1, 10)}
    for d in dob_digits:
        if d in digit_counts:
            digit_counts[d] += 1

    # Build 3×3 grid
    grid: list[list[list[int]]] = [[[] for _ in range(3)] for _ in range(3)]
    for digit, (row, col) in _GRID_POSITION.items():
        grid[row][col] = [digit] * digit_counts[digit]

    missing = [d for d, count in digit_counts.items() if count == 0]
    repeated = [d for d, count in digit_counts.items() if count > 1]

    # Check complete planes
    complete_planes = {
        name: info["trait"]
        for name, info in _PLANES.items()
        if all(digit_counts[d] > 0 for d in info["digits"])
    }

    return {
        "grid": grid,
        "digit_counts": digit_counts,
        "missing_digits": missing,
        "repeated_digits": repeated,
        "complete_planes": complete_planes,
    }


def loshu_interpretation(dob: str) -> dict:
    """
    Return a human-readable interpretation of the Lo Shu Grid.

    Includes strengths (complete planes), missing number meanings,
    and a summary of the grid balance.
    """
    data = build_loshu_grid(dob)

    _missing_meanings: dict[int, str] = {
        1: "Lack of confidence and self-expression",
        2: "Sensitivity and intuition may be underdeveloped",
        3: "Creativity and imagination need nurturing",
        4: "Practical organisation and discipline may be weak",
        5: "Difficulty adapting to change; emotional instability",
        6: "Home, family or creative vision may be neglected",
        7: "Spiritual depth and introspection may be lacking",
        8: "Material ambition and physical energy may be low",
        9: "Idealism and humanitarian concern may be absent",
    }

    missing_interpretations = {
        d: _missing_meanings[d]
        for d in data["missing_digits"]
    }

    return {
        "grid": data["grid"],
        "digit_counts": data["digit_counts"],
        "missing_digits": data["missing_digits"],
        "missing_interpretations": missing_interpretations,
        "repeated_digits": data["repeated_digits"],
        "complete_planes": data["complete_planes"],
    }
