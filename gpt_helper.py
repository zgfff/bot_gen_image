import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_prompt(thai_text):
    messages = [
        {"role": "system", "content": "You are a Thai textile designer who helps convert Thai inspiration into English prompts for AI image generation."},
        {"role": "user", "content": f"สร้าง prompt สำหรับ AI เพื่อวาดลายผ้าทอจากคำว่า: {thai_text}"}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )
    return response.choices[0].message.content.strip()
