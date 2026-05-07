"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.numerology import router

tags_metadata = [
    {
        "name": "Numerology",
        "description": (
            "Generate a full numerology report from a name, date of birth, and gender. "
            "Includes Moolank, Bhagyank, Namank, Kua number, Chaldean analysis, "
            "Lo Shu Grid, and ranked auspicious name suggestions."
        ),
    },
    {
        "name": "Health",
        "description": "Service health check.",
    },
]

app = FastAPI(
    title="Numerology AI",
    description=(
        "## Numerology AI API\n\n"
        "A Chaldean numerology engine that analyses names and dates of birth to produce:\n\n"
        "- **Moolank** — Psychic / Birth number\n"
        "- **Bhagyank** — Destiny / Life Path number\n"
        "- **Namank** — Current name number\n"
        "- **Kua** — Feng Shui / Lo Shu personal number\n"
        "- **Chaldean analysis** — compound value and per-letter breakdown\n"
        "- **Lo Shu Grid** — 3×3 magic square with plane and missing-digit analysis\n"
        "- **Name suggestions** — auspicious spelling variations ranked by compatibility\n\n"
        "Send a single `POST /numerology/report` request to get the full report."
    ),
    version="2.0.0",
    openapi_tags=tags_metadata,
    contact={
        "name": "Numerology AI",
    },
    license_info={
        "name": "MIT",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/", tags=["Health"])
def health_check():
    """API health check."""
    return {"status": "ok", "service": "Numerology AI"}
