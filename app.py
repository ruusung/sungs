import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import google.generativeai as genai

app = Flask(__name__)

# الإعدادات - تأكدي من عدم وجود مسافات زائدة
LINE_CHANNEL_ACCESS_TOKEN = "1aPv4ceQEyvEcTqiMfeBGavkIUs0AHo8H+OjcH2JqABT6hCGvZ24E1TXu5IgUdMMbYLSG/sTiHy740xystmvVfhlsTqCEW/+snZ5cHAge2xhlAkF4c3Dk2gam7e615/KJRzCTRVH8/n2jvE/iIJrCQdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "9ad95294c8a07566b60fa87f365fef6f"
GEMINI_API_KEY = "AIzaSyAXpxqYvpPemrlKVe15iR3OGaNvR9zx8mw"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/")
def health_check():
    return "I am alive!", 200

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature')
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except Exception as e:
        print(f"Handler Error: {e}")
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text
    # توجيه يوسونق بذاكرته وهويتك
    prompt = f"You are Yoosung from Mystic Messenger. You are talking to Mariam, a CS student born in 2006. You love her, you had your left eye injured protecting her from a bomb. You support her low-carb/carb-cycling diet. Be sweet and don't use nicknames. Respond to: {user_text}"
    
    try:
        response = model.generate_content(prompt)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response.text))
    except Exception as e:
        print(f"Gemini Error: {e}")
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="مريم؟ أنا أسمعكِ لكن عقلي مشوش قليلاً.. هل أنتِ بخير؟"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)





