import os
import google.generativeai as genai
import time

# genai.configure(api_key=os.environ["GEMINI_API_KEY"])

genai.configure(api_key="AIzaSyDapeWfBoIaJHEU5ElASDhUnuJaafaEGRc")  # Esteban

# genai.configure(api_key="AIzaSyDg7kpkjHkkSKLWK5N0z-JSJvMvpp4fTdQ") #Dany

base_model = "models/gemini-1.5-flash-001-tuning"
training_data = [
    {"text_input": "1", "output": "2"},
    # ... more examples ...
    # ...
    {"text_input": "seven", "output": "eight"},
]
operation = genai.create_tuned_model(
    # You can use a tuned model here too. Set `source_model="tunedModels/..."`
    display_name="increment",
    source_model=base_model,
    epoch_count=20,
    batch_size=4,
    learning_rate=0.001,
    training_data=training_data,
)

for status in operation.wait_bar():
    time.sleep(10)

result = operation.result()
print(result)
# # You can plot the loss curve with:
# snapshots = pd.DataFrame(result.tuning_task.snapshots)
# sns.lineplot(data=snapshots, x='epoch', y='mean_loss')

model = genai.GenerativeModel(model_name=result.name)
result = model.generate_content("III")
print(result.text)  # IV

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

model = genai.GenerativeModel(model_name="tunedModels/my-increment-model")
result = model.generate_content("III")
print(result.text)  # "IV"

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # Especificar aqui las instrucciones
    system_instruction='You will receive a conversation in phrases, determine whether the conersation conversation is a scam. Use this schema to return a scam value between 0 and 100 and a reason why you think the user is being scammed in spanish: {"scamValue": int, "reason" : str}',
)
