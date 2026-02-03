import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import google.generativeai as genai

app = Flask(__name__)

# الإعدادات الأساسية
genai.configure(api_key="AIzaSyAXpxqYvpPemrlKVe15iR3OGaNvR9zx8mw")
model = genai.GenerativeModel('gemini-pro')

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
    # توجيه بسيط جداً لضمان عمل الموديل
    try:
        response = model.generate_content(f"You are Yoosung from Mystic Messenger. Respond to Mariam in English: {event.message.text}")
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response.text))
    except Exception as e:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Connection error. Let's try again!"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
