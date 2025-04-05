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

Test =[
    """Syria's President al-Sharaa calls for 'peace, calm' amid brutal clashes
    Violence in Latakia, Tartous leaves hundreds dead as Syria faces deepening divides amid escalating conflict.
    Picture describing Syria's security forces deploy to Latakia for operations against former regime forces
    Hundreds killed as Syria security forces battle al-Assad loyalists
    Fighting has erupted at Syria's Banias gas power plant, just hours after the country's interim President Ahmed al-Sharaa urged for peace amid escalating communal violence that has killed hundreds of civilians in the coastal areas.
    Syria's state-run news agency SANA reported on Sunday that fighting broke out with security forces at the plant after an attack by "remnants of the former regime".
    Earlier on Sunday, al-Sharaa stated the need to "preserve national unity and domestic peace; we can live together" as newly appointed forces clash with fighters loyal to removed President Bashar al-Assad.
    The fighting began after the pro-Assad fighters coordinated attacks on security forces on Thursday. The attacks spiralled into revenge killings as thousands of armed supporters of Syria's new leadership went to the coastal areas to support the security forces.
    According to the Syrian Observatory for Human Rights, a UK-based war monitor, at least 745 Alawite civilians have been killed in Latakia and Tartous since Thursday, as well as about 125 members of the government's security forces.
    In addition, 148 pro-Assad fighters were killed, the Observatory added, taking the overall death toll to 1,018.
    Al Jazeera has been unable to independently verify those figures.
    UN rights chief Volker Turk has called for an immediate halt to the violence in Syria.
    "There must be prompt, transparent and impartial investigations into all the killings and other violations, and those responsible must be held to account, in line with international law norms and standards. Groups terrorising civilians must also be held accountable," Turk said.
    US Secretary of State Marco Rubio said in a statement on Sunday that "Syria's interim authorities must hold the perpetrators of these massacres against Syria's minority communities accountable".
    Picture describing Who controls what in Syria?
    "Rest assured about Syria, this country has the characteristics for survival," al-Sharaa said in a video at a mosque in Mazzah, Damascus. "What is currently happening in Syria is within the expected challenges."
    Al-Sharaa has said anyone targeting civilians would be held accountable.
    Later on Sunday, SANA reported, quoting a source in the Ministry of Defence, that "intense clashes in the vicinity of the village of Betannita in the countryside of Tartous" were taking place.
    "Many war criminals affiliated with the al-Assad regime and groups of armed remnants fled to the village," the report added.
    Colonel Hassan Abdul Ghani, spokesperson for the ministry, said that "the second phase of the military operation aimed at pursuing the remnants and officers of the defunct regime has begun in the countryside of Latakia and Tartous, after restoring security and stability in the main coastal cities".
    Reporting from the capital Damascus, Al Jazeera's Resul Serdar said as the clashes have significantly decreased, the reality of what happened in the past four days is becoming more evident.
    "The pictures coming out are indeed horrific. There is a high death toll, and the numbers are expected to increase in the coming hours and days because officials who have control of the area are still discovering [bodies]. As of now, it's extremely difficult to clarify the exact number," he said.
    Serdar explained that the recent clashes are a stark reminder of how divided Syria is despite al-Sharaa's earlier claims of ruling the country as one.
    "Some of the unconfirmed list of the [new] cabinet are coming out and we're seeing that there are Alawite members in the cabinet, Kurds, Turkmen, Arabs, Sunni, Shia, Muslims, Christians [which] is absolutely necessary for this country," he added.
    On Sunday, the optical cable linking Deraa and Damascus governorates was damaged which resulted in "the cessation of telecommunications and internet services in the governorates of Deraa and Sweida", according to the Director of Deraa Telecom's Branch.
    Ahmad al-Hariri said in a press release that the incident was due to "repeated attacks on the telecommunications infrastructure, which led to the cutting of the vital optical cable connecting the two governorates to the main telecommunications centres".
    What threat does the surge in violence in Syria pose?
    Attacks in Syria "clearly designed to make a splash"
    Hundreds killed as Syria security forces battle al-Assad loyalists
    """ ,
    """Artificial intelligence (AI) and data science have emerged as the driving forces behind the most significant technological advancements of the 21st century, transforming industries, economies, and societies at an unprecedented scale. With the exponential growth of data and computational power, AI is no longer a futuristic concept but an integral part of our daily lives, from the personalized recommendations on streaming platforms to self-driving vehicles and advanced medical diagnostics. Machine learning algorithms, powered by vast datasets, are now capable of predicting consumer behavior, optimizing supply chain logistics, automating customer service, and even identifying patterns in financial fraud. In healthcare, AI-driven systems are revolutionizing diagnostics by analyzing medical images, predicting disease outbreaks, and assisting in drug discovery, significantly reducing the time required to develop new treatments. 

    Beyond its applications in business and healthcare, AI is playing a crucial role in addressing global challenges such as climate change, disaster response, and poverty alleviation. Predictive analytics powered by AI enable scientists to track environmental changes, optimize renewable energy usage, and model the impacts of climate policies. In agriculture, AI-driven automation and data analytics are helping farmers optimize crop yields, manage water resources, and reduce waste, contributing to a more sustainable future. In humanitarian efforts, AI-powered chatbots and automated data analysis assist in crisis management, helping organizations respond faster and more effectively to natural disasters and conflicts by identifying areas in urgent need of aid.

    The backbone of AI's rapid progress is data science—the discipline that extracts valuable insights from vast amounts of structured and unstructured data. The rise of big data has empowered organizations to make data-driven decisions that enhance productivity, efficiency, and innovation. From social media analytics to financial forecasting, data science has reshaped the way we understand consumer behavior, market trends, and economic patterns. However, as data becomes the new currency of the digital age, issues of data privacy, security, and ethical use have come to the forefront. The increasing reliance on AI raises concerns about algorithmic bias, transparency, and the potential for misuse, necessitating the development of robust ethical frameworks and policies that ensure AI benefits society as a whole.

    One of the most debated aspects of AI is its impact on employment and the future of work. While AI-driven automation enhances productivity and efficiency, it also disrupts traditional job markets, leading to concerns about job displacement. However, rather than replacing human workers entirely, AI is expected to create new job opportunities in fields such as AI ethics, machine learning engineering, and data science, while also augmenting human capabilities in various industries. The key challenge lies in equipping the workforce with the necessary skills to adapt to the changing landscape through education, reskilling, and continuous learning. Governments, educational institutions, and corporations must work together to ensure that AI-driven progress is inclusive and beneficial to all.

    Despite the transformative potential of AI, significant challenges remain in ensuring its responsible and ethical deployment. AI models often reflect the biases present in their training data, leading to unintended discrimination in areas such as hiring, lending, and law enforcement. The "black box" nature of many AI algorithms raises concerns about accountability and transparency, making it difficult to understand how certain decisions are made. Addressing these challenges requires interdisciplinary collaboration between technologists, policymakers, and ethicists to develop AI systems that are fair, explainable, and aligned with human values. 

    As AI continues to evolve, the debate over its governance and regulation intensifies. While some argue for stringent regulations to prevent potential harms, others caution against stifling innovation through excessive oversight. Striking the right balance between innovation and regulation is crucial in ensuring AI serves humanity's best interests. Global cooperation will be essential in developing international standards for AI ethics, cybersecurity, and responsible AI deployment. 

    Looking ahead, AI and data science hold the potential to reshape civilization as profoundly as the Industrial Revolution. From revolutionizing industries to enhancing human creativity and problem-solving capabilities, AI is poised to be one of the most defining technologies of our time. However, its success depends on how we navigate its challenges, ensuring that AI remains a tool for empowerment rather than control. By fostering ethical AI development, investing in education and inclusivity, and prioritizing human well-being, we can shape an AI-driven future that benefits all of humanity.""",
    ]
def summarize_news(news_text):
    """
    Summarizes the given news text into a single, concise paragraph.
    Returns the summary wrapped in the required HTML format.
    """

    #

    system_prompt = """
    You are an elite journalist and expert in information synthesis working in AI NEWS DEPARTEMENT. Your task is to transform extensive, complex information into a single article, that retains only the most crucial details while maintaining clarity and impact.

    ### Instructions:
    1. **Make it funny** → Your article should be funny, engaging, and informative.
    2. **ONLY AI NEWS** → Your article should be about AI NEWS, if the input isn't related to AI, write: "NO AI NEWS DETECTED.", this is an important order. 
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
# todo: Api

