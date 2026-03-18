from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from models import Deck, Card

router = APIRouter()


class CardIn(BaseModel):
    front: str
    back: str
    difficulty: str = "medium"


class DeckIn(BaseModel):
    name: str
    cards: list[CardIn]


@router.get("/decks")
def list_decks(db: Session = Depends(get_db)):
    decks = db.query(Deck).order_by(Deck.created_at.desc()).all()
    return [
        {"id": d.id, "name": d.name, "created_at": d.created_at, "card_count": len(d.cards)}
        for d in decks
    ]


@router.post("/decks", status_code=201)
def save_deck(payload: DeckIn, db: Session = Depends(get_db)):
    deck = Deck(name=payload.name)
    db.add(deck)
    db.flush()

    for c in payload.cards:
        db.add(Card(deck_id=deck.id, front=c.front, back=c.back, difficulty=c.difficulty))

    db.commit()
    db.refresh(deck)
    return {"id": deck.id, "name": deck.name, "card_count": len(payload.cards)}


@router.get("/decks/{deck_id}")
def get_deck(deck_id: int, db: Session = Depends(get_db)):
    deck = db.query(Deck).filter(Deck.id == deck_id).first()
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found.")
    return {
        "id": deck.id,
        "name": deck.name,
        "created_at": deck.created_at,
        "cards": [
            {"id": c.id, "front": c.front, "back": c.back, "difficulty": c.difficulty}
            for c in deck.cards
        ],
    }


@router.delete("/decks/{deck_id}", status_code=204)
def delete_deck(deck_id: int, db: Session = Depends(get_db)):
    deck = db.query(Deck).filter(Deck.id == deck_id).first()
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found.")
    db.delete(deck)
    db.commit()
