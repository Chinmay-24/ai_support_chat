import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

# Pick a model – update name if you want a different one
MODEL_ID =  "gemini-flash-latest"

def generate_ai_reply(messages, system_prompt=None):
    """
    messages: list of {"role": "user"/"assistant", "content": "text"}
    system_prompt: optional str with instructions
    """
    model = genai.GenerativeModel(MODEL_ID)

    # Build the prompt from history
    parts = []
    if system_prompt:
        parts.append(f"System: {system_prompt}")
    for msg in messages:
        parts.append(f"{msg['role'].capitalize()}: {msg['content']}")
    prompt_text = "\n".join(parts)

    response = model.generate_content(prompt_text)
    # response.text contains the main output
    return response.text.strip()
