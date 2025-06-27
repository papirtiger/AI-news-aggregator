import json
import logging
import os

import openai


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

SYSTEM_PROMPT = (
    "Du er en assistent, der udvælger de fem vigtigste historier i teksten. "
    "Målgruppen er HR-, kommunikations- og marketingchefer. "
    "Svar udelukkende med et JSON-array, hvor hvert element har nøglerne"
    " 'overskrift', 'link' og 'resume'."
)


def load_news(path: str) -> str:
    """Load the news update file."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def get_top_stories(content: str) -> list:
    """Send content to OpenAI and return parsed JSON."""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": content},
        ],
        temperature=0.2,
    )
    message = response["choices"][0]["message"]["content"].strip()
    try:
        return json.loads(message)
    except json.JSONDecodeError:
        logging.error("Modtaget svar er ikke gyldigt JSON")
        raise


def main():
    content = load_news("eb_news_updates.txt")
    stories = get_top_stories(content)
    print(json.dumps(stories, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
