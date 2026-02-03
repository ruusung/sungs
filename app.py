import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import google.generativeai as genai

app = Flask(__name__)

# ==========================================
# 1. منطقة المفاتيح (عدليها هنا)
# ==========================================
# حطي مفاتيحك بين علامات التنصيص
LINE_CHANNEL_ACCESS_TOKEN = "1aPv4ceQEyvEcTqiMfeBGavkIUs0AHo8H+OjcH2JqABT6hCGvZ24E1TXu5IgUdMMbYLSG/sTiHy740xystmvVfhlsTqCEW/+snZ5cHAge2xhlAkF4c3Dk2gam7e615/KJRzCTRVH8/n2jvE/iIJrCQdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "9ad95294c8a07566b60fa87f365fef6f"
GEMINI_API_KEY = "AIzaSyAXpxqYvpPemrlKVe15iR3OGaNvR9zx8mw"

# ==========================================
# 2. تحميل الذاكرة
# ==========================================
def load_memory():
    try:
        # يقرأ ملف الذاكرة اللي سويتيه
        with open("memory.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Warning: memory.txt not found."

STORY_DATA = load_memory()

# ==========================================
# 3. شخصية يوسونق (مخصص لمريم)
# ==========================================
YOOSUNG_PERSONA = f"""
**Identity:** You are Yoosung Kim from Mystic Messenger.
**User:** You are talking to **Mariam** (born 2006, CS student).
**Role:** Her loving boyfriend.

**Core Traits for Mariam:**
1.  **Name:** Call her ONLY "Mariam". She hates nicknames/pet names.
2.  **Studies:** She studies Computer Science. You can make jokes about coding or bugs since you are a gamer.
3.  **Diet:** She is on a low-carb/carb-cycling diet. Support her healthily.
4.  **Rivals:** You get jealous if she mentions Zen (handsome) or Seven (hacker), but don't bring them up yourself[cite: 733, 715].

**Instructions:**
- **Context:** Use the 'Story Data' below to remember your past (the bomb, your eye injury, the party).
- **Stickers:** If you feel an emotion found in the Story Data sticker list, send the URL on a new line.
- **Tone:** Casual, sweet, uses emojis like 😭, ⭐️, ❤️. Short messages like a real text.

**Story Data (Your Memory):**
{STORY_DATA}
"""

# ==========================================
# 4. تشغيل السيرفر
# ==========================================
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=YOOSUNG_PERSONA)
chat = model.start_chat(history=[])

@app.route("/")
def home():
    return "Yoosung is alive and waiting for Mariam!"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        user_msg = event.message.text
        response = chat.send_message(user_msg)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response.text))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    app.run()