import os
import sys
from urllib import response

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.triggers.date import DateTrigger
from random import randrange

# 連結google sheet
#import gspread
#from oauth2client.service_account import ServiceAccountCredentials
'''
import sys
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials as SAC
'''
#--------

reply = ("抱歉我看不懂請重新輸入QQQ","嗨！我的名字叫管理🐔\n請重新輸入關鍵字","好好講話喔😡咕咕咕","八寶丸好好吃！！！\n請重新輸入關鍵字","嗚嗚拉拉","我好餓！咕咕嘎嘎","狗狗ㄍㄝ？","嘰哩雞裡？","氣噗噗","?","??!!")
from fsm import TocMachine
from utils import send_text_message
import schedule
import time
load_dotenv()

notify = 1
machine = TocMachine(
    states=["user", "enterFood","enterDate","enternum", "comfirm", "showAll","deletedfood", "delete","recommand","name","ask","info","new","delete2","recommand2","ask2"],
    transitions=[
        #輸入食材流程
        {"trigger": "advance","source": "user","dest": "enterFood","conditions": "is_going_to_enterFood",},
        {"trigger": "advance","source": "enterFood","dest": "enterDate","conditions": "is_going_to_enterDate",},
        {"trigger": "advance","source": "enterDate","dest": "enternum","conditions": "is_going_to_enternum",},
        {"trigger": "advance","source": "enternum","dest": "name","conditions": "is_going_to_name",},
        {"trigger": "advance","source": "name","dest": "comfirm","conditions": "is_going_to_comfirm",},
        
        #顯示冰箱的菜
        {"trigger": "advance","source": "user","dest": "showAll","conditions": "is_going_to_showAll",},
        #使用說明
        {"trigger": "advance","source": "user","dest": "info","conditions": "is_going_to_info",},
        #新增冰箱
        {"trigger": "advance","source": "user","dest": "new","conditions": "is_going_to_new",},
        #刪除食材
        {"trigger": "advance","source": "user","dest": "deletedfood","conditions": "is_going_to_deletedfood",},
        {"trigger": "advance","source": "deletedfood","dest": "delete","conditions": "is_going_to_delete",},
        {"trigger": "advance","source": "delete","dest": "delete2","conditions": "is_going_to_delete2",},
        #推薦食譜一
        {"trigger": "advance","source": "user","dest": "ask","conditions": "is_going_to_ask",},
        {"trigger": "advance","source": "ask","dest": "recommand","conditions": "is_going_to_recommand",},
        #推薦食譜二
        {"trigger": "advance","source": "user","dest": "ask2","conditions": "is_going_to_ask2",},
        {"trigger": "advance","source": "ask2","dest": "recommand2","conditions": "is_going_to_recommand2",},

        {"trigger": "go_back", "source": ["enterFood", "showAll","enterDate","comfirm","delete2","recommand","name","info","new","recommand2","ask2"], "dest": "user"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")

def push_message(push_text_str):
    line_bot_api.push_message(user_id, TextSendMessage(text=push_text_str))
    

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)
user_id = "U227736503c290a9f5fbe50b3423d5df2"



@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"

  
@app.route("/webhook", methods=["POST"])
def webhook_handler():
    # test connect to google sheet
    '''
    def gsheet(self, stocks):
        scopes = ["https://spreadsheets.google.com/feeds"]
 
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
	    "credentials.json", scopes)
 
        client = gspread.authorize(credentials)
 
        sheet = client.open_by_key(
	        "b86448485f36973bf9e1af9dc6d52291c79338b6").sheet1  #第一個工作表
    # ---------------
    '''
    signature = request.headers["X-Line-Signature"]
    notify = 1
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")
    

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, reply[randrange(11)])
        if notify == 1:
            #push_message("for testing")
            notify = 0
        
    
    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    
    app.run(host="0.0.0.0", port=port, debug=True)
