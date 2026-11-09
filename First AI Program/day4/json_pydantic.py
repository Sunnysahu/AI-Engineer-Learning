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


# Structure 

from pydantic import BaseModel

class Ticket(BaseModel):
    name:str
    email:str
    issue:str

schema = Ticket.model_json_schema()

response_format = {
    "type" : "json_object"
}

system_prompt = f"""
Extract the personal information from the ticket strictly based on this schema and give me a json output
{schema}
"""

message_system = {
    "role":"system",
    "content": system_prompt
}

text = "Hello My name is Sunny, and i have issue in Iphone, address is Jamshedpur, Jharkhand, my email is sunny@gmail.com, phone no. is 8210"

prompt = f"""
This a Customer ticket and please extract the personal information from this {text}
"""

message = {
    "role" : "user",
    "content" : prompt
}

messages = [message_system, message]

response = client.chat.completions.create(model=model, messages=messages, response_format=response_format)
answer = response.choices[0].message.content    
print(answer)


# Further Application can read the above answer

import json
raw_json = answer
data_file = json.loads(raw_json)
ticket = Ticket(**data_file)

print(ticket.name)
print(ticket.email)
print(ticket.issue)