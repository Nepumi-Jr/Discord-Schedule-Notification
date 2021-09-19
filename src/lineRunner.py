from flask import Flask, request, abort
import os
import requests
import json
import asyncio

from src.printUtil import *

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)
thisToken = "???"
thisChanSecret = "???"
thisNgrokToken = ""

if not os.path.exists("TOKEN"):
    printSuggest(
        "Token", "TOKEN not found...\nyou can save your own token by write it in file TOKEN")
    thisToken = input("enter a TOKEN : ")
else:
    try:
        with open("TOKEN", "r") as f:
            thisToken = f.read()
    except:
        printWarning("Token", "Can't read TOKEN...")
        thisToken = input("enter a TOKEN : ")

if not os.path.exists("CHANNEL_SECRET"):
    printSuggest(
        "Channel secret", "Channel secret not found...\nyou can save your own token by write it in file CHANNEL_SECRET")
    thisChanSecret = input("enter a CHANNEL_SECRET : ")
else:
    try:
        with open("CHANNEL_SECRET", "r") as f:
            thisChanSecret = f.read()
    except:
        printWarning("Channel secret", "Can't read CHANNEL_SECRET...")
        thisChanSecret = input("enter a CHANNEL_SECRET : ")


print("TOKEN : ", thisToken)
print("CHANNEL_SECRET : ", thisChanSecret)

thisToken = thisToken.strip()
thisChanSecret = thisChanSecret.strip()


def ngrokLog(log):
    printSuggest("ngrok", str(log))


line_bot_api = LineBotApi(thisToken)
handler = WebhookHandler(thisChanSecret)


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    printSuggest("Message", event.message.text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

# TODO : loop handler

# async def loopu():
#     while(True):
#         print("ayaya")
#         await asyncio.sleep(2)

# loop = asyncio.get_event_loop()
# loop.create_task(loopu())
# loop.run_forever()
# print("Meowwwww")
