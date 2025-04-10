import datetime
from openai import OpenAI
import os
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import time
import numpy as np
import pandas as pd
from math import inf
from dotenv import load_dotenv
import openpyxl
# Load environment variables
load_dotenv()

# OpenRouter API client setup
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("TOKEN"), 
)

def read_from_excel():
    try:
        models = pd.read_excel('model_arena_results.xlsx')
        models = pd.DataFrame(models)
        
        # Filter out any invalid model names if needed
        # This is optional but could help prevent API errors
        valid_models = models[models['Model'].notna()]
        
        if valid_models.empty:
            print("Warning: No valid models found in the Excel file.")
            
        return valid_models
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        # Return empty DataFrame instead of None to avoid errors
        return pd.DataFrame(columns=["Model", "ELO", "Response_Time", "Tokens", "Runs", "Failures"])

# results will have the Model, the score, the response time, the total runs, and winner(0) or loser(1)
# Update the excel file with the new results
def elo_hist_to_csv(history_updates, elo_csv):
    with open(elo_csv, "a") as f:
        f.write(",".join(history_updates) + "\n")
        f.flush()
    
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
            print(f"⚠️  Warning: Model {model_name} returned an empty response.")
            # Only update failures if the model exists in the DataFrame
            if model_name in models.index:
                models.loc[model_name, "Failures"] += 1
            response_time = inf
            return "Error: Empty response", -1, response_time

        # Token count as length of words (basic approximation)
        token_count = len(generated_text.split())

        return generated_text, token_count, response_time

    except Exception as e:
        print(f"❌  Exception for model {model_name}: {str(e)}")
        # Only update failures if the model exists in the DataFrame
        if model_name in models.index:
            models.loc[model_name, "Failures"] += 1
        return f"Error: {str(e)}", -1, 0

def expected_score(model_a, model_b):
    return 1 / (1 + 10**((model_a - model_b)/400))

# Run tests
def test_models(models, system_prompt, prompt):
    first_contestant = np.random.randint(0,len(models.index))
    second_contestant = np.random.randint(0,len(models.index))
    while (second_contestant == first_contestant):
        second_contestant = np.random.randint(0,len(models.index))
    print(" ==================== Prompt ========================= ")
    print("\t" + prompt)
    print()
    firstResponse, firstToken, firstDelay = generate_response(prompt, system_prompt, models.loc[first_contestant, "Model"])
    if firstToken == -1:
        print("Error in Model A")
        return
    print("\n ================ Model Number A ===================== ")
    print("\t" + firstResponse)
    print()
    secondResponse, secondToken, secondDelay = generate_response(prompt, system_prompt, models.loc[second_contestant, "Model"])
    if secondToken == -1:
        print("Error in Model B")
        return
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

    # Update ELO with consistent parameter ordering
    first_expected = expected_score(second_data[1], first_data[1])
    second_expected = expected_score(first_data[1], second_data[1])

    first_data[1] = round(first_data[1] + ELO_COEFICCIENT * (a_state - first_expected))
    second_data[1] = round(second_data[1] + ELO_COEFICCIENT * (b_state - second_expected))

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
models = read_from_excel()
current = 1
# Print The Menu
print()
console = Console()

banner_text = Text("Welcome To The Nexus Arena", style="bold magenta", justify="center")
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

    # Check if models DataFrame is not empty before testing
    if not models.empty:
        # Arena
        test_models(models, system_prompt, prompt)

        # Write to History
        elo_models = [str(i) for i in models.loc[:, "ELO"].values]
        elo_hist_to_csv(elo_models, 'elo_history.csv')
        models.to_excel('model_arena_results.xlsx', index=False)
    else:
        print("Error: No valid models found in the Excel file.")