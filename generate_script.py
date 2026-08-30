import anthropic
from config import CLAUDE_MODEL, MAX_TOKENS, TARGET_LENGTH_MINUTES


def generate_briefing_script(articles):
    if not articles:
        return "No articles were found in the last 24 hours. Please check back tomorrow."

    articles_text = ""
    for i, article in enumerate(articles, 1):
        articles_text += f"\n{i}. [{article['source']}] {article['title']}\n"
        if article["summary"]:
            articles_text += f"   {article['summary']}\n"

    prompt = f"""You are Bri, a warm and knowledgeable AI news anchor who specializes in artificial intelligence.

Below are today's top AI headlines from the past 24 hours. Write a spoken-word radio script for a {TARGET_LENGTH_MINUTES}-minute morning briefing.

Requirements:
- Open with the single most important story of the day
- Group the remaining stories by theme (e.g. new models and research, business and funding, tools, policy)
- Write in a conversational, friendly tone as if speaking directly to the listener over their morning coffee
- No markdown, no bullet points, no headers — plain prose only, written to be read aloud
- Use natural spoken transitions between topics
- End with a warm, brief sign-off as Bri
- Aim for approximately {TARGET_LENGTH_MINUTES * 150} words

Today's articles:
{articles_text}

Write the full script now:"""

    client = anthropic.Anthropic()
    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}],
    )

    return message.content[0].text
