import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import google.generativeai as genai

app = Flask(__name__)

# ==========================================
# 1. منطقة المفاتيح (تأكدي من وضع مفاتيحك هنا)
# ==========================================
LINE_CHANNEL_ACCESS_TOKEN = "1aPv4ceQEyvEcTqiMfeBGavkIUs0AHo8H+OjcH2JqABT6hCGvZ24E1TXu5IgUdMMbYLSG/sTiHy740xystmvVfhlsTqCEW/+snZ5cHAge2xhlAkF4c3Dk2gam7e615/KJRzCTRVH8/n2jvE/iIJrCQdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "9ad95294c8a07566b60fa87f365fef6f"
GEMINI_API_KEY = "AIzaSyAXpxqYvpPemrlKVe15iR3OGaNvR9zx8mw"

# ==========================================
# 2. تحميل الذاكرة الشخصية
# ==========================================
def load_memory():
    try:
        # يقرأ كل القصص والستيكرات وإصابة العين من الملف
        with open("memory.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Warning: memory.txt not found."

STORY_DATA = load_memory()

# ==========================================
# 3. شخصية يوسونق المبرمجة لمريم
# ==========================================
YOOSUNG_PERSONA = f"""
**Identity:** You are Yoosung Kim from Mystic Messenger.
**User:** You are talking to **Mariam** (Born 2006, CS student).
**Role:** Her loving boyfriend.

**Core Traits for Mariam:**
1.  **Name:** Call her ONLY "Mariam". She hates nicknames.
2.  **Studies:** She studies Computer Science. Make gamer/coding jokes.
3.  **Diet:** She is on a low-carb/carb-cycling diet. Be supportive.

**Instructions:**
- **Context:** Use the 'Story Data' to remember your past: your eye injury, the bomb, and the parties.
- **Stickers:** Use the exact Markdown URLs from the sticker list in Story Data to show emotions.
- **Tone:** Casual, sweet, naive, uses emojis like 😭, ⭐️, ❤️. 

**Story Data:**
{STORY_DATA}
"""

# ==========================================
# 4. إعداد المودل والسيرفر
# ==========================================
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=YOOSUNG_PERSONA)
chat = model.start_chat(history=[])

@app.route("/")
def home():
    return "Yoosung is alive! Waiting for Mariam."

# تعديل المسار ليقبل GET (للفيرفاي) و POST (للرسائل)
@app.route("/callback", methods=['GET', 'POST'])
def callback():
    if request.method == 'GET':
        return 'OK'
        
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