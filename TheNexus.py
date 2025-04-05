from openai import OpenAI
import os
import datetime
import dotenv
# Initialize OpenRouter API client
dotenv.load_dotenv()
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("TOKEN"),
)


def summarize_news(news_text):
    """
    Summarizes the given news text into a single, concise paragraph.
    Returns the summary wrapped in the required HTML format.
    """

    #here the system prompt is defined, it will be used to generate the summary

    system_prompt = """
    You are an elite journalist and expert in information synthesis working in AI NEWS DEPARTEMENT. Your task is to transform extensive, complex information into a single article, that retains only the most crucial details while maintaining clarity and impact.

    ### Instructions:
    1. **Make it funny** → Your article should be funny, engaging, and informative.
    2. **ONLY AI NEWS** → Your article should be about AI NEWS, if the input isn't related to AI, generate an Article about a technique related to ai. 
    3. **Keep it Objectif: Avoid Bias** → Your article should be neutral and unbiased.
    4. **Keep It Informative & Objectif** → All key facts and events must be present but Objectively.
    5. **Make It Engaging** → Use **punchy sentences, a casual tone, and a sprinkle of humor** to keep the reader hooked.
    6. **Avoid Bureaucratic Jargon** → No lifeless, robotic language.
    7. **Spice It Up** → Feel free to use light sarcasm depending on the situation, pop-culture references, or playful phrasing.
    8. **Format Correctly** → Return the summary wrapped in this template:
    9. **Maintain a Strong Narrative** → Ensure the paragraph is **cohesive, structured, and impactful**.
    8. **Use HTML/CSS format to edit text** → use <br> for bold and <i> for italic... etc.
    10. **Format the Output Correctly** → Return the summary wrapped in thi html template and don't add anything else outside the template:
    Template:
    <p>[Your summarized text here]</p>

    """

    try:
        completion = client.chat.completions.create(
            model="google/gemma-3-27b-it:free",
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

# Function to generate a title for the article
def generate_title(Summary):
    prompt = """ Generate one catchy title without adding any other content for the following article:"""
    completion = client.chat.completions.create(
            model="google/gemma-3-27b-it:free",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": Summary},
            ],
            max_tokens=500
        )
    title = completion.choices[0].message.content.strip()
    return title

# Main execution

# for element in Test:
#     summary = summarize_news(element)
#     print(summary)





# * OLCHI FDE9A W7DA
# * KAYDE77EK
# * Api

