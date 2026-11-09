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

text = "Hello My name is Sunny, and i have issue in Iphone, address is Jamshedpur"

prompt = f"""
This a Customer ticket and please extract the personal information from this {text}
"""

message = {
    "role" : role,
    "content" : prompt
}

message = [message]

response = client.chat.completions.create(model=model, messages=message, temperature=2)
answer = response.choices[0].message.content    
print(answer)