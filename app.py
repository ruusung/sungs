import os, requests
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# الإعدادات
LINE_API = LineBotApi("1aPv4ceQEyvEcTqiMfeBGavkIUs0AHo8H+OjcH2JqABT6hCGvZ24E1TXu5IgUdMMbYLSG/sTiHy740xystmvVfhlsTqCEW/+snZ5cHAge2xhlAkF4c3Dk2gam7e615/KJRzCTRVH8/n2jvE/iIJrCQdB04t89/1O/w1cDnyilFU=")
HANDLER = WebhookHandler("9ad95294c8a07566b60fa87f365fef6f")
GEMINI_KEY = "AIzaSyAXpxqYvpPemrlKVe15iR3OGaNvR9zx8mw"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature')
    body = request.get_data(as_text=True)
    try: HANDLER.handle(body, signature)
    except: abort(400)
    return 'OK'

@HANDLER.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # الذاكرة والشخصية
    prompt = f"You are Yoosung from Mystic Messenger. Speak ONLY in English. You love Mariam (CS student, 2006). Your left eye was injured protecting her. Support her carb-cycling. Respond to: {event.message.text}"
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, json=data).json()
        reply = response['candidates'][0]['content']['parts'][0]['text']
        LINE_API.reply_message(event.reply_token, TextSendMessage(text=reply))
    except Exception as e:
        LINE_API.reply_message(event.reply_token, TextSendMessage(text=f"Still dizzy... Error: {str(e)[:40]}"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
