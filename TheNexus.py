from openai import OpenAI
import os
# Initialize 
# OpenRouter API client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("TOKEN"),  # Replace with your actual API key
)

def summarize_news(news_articles):
    combined_text = "\n\n".join(news_articles)  # Merge articles with spacing
    prompt = (
        "Read the following news articles and generate a single, concise summary that includes only the key points:\n\n"
        f"{combined_text}\n\n"
        "Provide only the summary itself, without introductions or extra phrases."
    )

    try:
        completion = client.chat.completions.create(
            model="sophosympatheia/rogue-rose-103b-v0.2:free",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )

        if not hasattr(completion, 'choices') or not completion.choices:
            return "Error: No valid response received from the API"

        summary = completion.choices[0].message.content

        # Remove the first line if it contains unwanted phrases
        summary_lines = summary.split("\n")
        if len(summary_lines) > 1 and ("Sure," in summary_lines[0] or "summary" in summary_lines[0].lower()):
            summary = "\n".join(summary_lines[1:])  # Remove only the first line

        return summary.strip()  # Clean any leading/trailing whitespace

    except Exception as e:
        return f"Error occurred: {str(e)}"

# Example usage
news_list = [
    "Hello and welcome to today's news summary! We have several updates for you. Stock markets saw a sharp decline today due to global economic concerns...",
    "Before we get to the main news, let's remind our readers that tax season is coming up! Now, for today's headlines: The government announced new tax reforms affecting small businesses...",
    "In a groundbreaking discovery, scientists have found a new method to improve solar panel efficiency, which could revolutionize renewable energy. But first, let's thank our sponsors for making this report possible!",
    "Just a quick note before we continue: The following report is based on credible sources. Now, back to the main news...",
    "Breaking: The new economic report suggests inflation may rise further, impacting consumer goods prices.",
    "And that's a wrap for today's news! Stay tuned for more updates."
]

summary = summarize_news(news_list)
print("🔹 Summarized News:\n", summary)
