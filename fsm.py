#from asyncio.windows_events import NULL
from transitions.extensions import GraphMachine

from utils import send_text_message


class TocMachine(GraphMachine):
    date = []
    foodtype = []
    num = []
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
    #輸入食材流程
    def is_going_to_enterFood(self, event):
        text = event.message.text
        return text.lower() == "開始"

    def is_going_to_enterDate(self, event):
        text = event.message.text
        return True

    def is_going_to_comfirm(self, event):
        text = event.message.text
        return True

    #other
    def is_going_to_state2(self, event):
        text = event.message.text
        return text.lower() == "go to state2"


    #輸入食材流程
    def on_enter_enterFood(self, event):
        print("I'm entering state1")

        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入菜名我們將會儲存至資料庫")
        
    
    #輸入日期
    def on_enter_enterDate(self, event):
        print("I'm entering state1")

        reply_token = event.reply_token
        send_text_message(reply_token, "已收到菜名，請輸入保存期限，屆時會提醒你")
        
    
    #確認
    def on_enter_comfirm(self, event):
        print("I'm entering state1")

        reply_token = event.reply_token
        send_text_message(reply_token, "已收到日期，跟你確認一下機制")
        self.go_back()
    



    def on_enter_state2(self, event):
        print("I'm entering state2")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger state2")
        self.go_back()

    def on_exit_state2(self):
        print("Leaving state2")
