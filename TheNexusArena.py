from openai import OpenAI
import os
import time
import openpyxl
from math import inf
# OpenRouter API client setup
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("TOKEN"),  # Replace with your actual API key
)

# List of models to compare
models = [
    "sophosympatheia/rogue-rose-103b-v0.2:free",
    "open-r1/olympiccoder-7b:free",
    "open-r1/olympiccoder-32b:free",
    "google/gemma-3-27b-it:free",
    "deepseek/deepseek-r1-zero:free",
    "qwen/qwq-32b:free",
    "cognitivecomputations/dolphin3.0-r1-mistral-24b:free",
    "google/gemini-2.0-pro-exp-02-05:free",
    "meta-llama/llama-3.3-70b-instruct:free"
]

# Excel file to store rankings
excel_file = "model_arena_results.xlsx"

def load_or_create_excel():
    """Load existing Excel file or create a new one."""
    if not os.path.exists(excel_file):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Arena Results"
        sheet.append(["Model", "Total Score", "Last Score", "Avg Response Time", "Total Runs"])
        workbook.save(excel_file)
    return openpyxl.load_workbook(excel_file)

def update_excel(results):
    """Update Excel with new rankings."""
    workbook = load_or_create_excel()
    sheet = workbook.active
    model_data = {sheet.cell(row=i, column=1).value: i for i in range(2, sheet.max_row + 1)}

    for model, _, tokens, time_taken in results:
        score = tokens  # Use token count as a simple score metric
        row = model_data.get(model)

        if row:
            # Update existing model entry
            total_score = sheet.cell(row=row, column=2).value + score
            last_score = score
            total_runs = sheet.cell(row=row, column=5).value + 1
            avg_time = round(((sheet.cell(row=row, column=4).value * (total_runs - 1)) + time_taken) / total_runs, 2)

            sheet.cell(row=row, column=2, value=total_score)
            sheet.cell(row=row, column=3, value=last_score)
            sheet.cell(row=row, column=4, value=avg_time)
            sheet.cell(row=row, column=5, value=total_runs)
        else:
            # Insert new model entry
            sheet.append([model, score, score, time_taken, 1])

    workbook.save(excel_file)

def test_models(prompt, system_prompt):
    """Test multiple models on a given prompt."""
    results = []

    for model in models:
        try:
            print(f"🔄 Testing model: {model}...")  # Debugging output
            start_time = time.time()
            response = client.chat.completions.create(
                model=model,
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
                continue

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
