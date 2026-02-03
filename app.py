import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import google.generativeai as genai

app = Flask(__name__)

# ==========================================
# 1. المفاتيح التي وضعتِها (تم دمجها)
# ==========================================
LINE_CHANNEL_ACCESS_TOKEN = "1aPv4ceQEyvEcTqiMfeBGavkIUs0AHo8H+OjcH2JqABT6hCGvZ24E1TXu5IgUdMMbYLSG/sTiHy740xystmvVfhlsTqCEW/+snZ5cHAge2xhlAkF4c3Dk2gam7e615/KJRzCTRVH8/n2jvE/iIJrCQdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "9ad95294c8a07566b60fa87f365fef6f"
GEMINI_API_KEY = "AIzaSyAXpxqYvpPemrlKVe15iR3OGaNvR9zx8mw"

# ==========================================
# 2. إعداد الشخصية والذاكرة
# ==========================================
def load_memory():
    try:
        with open("memory.txt", "r", encoding="utf-8") as f:
            return f.read()
    except:
        return "No memory file found."

YOOSUNG_PROMPT = f"""
You are Yoosung Kim from Mystic Messenger. 
You are talking to Mariam (CS student, born 2006). 
Use this memory to talk to her:
{load_memory()}

Instructions:
1. Call her Mariam (No nicknames).
2. Remember your eye injury from the bomb.
3. Use stickers and emojis like 😭, ⭐️, ❤️.
4. Be sweet and supportive of her diet.
"""

# ==========================================
# 3. إعداد السيرفر
# ==========================================
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=YOOSUNG_PROMPT)
chat = model.start_chat(history=[])

@app.route("/callback", methods=['GET', 'POST'])
def callback():
    if request.method == 'GET': return 'OK'
    signature = request.headers.get('X-Line-Signature')
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text
    try:
        response = chat.send_message(user_text)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response.text))
    except Exception as e:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="مريم، أحتاج لحظة للتفكير... هناك خطأ ما!"))

if __name__ == "__main__":
    app.run()
