import openai
from dotenv import load_dotenv
import os

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")

OPENAI_MODEL = "gpt-4o-mini"  # Stelle sicher, dass dieses Modell verfügbar ist

TOPIC = "climat change"

def sentiment_analysis(input_text, TOPIC):
    """
    Sentiment analysis of text from politicians of specific topic. Output is "positiv", "negativ", "neutral".
    """
    openai.api_key = openai_key
    output = ""

    prompt = f"Read the following article by a politician and analyze the politician's stance toward {TOPIC}. Return only one word that describes the stance: either 'positive', 'negative', or 'neutral'. The output should be a single word only: positive, negative, or neutral."

    try:
        response = openai.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        prompt
                    )
                },
                {
                    "role": "user",
                    "content": input_text
                }
            ]
        )
        output = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"\nError during processing: {e}")

    return output