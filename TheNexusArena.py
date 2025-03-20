from openai import OpenAI
import os
import time
import numpy as np
import pandas as pd
import math
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
# OpenRouter API client setup
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("TOKEN"),
)

# List of models to compare
models = [
    "google/gemini-2.0-pro-exp-02-05:free",
    "sophosympatheia/rogue-rose-103b-v0.2:free",
    "open-r1/olympiccoder-7b:free",
    "open-r1/olympiccoder-32b:free",
    "google/gemma-3-27b-it:free",
    "deepseek/deepseek-r1-zero:free",
    "qwen/qwq-32b:free",
    "cognitivecomputations/dolphin3.0-r1-mistral-24b:free",

    "meta-llama/llama-3.3-70b-instruct:free"
]

# Excel file to store rankings
excel_file = "model_arena_results.xlsx"

tslika = [["google/gemini-2.0-pro-exp-02-05:free", 1500, 1.0, 1.0, 1], 
          ["qwen/qwq-32b:free", 1223, 1.0, 1.0, 1]]

def generate_response(prompt, system_prompt, model_name):
    """Test multiple models on a given prompt."""
    try:
        start_time = time.time()
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        end_time = time.time()
        response_time = round(end_time - start_time, 2)

        # Extract content
        generated_text = response.choices[0].message.content.strip()
        
        # Handle cases where response is empty
        if not generated_text:
            print(f"⚠️ Warning: Model {model_name} returned an empty response.")
            response_time = math.inf
            return "Error: Empty response", 0, response_time

        # Token count as length of words (basic approximation)
        token_count = len(generated_text.split())

        return generated_text, token_count, response_time

    except Exception as e:
        print(f"❌ Exception for model {model_name}: {str(e)}")
        return f"Error: {str(e)}", 0, 0

def expected_score(model_a, model_b):
    return 1 / (1 + 10**((model_a - model_b)/400))


def test_models(models, system_prompt, prompt):
    first_contestant = np.random.randint(0,len(models.index))
    second_contestant = np.random.randint(0,len(models.index))
    while (second_contestant == first_contestant):
        second_contestant = np.random.randint(0,len(models.index))
    print(" ==================== Prompt ========================= ")
    print("\t" + prompt)
    print()
    firstResponse, firstToken, firstDelay = generate_response(prompt, system_prompt, models.loc[first_contestant, "Model Name"])
    print("\n ================ Model Number A ===================== ")
    print("\t" + firstResponse)
    print()
    secondResponse, secondToken, secondDelay = generate_response(prompt, system_prompt, models.loc[second_contestant, "Model Name"])
    print("\n ================ Model Number B ===================== ")
    print("\t" + secondResponse)
    first_data = models.loc[first_contestant, :].values
    second_data = models.loc[second_contestant, :].values
    Choice = input("\nshkon rbe7? A wla B wla Ta wa7ed? ( A | B | T ) : ")
    
    #Update ELO
    ELO_COEFICCIENT = 100
    a_state = 0
    b_state = 0
    verdict = ""
    if Choice == "A":
        verdict = " A won "
        a_state = 1
        b_state = 0
    elif Choice == "B" :
        verdict = " B won "
        a_state = 0
        b_state = 1
    else:
        verdict = " It was a tie "
        a_state = 0.5
        b_state = 0.5
    first_data[1] = round(first_data[1] + ELO_COEFICCIENT *  (a_state - expected_score(second_data[1], first_data[1])))
    second_data[1] = round(second_data[1] + ELO_COEFICCIENT *  (b_state - expected_score(first_data[1], second_data[1])))

    # Update Local Runs
    first_data[4] += 1
    second_data[4] += 1

    # Update Average response time
    first_data[2] = round(((first_data[2]*(first_data[4] - 1)) + firstDelay)/(first_data[4]),2)
    second_data[2] = round(((second_data[2]*(second_data[4] - 1)) + secondDelay)/(second_data[4]),2)

    #Update Average Token Size
    first_data[3] = round(((first_data[3]*(first_data[4] - 1)) + firstToken)/(first_data[4]),2)
    second_data[3] = round(((second_data[3]*(second_data[4] - 1)) + secondToken)/(second_data[4]),2)
        
    #Update Original DataFrame
    models.loc[first_contestant] = first_data
    models.loc[second_contestant] = second_data

    # Show Results
    print("\n" + "=" * 45)
    print(">        📊 Final Results Summary 📊        <")
    print("=" * 45)
    print(f"\n✅ Verdict: {verdict}\n")

    print("🎯 Model A:")
    print("-" * 20)
    for i in models.columns:
        print(f"  • {i} : {models.loc[first_contestant, i]}")

    print("\n🎯 Model B:")
    print("-" * 20)
    for i in models.columns:
        print(f"  • {i} : {models.loc[second_contestant, i]}")

    print("=" * 45 + "\n")
    


# get input
models =  pd.DataFrame(tslika, columns=["Model Name", "ELO", "Average Response Time", "Average Token Size", "Total Runs"]) #input

current = 1

# Print The Menu
console = Console()

banner_text = Text("Welcome To ChatBot Arena", style="bold magenta", justify="center")
panel = Panel.fit(banner_text, border_style="bright_cyan", padding=(1, 4), title="🔥 AI Arena 🔥", subtitle="🤖 May the best model win!")

console.print(panel)
 

while True:
    
    print()
    print("> > > Match Number : " + str(current))
    current += 1
    print()

    # get prompts
    prompt = input("| Yooo, Something in Mind? : ")
    print()
    system_prompt = "You are a helpful assistant"

    #Arena
    test_models(models,system_prompt, prompt)

    #Write to History
    
    
# Write Output

# Who's Better Barcelona or Real Madrid?