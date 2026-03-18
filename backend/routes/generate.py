from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator
from claude import generate_flashcards

router = APIRouter()


class GenerateRequest(BaseModel):
    notes: str

    @field_validator("notes")
    @classmethod
    def notes_must_be_valid(cls, v):
        v = v.strip()
        if len(v) < 50:
            raise ValueError("Notes must be at least 50 characters.")
        if len(v) > 10000:
            raise ValueError("Notes must be under 10,000 characters.")
        return v


@router.post("/generate")
def generate(request: GenerateRequest):
    try:
        cards = generate_flashcards(request.notes)
        return {"cards": cards, "count": len(cards)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
