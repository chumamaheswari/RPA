import os
import json
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def generate_flashcards(notes: str) -> list[dict]:
    prompt = f"""You are a flashcard generator. Given the following notes, generate between 5 and 30 concise flashcards.

Rules:
- Each flashcard tests exactly ONE concept
- Front (question): under 20 words
- Back (answer): under 30 words
- Do not repeat the question phrasing in the answer
- Assign a difficulty: "easy", "medium", or "hard"

Return ONLY a valid JSON array with no extra text. Format:
[
  {{"front": "question here", "back": "answer here", "difficulty": "easy"}},
  ...
]

Notes:
{notes}"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()

    # Strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    cards = json.loads(raw)

    # Validate and sanitize each card
    result = []
    for i, card in enumerate(cards):
        if "front" in card and "back" in card:
            result.append({
                "id": i + 1,
                "front": str(card["front"]).strip(),
                "back": str(card["back"]).strip(),
                "difficulty": card.get("difficulty", "medium"),
            })

    return result
