from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, ImageSendMessage
from linebot.exceptions import InvalidSignatureError
from dotenv import load_dotenv
import os

from gpt_helper import generate_prompt
from image_gen import generate_image

load_dotenv()

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return "Invalid signature", 400

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    thai_text = event.message.text
    prompt = generate_prompt(thai_text)
    image_url = generate_image(prompt)

    image_msg = ImageSendMessage(
        original_content_url=image_url,
        preview_image_url=image_url
    )
    line_bot_api.reply_message(event.reply_token, image_msg)

if __name__ == "__main__":
    app.run(port=5000)
