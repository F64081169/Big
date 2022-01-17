#from asyncio.windows_events import NULL
from itertools import count
from transitions.extensions import GraphMachine
import datetime
from dateutil import rrule
import schedule
import time

from utils import send_showAll, send_text_message,send_showAll,job_that_executes_once

expireyear = []
expiremonth = []
expireday = []
oneday = []
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
        expire = event.message.text
        
         
        expireyear.append(expire.split()[0])
        expiremonth.append(expire.split()[1])
        expireday.append(expire.split()[2])
        today = datetime.date.today() 
        print(int(expire.split()[0]))
        print(int(expire.split()[1]))
        print(int(expire.split()[2]))
        oneday.append(datetime.date(int(expire.split()[0]),int(expire.split()[1]),int(expire.split()[2])))
        
        days = rrule.rrule(rrule.DAILY, dtstart=today, until=oneday).count()
        schedule.every(days).day.at("8:30").do(job_that_executes_once("你的"+TocMachine.foodtype[TocMachine.count])+"已到期")
        reply_token = event.reply_token
        send_text_message(reply_token, "已收到日期，跟你確認一下機制:\n"+TocMachine.foodtype[TocMachine.count]+"\n"+TocMachine.date[TocMachine.count]+ "\n"+str(days))
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
