#from asyncio.windows_events import NULL
from itertools import count
from transitions.extensions import GraphMachine

from utils import send_showAll, send_text_message,send_showAll


class TocMachine(GraphMachine):
    date = []
    foodtype = []
    num = []
    count = 0
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
    #輸入食材流程
    def is_going_to_enterFood(self, event):
        text = event.message.text
        return text.lower() == "開始紀錄"

    def is_going_to_enterDate(self, event):
        text = event.message.text
        return True

    def is_going_to_comfirm(self, event):
        text = event.message.text
        return True

    #other
    def is_going_to_showAll(self, event):
        text = event.message.text
        return text.lower() == "查看冰箱"


    #輸入食材流程
    def on_enter_enterFood(self, event):
        print("I'm entering state1")

        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入菜名我們將會儲存至資料庫")
        
    
    #輸入日期
    def on_enter_enterDate(self, event):
        print("I'm entering state1")
        TocMachine.foodtype.append(event.message.text)
        reply_token = event.reply_token
        send_text_message(reply_token, "已收到菜名，請輸入保存期限，屆時會提醒你 "+TocMachine.foodtype[TocMachine.count])
        
    
    #確認
    def on_enter_comfirm(self, event):
        print("I'm entering state1")
        TocMachine.date.append(event.message.text)
        reply_token = event.reply_token
        send_text_message(reply_token, "已收到日期，跟你確認一下機制:\n"+TocMachine.foodtype[TocMachine.count]+"\n"+TocMachine.date[TocMachine.count])
        TocMachine.count+=1
        self.go_back()
    



    def on_enter_showAll(self, event):
        print("I'm entering state2")
        
        reply_token = event.reply_token
        text = ""
        for i in range (0,TocMachine.count):
            text = text + TocMachine.foodtype[i]+"\t"+TocMachine.date[i]+"\n"
        send_showAll(reply_token,text)
        
        self.go_back()

    def on_exit_showAll(self):
        print("Leaving state2")
