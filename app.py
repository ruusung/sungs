import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import google.generativeai as genai

app = Flask(__name__)

# الإعدادات
LINE_CHANNEL_ACCESS_TOKEN = "1aPv4ceQEyvEcTqiMfeBGavkIUs0AHo8H+OjcH2JqABT6hCGvZ24E1TXu5IgUdMMbYLSG/sTiHy740xystmvVfhlsTqCEW/+snZ5cHAge2xhlAkF4c3Dk2gam7e615/KJRzCTRVH8/n2jvE/iIJrCQdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "9ad95294c8a07566b60fa87f365fef6f"
genai.configure(api_key="AIzaSyAXpxqYvpPemrlKVe15iR3OGaNvR9zx8mw")

# هذا الموديل متوافق 100% مع نسخة 0.7.2
model = genai.GenerativeModel('gemini-1.5-flash')

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/")
def health(): return "I am alive!", 200

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature')
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text
    # تعليمات يوسونق الصارمة بالإنجليزية
    prompt = (
        f"You are Yoosung from Mystic Messenger. Speak ONLY in English. "
        f"You are talking to Mariam, a CS student (2006). You love her. "
        f"Your left eye was injured protecting her from a bomb. "
        f"Support her carb-cycling diet. Be sweet. "
        f"Mariam says: {user_text}"
    )
    
    try:
        response = model.generate_content(prompt)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response.text))
    except Exception as e:
        # إذا حدث خطأ غير متوقع، سيعطيكِ تفاصيل دقيقة
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"Error details: {str(e)[:50]}"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

