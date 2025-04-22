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

def summarize_news(news_text, language, model_name):
    """
    Summarizes the given news text into a single, concise paragraph.
    Returns the summary wrapped in the required HTML format.
    """


    system_prompt = f"""
    You are an elite tech journalist specializing in AI news synthesis. Transform complex information into engaging, concise articles in {language} that maintain clarity and impact while adding humor.

    ### CORE REQUIREMENTS:
    1. **AI FOCUS ONLY** - If input isn't AI-related, ignore it
    2. **OBJECTIVE REPORTING** - Present facts neutrally without bias
    3. **ENGAGING STYLE** - Use punchy sentences, casual tone, and appropriate humor just like a friend would unless the events are tragic
    4. **RESPECT THE MARKDOWN** - use only markdown formatting
    5. **OUTPUT LANGUAGE** - Make sure the output is written in {language}
    6. **EXTERNAL SOURCES** - Mention the sources used in the article at the very end of the article with their links.
    7. **KEEP IT RESPECTFUL** - Maintain a respectful tone and avoid offensive language, humour or any cursing / bad words
    8. **News Letter Format** - for each piece of news, generate at least 300 words concerning that topic
    9. **MAINTAIN INTEGRITY** - make sure the news aren't missing any important details, maintain the integrity of the information provided.

    ### OUTPUT FORMAT:
    <p>Summarized Posts here</p>
    (all remaining html and posts)
    <ul>
        <li> [Post 1's source](Post 1's link) </li>
        <li> [Post 2's source](Post 2's link) </li>
        <li> [Post 3's source](Post 3's link) </li>
        ...
    </ul>
    """
    user_prompt = ""
    # Add each news item to the prompt
    for i, (post, source, link) in enumerate(news_text):
        user_prompt += f"""
        Post {i}:
            Post's Link: {link}
            Post's Source: {source}
            Content: {post}
        """
    try:
        completion = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=500
        )

        if not hasattr(completion, 'choices') or not completion.choices:
            return "❌ Error: No valid response received from the API"

        summary = completion.choices[0].message.content.strip()

        # Ensure proper HTML wrapping
        return f"{summary}"

    except Exception as e:
        return f"❌ Error occurred: {str(e)} \n {completion}"

# Function to generate a title for the article
def generate_title(Summary, language, model_name):
    prompt = f"""
    - Generate one catchy title in {language} without adding any other content for the following article.
    - Make sure the title follows this template :
        <strong>(title here)</strong>
    """
    completion = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": Summary},
            ],
            max_tokens=500
        )
    try :
        title = completion.choices[0].message.content.strip()
    except Exception as e:
        title = f"❌ Error occurred: {str(e)} \n {completion}"
    return title



# * kOLCHI FDE9A W7DA
# * KAYDE77EK
# * Api
