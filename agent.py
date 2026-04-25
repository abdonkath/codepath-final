import anthropic
import json
from knowledge_base import retrieve

client = anthropic.Anthropic()


def suggest_tasks(pet_name: str, species: str, breed: str, age: int) -> list[dict]:
    care_guide = retrieve(species, breed)

    prompt = f"""You are a pet care assistant. Based on the care guide below, suggest a starter task list for a new pet.

Pet details:
- Name: {pet_name}
- Species: {species}
- Breed: {breed if breed else "not specified"}
- Age: {age} years old

Care guide:
{care_guide}

Return ONLY a JSON array of 4-6 tasks. Each task must have:
- "name": short task name (string)
- "category": one of "Exercise", "Grooming", "Health", "Feeding", "Training", "Other"
- "duration_minutes": estimated time in minutes (integer)
- "priority": 1-5, where 5 is most urgent (integer)
- "time": suggested time in "HH:MM" 24-hour format (string)
- "recurring": true if this should repeat regularly (boolean)
- "interval_days": how often it recurs in days, e.g. 1=daily, 7=weekly (integer)

Return only the JSON array. No explanation, no markdown fences."""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    return json.loads(raw.strip())