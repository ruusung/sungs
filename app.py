import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import google.generativeai as genai

app = Flask(__name__)

# الإعدادات
genai.configure(api_key="AIzaSyAXpxqYvpPemrlKVe15iR3OGaNvR9zx8mw")
# التغيير هنا: استخدام الموديل بدون كلمة models/ ليتوافق مع النسخة 0.8.0
model = genai.GenerativeModel('gemini-1.5-flash')

line_bot_api = LineBotApi("1aPv4ceQEyvEcTqiMfeBGavkIUs0AHo8H+OjcH2JqABT6hCGvZ24E1TXu5IgUdMMbYLSG/sTiHy740xystmvVfhlsTqCEW/+snZ5cHAge2xhlAkF4c3Dk2gam7e615/KJRzCTRVH8/n2jvE/iIJrCQdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("9ad95294c8a07566b60fa87f365fef6f")

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
    # الذاكرة التي تميزك يا مريم
    prompt = (
        f"You are Yoosung (Mystic Messenger). Respond to Mariam (CS student, 2006) in English. "
        f"Remember your left eye injury. Support her carb-cycling. "
        f"Input: {event.message.text}"
    )
    try:
        response = model.generate_content(prompt)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response.text))
    except Exception as e:
        # هذا السطر سيعطيكِ السبب الحقيقي (Auth, Quota, or Model)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"Debug Info: {str(e)[:50]}"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
