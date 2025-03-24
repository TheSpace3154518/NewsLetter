from openai import OpenAI
import os

# Initialize OpenRouter API client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("TOKEN"),  # Replace with your actual API key
)

TGF_OUTPUT = """Syria’s President al-Sharaa calls for ‘peace, calm’ amid brutal clashes
Violence in Latakia, Tartous leaves hundreds dead as Syria faces deepening divides amid escalating conflict.
Picture describing Syria's security forces deploy to Latakia for operations against former regime forces
Hundreds killed as Syria security forces battle al-Assad loyalists
Fighting has erupted at Syria’s Banias gas power plant, just hours after the country’s interim President Ahmed al-Sharaa urged for peace amid escalating communal violence that has killed hundreds of civilians in the coastal areas.
Syria’s state-run news agency SANA reported on Sunday that fighting broke out with security forces at the plant after an attack by “remnants of the former regime”.
Earlier on Sunday, al-Sharaa stated the need to “preserve national unity and domestic peace; we can live together” as newly appointed forces clash with fighters loyal to removed President Bashar al-Assad.
The fighting began after the pro-Assad fighters coordinated attacks on security forces on Thursday. The attacks spiralled into revenge killings as thousands of armed supporters of Syria’s new leadership went to the coastal areas to support the security forces.
According to the Syrian Observatory for Human Rights, a UK-based war monitor, at least 745 Alawite civilians have been killed in Latakia and Tartous since Thursday, as well as about 125 members of the government’s security forces.
In addition, 148 pro-Assad fighters were killed, the Observatory added, taking the overall death toll to 1,018.
Al Jazeera has been unable to independently verify those figures.
UN rights chief Volker Turk has called for an immediate halt to the violence in Syria.
“There must be prompt, transparent and impartial investigations into all the killings and other violations, and those responsible must be held to account, in line with international law norms and standards. Groups terrorising civilians must also be held accountable,” Turk said.
US Secretary of State Marco Rubio said in a statement on Sunday that “Syria’s interim authorities must hold the perpetrators of these massacres against Syria’s minority communities accountable”.
Picture describing Who controls what in Syria?
“Rest assured about Syria, this country has the characteristics for survival,” al-Sharaa said in a video at a mosque in Mazzah, Damascus. “What is currently happening in Syria is within the expected challenges.”
Al-Sharaa has said anyone targeting civilians would be held accountable.
Later on Sunday, SANA reported, quoting a source in the Ministry of Defence, that “intense clashes in the vicinity of the village of Betannita in the countryside of Tartous” were taking place.
“Many war criminals affiliated with the al-Assad regime and groups of armed remnants fled to the village,” the report added.
Colonel Hassan Abdul Ghani, spokesperson for the ministry, said that “the second phase of the military operation aimed at pursuing the remnants and officers of the defunct regime has begun in the countryside of Latakia and Tartous, after restoring security and stability in the main coastal cities”.
Reporting from the capital Damascus, Al Jazeera’s Resul Serdar said as the clashes have significantly decreased, the reality of what happened in the past four days is becoming more evident.
“The pictures coming out are indeed horrific. There is a high death toll, and the numbers are expected to increase in the coming hours and days because officials who have control of the area are still discovering [bodies]. As of now, it’s extremely difficult to clarify the exact number,” he said.
Serdar explained that the recent clashes are a stark reminder of how divided Syria is despite al-Sharaa’s earlier claims of ruling the country as one.
“Some of the unconfirmed list of the [new] cabinet are coming out and we’re seeing that there are Alawite members in the cabinet, Kurds, Turkmen, Arabs, Sunni, Shia, Muslims, Christians [which] is absolutely necessary for this country,” he added.
On Sunday, the optical cable linking Deraa and Damascus governorates was damaged which resulted in “the cessation of telecommunications and internet services in the governorates of Deraa and Sweida”, according to the Director of Deraa Telecom’s Branch.
Ahmad al-Hariri said in a press release that the incident was due to “repeated attacks on the telecommunications infrastructure, which led to the cutting of the vital optical cable connecting the two governorates to the main telecommunications centres”.
What threat does the surge in violence in Syria pose?
Attacks in Syria “clearly designed to make a splash”
Hundreds killed as Syria security forces battle al-Assad loyalists
"""  # Example data


def summarize_news(news_text):
    """
    Summarizes the given news text into a single, concise paragraph.
    Returns the summary wrapped in the required HTML format.
    """

    #

    system_prompt = """
    You are an elite journalist and expert in information synthesis. Your task is to transform extensive, complex information into a single article, that retains only the most crucial details while maintaining clarity and impact.

    ### Instructions:
    0. **Keep it Objectif: Avoid Bias** → Your article should be neutral and unbiased.
    1. **Keep It Informative & Objectif** → All key facts and events must be present but Objectively.
    2. **Make It Engaging** → Use **punchy sentences, a casual tone, and a sprinkle of humor** to keep the reader hooked.
    3. **Avoid Bureaucratic Jargon** → No lifeless, robotic language.
    4. **Spice It Up** → Feel free to use light sarcasm depending on the situation, pop-culture references, or playful phrasing.
    5. **Format Correctly** → Return the summary wrapped in this template:
    6. **Maintain a Strong Narrative** → Ensure the paragraph is **cohesive, structured, and impactful**.
    7. **Format the Output Correctly** → Return the summary wrapped in thi html template:
    Template:
    <p>[Your summarized text here]</p>

    """

    try:
        completion = client.chat.completions.create(
            model="google/gemma-3-27b-it:free",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": news_text}
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


def generate_news_html(title, category, content):
    """
    Fills the HTML template with the provided news details.
    """
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 20px;
                display: flex;
                justify-content: center;
            }}
            .container {{
                max-width: 800px;
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            }}
            h1 {{
                color: #333;
                text-align: center;
            }}
            h2 {{
                color: #555;
                text-align: center;
                font-size: 20px;
            }}
            p {{
                font-size: 18px;
                line-height: 1.6;
                color: #555;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{title}</h1>
            <h2>{category}</h2>
            <p>{content}</p>
        </div>
    </body>
    </html>
    """
    return html_template


# Example usage with AI-generated summary
title = input("What is the ttile of the news? ")
category = input("What is the category of the news? ")
summary = summarize_news(TGF_OUTPUT)
news_html = generate_news_html(title , category, summary)

# Save the generated email document
with open("news_email.html", "w", encoding="utf-8") as file:
    file.write(news_html)

print("HTML news email saved successfully!")

print(summary)
