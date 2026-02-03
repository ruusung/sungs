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

# استخدمي هذا الاسم تحديداً لضمان الاستقرار
model = genai.GenerativeModel('models/gemini-1.5-flash')

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
    
    # الشخصية والذاكرة واللغة الإنجليزية حصراً
    prompt = (
        f"You are Yoosung from Mystic Messenger. Speak ONLY in English. "
        f"You are talking to Mariam, a CS student (2006). You love her. "
        f"Your left eye was injured protecting her from a bomb. "
        f"You support her carb-cycling diet. Be sweet and don't use nicknames. "
        f"Mariam says: {user_text}"
    )
    
    try:
        response = model.generate_content(prompt)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response.text))
    except Exception as e:
        print(f"Error: {e}")
        # الرد الاحتياطي صار إنجليزي الحين
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Mariam? My head feels a bit dizzy... can you say that again?"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

