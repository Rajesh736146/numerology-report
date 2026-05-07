"""Numerology API router."""

from fastapi import APIRouter, HTTPException

from ..models.numerology_models import (
    NumerologyRequest,
    NumerologyResponse,
)
from ..services.numerology_service import (
    calculate_moolank,
    calculate_bhagyank,
    calculate_namank,
    calculate_kua,
)
from ..services.suggestion_service import suggest_names
from ..services.chaldean_service import calculate_chaldean, letter_values
from ..services.loshu_service import loshu_interpretation
from ..constants.compounds import GOOD_COMPOUNDS, NEUTRAL_COMPOUNDS
from ..utils.helper import clean_name

router = APIRouter(prefix="/numerology", tags=["Numerology"])


@router.post(
    "/report",
    response_model=NumerologyResponse,
    summary="Generate full numerology report",
    response_description="Complete numerology report including core numbers, Chaldean analysis, Lo Shu Grid, and name suggestions",
)
def generate_report(request: NumerologyRequest):
    """
    Generate a complete numerology report in a single API call.

    **Input:** full name, date of birth, and gender.

    **Output includes:**
    - `moolank` — Psychic / Birth number (reduced birth day)
    - `bhagyank` — Destiny / Life Path number (reduced full DOB)
    - `namank` — Name number via Chaldean chart
    - `kua` — Kua / Feng Shui number derived from birth year and gender
    - `chaldean` — Compound value, final number, meaning, and per-letter values for the current name
    - `loshu` — Lo Shu 3×3 Grid with digit counts, missing digits, repeated digits, and complete planes
    - `suggestions` — Auspicious spelling variations of the first name ranked by compatibility score
    """
    try:
        names = clean_name(request.full_name).split()
        first_name = names[0]
        surname = " ".join(names[1:])

        moolank = calculate_moolank(request.dob)
        bhagyank = calculate_bhagyank(request.dob)
        namank = calculate_namank(request.full_name)
        kua = calculate_kua(request.dob, request.gender)
        loshu = loshu_interpretation(request.dob)

        chaldean = calculate_chaldean(request.full_name)
        compound = chaldean["compound"]
        chaldean_meaning = (
            GOOD_COMPOUNDS.get(compound)
            or NEUTRAL_COMPOUNDS.get(compound)
            or "No specific interpretation available"
        )

        suggestions = suggest_names(
            first_name=first_name,
            surname=surname,
            moolank=moolank,
            bhagyank=bhagyank,
            namank=namank,
        )

        return {
            "moolank": moolank,
            "bhagyank": bhagyank,
            "namank": namank,
            "kua": kua,
            "chaldean": {
                "name": request.full_name,
                "compound": compound,
                "final": chaldean["final"],
                "meaning": chaldean_meaning,
                "letter_values": letter_values(request.full_name),
            },
            "loshu": loshu,
            "suggestions": suggestions,
        }

    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
