import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import schedule

user_id = "U227736503c290a9f5fbe50b3423d5df2"

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"

def send_showAll(reply_token,text):
    line_bot_api = LineBotApi(channel_access_token)
    
            
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"
def job_that_executes_once(push_text_str):
# 此處編寫的任務只會執行一次...
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.push_message(user_id, TextSendMessage(text=push_text_str))
    return schedule.CancelJob

"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
