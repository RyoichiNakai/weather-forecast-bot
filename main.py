from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
from getweathedata import GetWeatherData

app = Flask(__name__)

# 環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = "8jJ/l8M2VZPF9yYx4uKG/vYwiYiSisKvUmdWtOVTdG9J78rsguW9fFhsqLamRW8v/zy9rRQC/p4xQk6W2q9SZydJvpSWSWwNArCNpsSObahQaVtr3FeNO4SomuqTVEyOMrm/4ZzG58j6Uu10TUze1gdB04t89/1O/w1cDnyilFU="
YOUR_CHANNEL_SECRET = "9d09dedc101e44bb3beccdc346336ccc"

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    input_text = event.message.text

    r = GetWeatherData(input_text)
    reply_text = r.show_weatherData()

    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply_text))


if __name__ == "__main__":
    # app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
