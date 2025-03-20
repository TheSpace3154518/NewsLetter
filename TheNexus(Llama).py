from openai import OpenAI
import os

# Initialize OpenRouter API client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("TOKEN"),  # Replace with your actual API key
)

def summarize_news(news_articles):
    prompt = "\n\n".join(news_articles)  # Merge articles with spacing
    sys_prompt = (
        "You are an advanced AI trained to generate **clear, concise, and high-quality summaries** while preserving key information. Your task is to extract the **most relevant details** from the given text and present them in a structured and logical manner.  \n\n"
        "🔹 **Key Instructions**:  \n"
        "1️⃣ **Focus on Facts**: Retain only the most **important information**, discarding trivial details, repetitive phrases, or unnecessary introductions.  \n"
        "2️⃣ **Be Concise & Precise**: Express the core message in the fewest words possible **without losing meaning**.  \n"
        "3️⃣ **Avoid Noise**: Ignore irrelevant details, filler content, and non-essential context (e.g., greetings, unrelated topics, advertisements).  \n"
        "4️⃣ **Maintain Objectivity**: Summarize **without bias**, avoiding opinions or assumptions not present in the original text.  \n"
        "5️⃣ **Use Structured Output**: Provide a **single coherent paragraph** for short summaries or **bulleted key points** for longer texts.  \n\n"
        "🔹 **Example Formatting**:  \n"
        "✔️ **Single-Paragraph Summary (for short texts)**  \n"
        "✔️ **Bullet-Point Summary (for long texts, reports, or complex topics)**  \n\n"
        "📌 **Your output should be a refined, professional summary that captures all essential points in a digestible format.**  \n"
    )

    try:
        completion = client.chat.completions.create(
            model="cognitivecomputations/dolphin3.0-r1-mistral-24b:free",
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )

        if not hasattr(completion, 'choices') or not completion.choices:
            return "Error: No valid response received from the API"

        summary = completion.choices[0].message.content

        # Remove the first line if it contains unwanted phrases
        summary_lines = summary.split("\n")
        if len(summary_lines) > 0 and ("Sure," in summary_lines[0] or "summary" in summary_lines[0].lower()):
            summary = "\n".join(summary_lines[0:])  # Remove only the first line

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