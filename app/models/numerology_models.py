"""Pydantic models for numerology API request and response validation."""

import re
from pydantic import BaseModel, field_validator, Field


class NumerologyRequest(BaseModel):
    """Request payload for generating a numerology report."""

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "full_name": "Rahul Sharma",
                    "dob": "15/08/1990",
                    "gender": "M",
                }
            ]
        }
    }

    full_name: str = Field(..., min_length=2, description="Full name (first + surname)")
    dob: str = Field(..., description="Date of birth in DD/MM/YYYY or DD-MM-YYYY format")
    gender: str = Field(..., description="Gender: 'M' or 'F'")

    @field_validator("dob")
    @classmethod
    def validate_dob(cls, v: str) -> str:
        pattern = r"^\d{2}[\/\-]\d{2}[\/\-]\d{4}$"
        if not re.match(pattern, v):
            raise ValueError("DOB must be in DD/MM/YYYY or DD-MM-YYYY format")
        return v

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, v: str) -> str:
        if v.upper() not in ("M", "F"):
            raise ValueError("Gender must be 'M' or 'F'")
        return v.upper()

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, v: str) -> str:
        parts = v.strip().split()
        if len(parts) < 2:
            raise ValueError("full_name must include at least a first name and a surname")
        return v.strip()


class NameSuggestion(BaseModel):
    """A single name suggestion with its numerological values."""

    first_name: str
    full_name: str
    compound: int
    final: int
    meaning: str
    score: int = Field(default=0, description="Compatibility score (higher is better)")


class LoShuGrid(BaseModel):
    """Lo Shu Grid analysis result."""

    grid: list[list[list[int]]]
    digit_counts: dict[int, int]
    missing_digits: list[int]
    missing_interpretations: dict[int, str]
    repeated_digits: list[int]
    complete_planes: dict[str, str]


class ChaldeanResponse(BaseModel):
    """Chaldean calculation result for a name."""

    name: str
    compound: int
    final: int
    meaning: str
    letter_values: dict[str, int]


class NumerologyResponse(BaseModel):
    """Full numerology report response."""

    moolank: int = Field(..., description="Birth / Psychic number")
    bhagyank: int = Field(..., description="Destiny / Life Path number")
    namank: int = Field(..., description="Current name number (Chaldean)")
    kua: int = Field(..., description="Kua number (Lo Shu / Feng Shui)")
    chaldean: ChaldeanResponse = Field(..., description="Chaldean analysis of the current name")
    loshu: LoShuGrid = Field(..., description="Lo Shu Grid analysis")
    suggestions: list[NameSuggestion] = Field(..., description="Ranked auspicious name suggestions")
