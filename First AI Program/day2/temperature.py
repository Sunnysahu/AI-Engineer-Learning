import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API Key Not Available")

client = Groq(api_key = my_api_key)

# model = "llama-3.3-70b-versatile"
model = "openai/gpt-oss-20b"

role = "user"
prompt = "Suggest a name for my good company"

message_system = {
    "role" : "system",
    "content" : "You Are my brand manager who suggest name for my food company. name should be in one word nothing other unnecesary text"
}

message = {
    "role" : role,
    "content" : prompt
}

messages = [message_system, message]

response = client.chat.completions.create(model = model, messages = messages, temperature = 2)
print(response.choices[0].message.content)

