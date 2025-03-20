from openai import OpenAI
import os
import time
import openpyxl
from math import inf
import pandas as pd
# OpenRouter API client setup
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("TOKEN"),  # Replace with your actual API key
)
def read_from_excel():
    models = pd.read_excel('model_arena_results.xlsx')
    # List of models to compare
    models = pd.modelsFrame(models)
    models["Model"] = models['Model'].unique()
# results will have the model name, the score, the response time, the total runs, and winner(0) or loser(1)
def update_excel(results, models):
    for model, score, Avg_Response_Time, Total_Runs,_ in results:
        if model in models['Model'].values:
            models.loc[models['Model'] == model, 'ELO'] += score
            models.loc[models['Model'] == model, 'Avg Response Time'] += Avg_Response_Time
            models.loc[models['Model'] == model, 'Total Runs'] += 1
        else:
            models = models.append({'model': model, 'score': score, 'Avg_Response_Time': Avg_Response_Time, 'Total_Runs': Total_Runs}, ignore_index=True)
def Elo_hist_to_csv(results, Elo_csv):
    """
    Update the ELO history CSV file with the latest results
    
    Args:
        results (list): List of tuples with (model, score, Avg_Response_Time, Total_Runs)
        Elo_csv (str): Path to the CSV file storing ELO history
    
    Returns:
        None: The function updates the CSV file directly
    """
    try:
        # Read existing ELO history
        models_history = pd.read_csv(Elo_csv)
        
        # Get the current timestamp for this update
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # For each model in the results, add a new entry to the history
        for model, elo_score, avg_response_time, total_runs in results:
            # Create a new row with the current data
            new_row = {
                'Timestamp': timestamp,
                'Model': model,
                'ELO': elo_score
            }
            
            # Append the new row to the history DataFrame
            models_history = pd.concat([models_history, pd.DataFrame([new_row])], ignore_index=True)
        
        # Save the updated history back to CSV
        models_history.to_csv(Elo_csv, index=False)
        print(f"✅ ELO history updated successfully in {Elo_csv}")
        
    except Exception as e:
        print(f"❌ Error updating ELO history: {str(e)}")
        
        # If the file doesn't exist, create it with the current results
        if "No such file or directory" in str(e):
            try:
                # Create a new DataFrame with the current results
                columns = ['Timestamp', 'Model', 'ELO', 'Avg_Response_Time', 'Total_Runs']
                new_history = pd.DataFrame(columns=columns)
                
                # Add timestamp to each result
                import datetime
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                for model, elo_score, avg_response_time, total_runs in results:
                    new_row = {
                        'Timestamp': timestamp,
                        'Model': model,
                        'ELO': elo_score,
                        'Avg_Response_Time': avg_response_time,
                        'Total_Runs': total_runs
                    }
                    new_history = pd.concat([new_history, pd.DataFrame([new_row])], ignore_index=True)
                
                # Save the new history to CSV
                new_history.to_csv(Elo_csv, index=False)
                print(f"✅ Created new ELO history file: {Elo_csv}")
            except Exception as create_error:
                print(f"❌ Error creating new ELO history file: {str(create_error)}")
    

# def load_or_create_excel():
#     """Load existing Excel file or create a new one."""
#     if not os.path.exists(excel_file):
#         workbook = openpyxl.Workbook()
#         sheet = workbook.active
#         sheet.title = "Arena Results"
#         sheet.append(["Model", "Total Score", "Last Score", "Avg Response Time", "Total Runs"])
#         workbook.save(excel_file)
#     return openpyxl.load_workbook(excel_file)

# def update_excel(results):
#     """Update Excel with new rankings."""
#     workbook = load_or_create_excel()
#     sheet = workbook.active
#     model_models = {sheet.cell(row=i, column=1).value: i for i in range(2, sheet.max_row + 1)}

#     for model, _, tokens, time_taken in results:
#         score = tokens  # Use token count as a simple score metric
#         row = model_models.get(model)

#         if row:
#             # Update existing model entry
#             total_score = sheet.cell(row=row, column=2).value + score
#             last_score = score
#             total_runs = sheet.cell(row=row, column=5).value + 1
#             avg_time = round(((sheet.cell(row=row, column=4).value * (total_runs - 1)) + time_taken) / total_runs, 2)

#             sheet.cell(row=row, column=2, value=total_score)
#             sheet.cell(row=row, column=3, value=last_score)
#             sheet.cell(row=row, column=4, value=avg_time)
#             sheet.cell(row=row, column=5, value=total_runs)
#         else:
#             # Insert new model entry
#             sheet.append([model, score, score, time_taken, 1])

#     workbook.save(excel_file)

def generate_response(prompt, system_prompt, model_name):
    """Test multiple models on a given prompt."""
    results = []
    try:
        print(f"🔄 Testing model: {model}...")  # Debugging output
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
            print(f"⚠️ Warning: Model {model} returned an empty response.")
            response_time = inf
            results.append((model, "Error: Empty response", 0, response_time))

        # Token count as length of words (basic approximation)
        token_count = len(generated_text.split())

        results.append((model, generated_text, token_count, response_time))

    except Exception as e:
        print(f"❌ Exception for model {model}: {str(e)}")
        results.append((model, f"Error: {str(e)}", 0, 0))

    results.sort(key=lambda x: x[1], reverse=True)
    return results

# User inputs prompt
system_prompt = input("Enter a system prompt: ")
user_prompt = input("Enter a test prompt: ")


# Get results
arena_results = test_models(user_prompt, system_prompt)

# Display results
print("\n🏆 **Model Arena Results** 🏆\n")
for rank, (model, response, tokens, time_taken) in enumerate(arena_results, start=1):
    print(f"🔹 Rank #{rank} | **Model**: {model}")
    print(f"🕒 Response Time: {time_taken}s | 📝 Token Count: {tokens}")
    print(f"📜 Response:\n{response[:500]}...\n{'-'*50}\n")
