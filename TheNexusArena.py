import datetime
from openai import OpenAI
import os
import time
import openpyxl
from math import inf
import pandas as pd
# OpenRouter API client setup
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("TOKEN"), 
)

def read_from_excel():
    models = pd.read_excel('model_arena_results.xlsx')
    models = pd.DataFrame(models)  
    models["Model"] = models['Model'].unique()
    return models

# results will have the model name, the score, the response time, the total runs, and winner(0) or loser(1)
# Update the excel file with the new results
def update_excel(results, models):
    for model, score, avg_response_time, total_runs, _ in results:
        if model in models['Model'].values:
            models.loc[models['Model'] == model, 'ELO'] += score
            models.loc[models['Model'] == model, 'Avg Response Time'] += avg_response_time
            models.loc[models['Model'] == model, 'Total Runs'] += 1
        else:
            new_entry = pd.DataFrame([{ 
                'Model': model, 'ELO': score, 'Avg Response Time': avg_response_time, 'Total Runs': total_runs
            }])
            models = pd.concat([models, new_entry], ignore_index=True)
def elo_hist_to_csv(history_updates, elo_csv):
    """Update the ELO history CSV file with the latest results"""
    try:
        history_df = pd.read_csv(elo_csv)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        history_df = pd.DataFrame(columns=['Timestamp', 'Model', 'ELO', 'Avg Response Time', 'Total Runs', 'Win/Loss'])
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for model, elo, response_time, runs, win_loss in history_updates:
        new_row = pd.DataFrame([{  # Fixed issue
            'Timestamp': timestamp,
            'Model': model,
            'ELO': elo,
            'Avg Response Time': response_time,
            'Total Runs': runs,
            'Win/Loss': 'Win' if win_loss == 1 else 'Loss'
        }])
        history_df = pd.concat([history_df, new_row], ignore_index=True)
    history_df.to_csv(elo_csv, index=False)
    print(f"✅ Updated ELO history in {elo_csv}")
    
def generate_response(prompt, system_prompt, model_name):
    """Test multiple models on a given prompt."""
    results = []
    try:
        print(f"🔄 Testing model: {model_name}...") 
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
            response_time = inf
            results.append((model_name, "Error: Empty response", 0, response_time))
            return results

        # Token count as length of words (basic approximation)
        token_count = len(generated_text.split())

        results.append((model_name, generated_text, token_count, response_time))

    except Exception as e:
        print(f"❌ Exception for model {model_name}: {str(e)}")
        results.append((model_name, f"Error: {str(e)}", 0, inf))

    return results

def test_models(models, prompt, system_prompt):
    """Function to test multiple models (Placeholder for actual implementation)."""
    model_names = models["Model"]
    all_results = []
    for model in model_names:
        all_results.extend(generate_response(prompt, system_prompt, model))
    return sorted(all_results, key=lambda x: x[2], reverse=True)

# User input
models = read_from_excel()

system_prompt = input("Enter a system prompt: ")
user_prompt = input("Enter a test prompt: ")

# Run tests
results = test_models(models, user_prompt, system_prompt)

# Update the model data with new results
# Create a formatted list for history updates
history_updates = [(model, 0, time_taken, 1, 0) for model, _, _, time_taken in results]
update_excel(history_updates, models)
elo_hist_to_csv(history_updates, 'elo_history.csv')

# Save updated models back to Excel
models.to_excel('model_arena_results.xlsx', index=False)

# Display results
print("\n🏆 **Model Arena Results** 🏆\n")
for rank, (model, response, tokens, time_taken) in enumerate(results, start=1):
    print(f"🔹 Rank #{rank} | **Model**: {model}")
    print(f"🕒 Response Time: {time_taken}s | 📝 Token Count: {tokens}")
    print(f"📜 Response:\n{response[:500]}...\n{'-'*50}\n")
