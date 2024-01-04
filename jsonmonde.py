import os
import openai

# Set your API key here directly or ensure it's set as an environment variable
openai.api_key = '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'

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-1106",
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
        {"role": "user", "content": "Analyze the exercise Barbell Bench Press in JSON format and provide details about its agonists, synergists, joint movements, and force type."}
    ]
)

print(response.choices[0].message.content)

