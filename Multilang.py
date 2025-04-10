from openai import OpenAI


def MultiLanguage(news_text, language):
    system_prompt = f"""
    You are a helpful translation assistant. You will be given a news article and your task is to translate it into the specified language {language}.
    Please ensure that the translation is accurate and maintains the original meaning of the text."""
    try:
        completion = client.chat.completions.create(
            model="google/gemini-2.5-pro-exp-03-25:free",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": news_text},
            ],
            max_tokens=500
        )

        if not hasattr(completion, 'choices') or not completion.choices:
            return "❌ Error: No valid response received from the API"

        summary = completion.choices[0].message.content.strip()

        # Ensure proper HTML wrapping
        return f"{summary}"

    except Exception as e:
        return f"❌ Error occurred: {str(e)}"
    

# Example usage
if __name__ == "__main__":
    news_text = "This is a sample news article."
    language = "Spanish"
    translated_text = MultiLanguage(news_text, language)
    print(translated_text)