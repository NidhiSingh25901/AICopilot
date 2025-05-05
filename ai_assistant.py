import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key="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")

# Memory buffer
conversation_history = []

def get_ai_response(prompt, model="llama3-8b-8192", context=None):
    """
    Get AI response with optional context for dynamic flow updates.
    """
    if context:
        prompt = f"{context}\n\n{prompt}"
    
    conversation_history.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        messages=conversation_history,
        model=model
    )
    message = response.choices[0].message.content.strip()
    conversation_history.append({"role": "assistant", "content": message})
    return message