from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, LocationMessage
import os
from api.getweathedata import GetWeatherData
from api.geogetter import GetCoordinate

app = Flask(__name__)

# 環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = ""
YOUR_CHANNEL_SECRET = ""

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
    get_coordinate = GetCoordinate(input_text)
    geocodes = get_coordinate.coordinate()
    
    if geocodes == 1:
        reply_text = '都市名を入力してください'
    else:
        lat = geocodes[0]  # 緯度
        lon = geocodes[1]  # 経度
        r = GetWeatherData(input_text, lat, lon)
        reply_text = r.show_weatherData()

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))


@handler.add(MessageEvent, message=LocationMessage)
def handle_location(event):
    input_text = event.message.address

    r = GetWeatherData(input_text)
    reply_text = r.show_weatherData()

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))


if __name__ == "__main__":
    # app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
