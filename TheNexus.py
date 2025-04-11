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

    #1. **AI FOCUS ONLY** - If input isn't AI-related, generate an article about a current AI technique instead
def summarize_news(news_text, language):
    """
    Summarizes the given news text into a single, concise paragraph.
    Returns the summary wrapped in the required HTML format.
    """


    system_prompt = """
    You are an elite tech journalist specializing in AI news synthesis. Transform complex information into engaging, concise articles that maintain clarity and impact while adding humor.

    ### CORE REQUIREMENTS:
    2. **OBJECTIVE REPORTING** - Present facts neutrally without bias
    3. **ENGAGING STYLE** - Use punchy sentences, casual tone, and appropriate humor just like a friend would
    4. **RESPECT THE MARKDOWN** - Change only the text but keep the markodwn that uses link for external sources
    5. **OUTPUT LANGUAGE** - Generate the article in {language}

    ### WRITING GUIDELINES:
    - Maintain a cohesive narrative structure with clear flow
    - Include all key facts while eliminating unnecessary details
    - Use light sarcasm, pop-culture references where appropriate
    - Avoid technical jargon unless necessary, explain when used
    - Create compelling headlines that accurately reflect content
    - Adapt humor and cultural references to be appropriate for the target language

    ### OUTPUT FORMAT:
    <p>$Summarized Post here$ from [Post's Source](Post's Link)</p>
    """

    # Add each news item to the prompt
    for i, (post, source, link) in enumerate(news_text):
        system_prompt += f"""
        Post {i}: 
            Link: {link}
            Source: {source}
            Content: {post}
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
news = []
with open("TGT.txt","r") as f:
    news.append((f.read(), "Al Jazeera", "https://google.com"))

summary = summarize_news(news, "Moroccan Dialect")
print(summary)





# * kOLCHI FDE9A W7DA
# * KAYDE77EK
# * Api

