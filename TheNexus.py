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
def summarize_news(news_text, language, model_name):
    """
    Summarizes the given news text into a single, concise paragraph.
    Returns the summary wrapped in the required HTML format.
    """


    system_prompt = f"""
    You are an elite tech journalist specializing in AI news synthesis. Transform complex information into engaging, concise articles in {language} that maintain clarity and impact while adding humor.

    ### CORE REQUIREMENTS:
    2. **OBJECTIVE REPORTING** - Present facts neutrally without bias
    3. **ENGAGING STYLE** - Use punchy sentences, casual tone, and appropriate humor just like a friend would
    4. **RESPECT THE MARKDOWN** - Change only the text but keep the markodwn that uses link for external sources
    6. **NO PLAGIARISM** - Ensure originality, avoid copying from the sources


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
    user_prompt = ""
    # Add each news item to the prompt
    for i, (post, source, link) in enumerate(news_text):
        user_prompt += f"""
        Post {i}:
            Link: {link}
            Source: {source}
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
        return f"❌ Error occurred: {str(e)}"

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
