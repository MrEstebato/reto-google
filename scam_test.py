import os
import google.generativeai as genai

# genai.configure(api_key=os.environ["GEMINI_API_KEY"])

genai.configure(api_key="AIzaSyDapeWfBoIaJHEU5ElASDhUnuJaafaEGRc")  # Esteban

# genai.configure(api_key="AIzaSyDg7kpkjHkkSKLWK5N0z-JSJvMvpp4fTdQ") #Dany

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # Especificar aqui las instrucciones
    system_instruction='You will receive a conversation in phrases, determine whether the conersation conversation is a scam. Use this schema to return a scam value between 0 and 100 and a reason why you think the user is being scammed in spanish: {"scamValue": int, "reason" : str}',
)

chat_session = model.start_chat(history=[])

with open("response.json", "w") as f:
    prompt = "Message"
    response = chat_session.send_message(prompt)
    f.write(response.text)

# response = chat_session.send_message("Aqui van los prompts.")
