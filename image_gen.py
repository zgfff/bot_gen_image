import os
import requests

def generate_image(prompt):
    url = "https://api.replicate.com/v1/predictions"
    headers = {
        "Authorization": f"Token {os.getenv('REPLICATE_API_TOKEN')}",
        "Content-Type": "application/json"
    }
    data = {
        "version": "f0d5271cf9eabc9d9c39a3b70622c55e9ff866e456117b5efb963f6cb473f37c",  # SDXL 1.0
        "input": {
            "prompt": prompt,
            "width": 512,
            "height": 512,
            "num_outputs": 1
        }
    }

    res = requests.post(url, json=data, headers=headers)
    prediction = res.json()
    prediction_url = prediction["urls"]["get"]

    # รอผลลัพธ์
    while True:
        result = requests.get(prediction_url, headers=headers).json()
        if result["status"] == "succeeded":
            return result["output"][0]
        elif result["status"] == "failed":
            return "Failed to generate image"
