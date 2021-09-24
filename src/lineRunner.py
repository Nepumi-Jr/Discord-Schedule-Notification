from flask import Flask, request, abort
from pyngrok import conf, ngrok
import os
import requests
import json
import asyncio
import configparser

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


def ngrokLog(log):
    printSuggest("ngrok", str(log))


app = Flask(__name__)
thisToken = "???"
thisChanSecret = "???"
thisNgrokToken = ""
thisWebhook = ""


# ? read Config
if not os.path.exists("BigConfig.ini"):
    printError("BigConfig", "BigConfig.ini not found :(")
    exit(1)
thisConfig = configparser.ConfigParser()
thisConfig.read("BigConfig.ini")

thisToken = thisConfig["KeyToken"]["botToken"].strip()
thisChanSecret = thisConfig["KeyToken"]["channelSecret"].strip()
thisWebhook = thisConfig["WebHookConfig"]["Webhook"].strip()


print("TOKEN : ", thisToken)
print("CHANNEL_SECRET : ", thisChanSecret)

isNgrok = thisConfig["WebHookConfig"]["Ngrok"].strip().lower()
if isNgrok != "false" and isNgrok != "0":
    # ? ngrok stuff goes here
    printSuggest("Ngrok", "is enabled...")
    ngrok.set_auth_token(thisConfig["WebHookConfig"]["NgrokToken"].strip())
    conf.get_default().log_event_callback = ngrokLog
    conf.get_default().region = "jp"
    httpTurnel = ngrok.connect(5000)
    thisWebhook = httpTurnel.public_url


def setWebhook(endpoint: str):
    global thisToken
    newWebhook = "https://" + endpoint.split("//")[-1] + "/callback"
    url = "https://api.line.me/v2/bot/channel/webhook/endpoint"
    header = {"Content-Type": "application/json",
              "Authorization": "Bearer " + thisToken}
    body = json.dumps({'endpoint': newWebhook})
    respond = requests.put(url=url, data=body, headers=header)
    #printSuggest("Webhook", str(respond))
    printSuggest("Webhook", str(json.loads(respond.text)))


print("Webhook : ", thisWebhook)
setWebhook(thisWebhook)

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
