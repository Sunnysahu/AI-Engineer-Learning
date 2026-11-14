import os
from pathlib import Path
from time import sleep
from dotenv import load_dotenv
from groq import Groq
import json

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key kaha hai bhai")

client=Groq(api_key=my_api_key)
model="openai/gpt-oss-20b"

def get_product_price(product):
    if product == 'iPhone 17':
        return 1000
    elif product == "iPhone 15":
        return 500
    else:
        return 0
    
def calculator(expression):
    try:
        return eval(expression)
    except:
        return "calc error!"

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_product_price",
            "description": "Get the price of a product",
            "parameters": {
                "type": "object",
                "properties": {
                    "product": {
                        "type": "string"
                    }
                },
                "required": ["product"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Calculate a mathematical expression",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

system_prompt = """
You are a shopping assistant.

You have these tools:

get_product_price(product)
calculator(expression)
IMPORTANT:
Call tools exactly like these examples:

Action: get_product_price("iPhone 17")
Action: calculator("5000 - 1000")

Never write:
get_product_price(product="iPhone 17")

Never write:
calculator(expression="5000 - 1000")
Follow these rules:

1. Decide what you need to do next.
2. Call ONLY ONE tool at a time.
3. After writing an Action, STOP immediately.
4. Never guess or invent a tool result.
5. Wait until you receive an Observation.
6. Then decide your next action.
7. When the task is complete, give the Final Answer.

Format:

Thought: what you need to do
Action: tool_name(argument)

When finished:

Final Answer: your answer
"""

available_functions = {
    "get_product_price": get_product_price,
    "calculator": calculator
}

def run_agent(question):

    messages = [
        {
            "role": "system",
            "content": "You are a shopping assistant. "
                       "Use get_product_price to find product prices. "
                       "Use calculator to calculate remaining money. "
                       "Use tools whenever necessary. "
                       "Give a final answer when finished."
        },
        {
            "role": "user",
            "content": question
        }
    ]

    for step in range(5):

        print("\n------------------")
        print("STEP", step + 1)
        print("------------------")

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        # No tool call means the model has finished
        if not message.tool_calls:
            print("Final Answer:", message.content)
            break

        # Save assistant's tool-call message
        messages.append(
            message.model_dump(exclude_none=True)
        )

        # Execute requested tools
        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name

            tool_args = json.loads(
                tool_call.function.arguments
            )

            print("Action:", tool_name, tool_args)

            if tool_name in available_functions:

                function = available_functions[tool_name]

                observation = function(**tool_args)

            else:
                observation = "Tool not found"

            print("Observation:", observation)

            # Send observation back to the model
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(observation)
            })




prompt="""
I have 5000 rupees. What is the price of an iphone 17?
and how much money will I have left?
"""
run_agent(prompt)