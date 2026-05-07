"""
Name mutation rules for generating natural-sounding spelling variations.

Rules are intentionally conservative — every substitution should produce
a name that looks plausible and pronounceable in Indian/English naming conventions.
"""

# Vowel elongation and common alternate spellings (applied per character position)
CHAR_SUBSTITUTIONS: dict[str, list[str]] = {
    "a": ["aa", "ah"],
    "e": ["ee", "i"],
    "i": ["ee", "y"],
    "o": ["oh", "oo"],
    "u": ["oo", "ou"],
    "k": ["c", "ck"],
    "s": ["sh", "z"],
    "v": ["w"],
    "w": ["v"],
    "n": ["nn"],
    "r": ["rr"],
    "t": ["th"],
    "j": ["dj"],
    "c": ["k", "ck"],
    "f": ["ph"],
    "y": ["ie", "i"],
    "z": ["s"],
    "x": ["ks"],
}

# Suffix swaps — only applied to the LAST character(s) of a name
# Key: ending the name currently has, Value: alternatives to try
SUFFIX_SWAPS: dict[str, list[str]] = {
    "a":   ["aa", "ah", "ia"],
    "i":   ["ee", "y", "ie"],
    "u":   ["oo", "ou"],
    "an":  ["aan", "en", "in"],
    "in":  ["een", "yn"],
    "on":  ["oon", "an"],
    "ul":  ["ool", "al"],
    "al":  ["aal", "el"],
    "ar":  ["aar", "er"],
    "it":  ["ith", "eet"],
    "at":  ["ath", "aat"],
    "ay":  ["ai", "aye"],
    "ey":  ["ay", "ee"],
    "sh":  ["ssh"],
    "raj": ["raaj", "raje"],
    "ram": ["raam"],
    "dev": ["deev", "deva"],
    "kumar": ["kumaar", "kumarr"],
}

# Legacy alias for backward compatibility
MUTATION_RULES: dict[str, list[str]] = CHAR_SUBSTITUTIONS
