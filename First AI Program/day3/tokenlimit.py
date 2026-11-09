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
prompt1 = "Hi"
prompt2 = "Time Travel in Detail"
prompt3 = "Write a 30 words eassy on Machine learning"

prompts = [prompt1, prompt2, prompt3]

for prompt in prompts :
    message = {
        "role" : role,
        "content" : prompt
    }
    messages = [message]
    resposne = client.chat.completions.create(model = model, messages = messages, max_tokens = 50)
    usage = resposne.usage
    print(f"Prompt : {prompt} --> Your Tokens : {usage.prompt_tokens} --> Completion Tokens : {usage.completion_tokens} --> Total Token : {usage.prompt_tokens + usage.completion_tokens} --> Finish Reason : {resposne.choices[0].finish_reason}")



# message_system = {
#     "role" : "system",
#     "content" : "You Are my brand manager who suggest name for my food company. name should be in one word nothing other unnecesary text"
# }

# message = {
#     "role" : role,
#     "content" : prompt
# }

# messages = [message_system, message]

# response = client.chat.completions.create(model = model, messages = messages, temperature = 2)
# print(response.choices[0].message.content)

