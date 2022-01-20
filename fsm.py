#from asyncio.windows_events import NULL
from itertools import count
from transitions.extensions import GraphMachine
import datetime
from dateutil import rrule
import schedule
import time
from apscheduler.schedulers.background import BlockingScheduler,BackgroundScheduler
from apscheduler.triggers.date import DateTrigger

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
    def my_job():
        print('到期了')
        
    #輸入食材流程
    def is_going_to_enterFood(self, event):
        text = event.message.text
        return text.lower() == "開始記錄"

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
        print(expire.split()[0])
        print(expire.split()[1])
        print(expire.split()[2])
        reply_token = event.reply_token
        #oneday.append(datetime.date(int(expire.split()[0]),int(expire.split()[1]),int(expire.split()[2])))
         
        #days = rrule.rrule(rrule.DAILY, dtstart=today, until=oneday).count()
        #schedule.every(days).day.at("8:30").do(job_that_executes_once("你的"+TocMachine.foodtype[TocMachine.count])+"已到期")
        send_text_message(reply_token, "已收到日期，跟你確認一下機制:\n"+TocMachine.foodtype[TocMachine.count]+"\n"+TocMachine.date[TocMachine.count])#+TocMachine.foodtype[TocMachine.count]+"\n"+TocMachine.date[TocMachine.count]+ "\n"+str(days))
        scheduler = BackgroundScheduler()
        intervalTrigger=DateTrigger(run_date=expire.split()[0]+'-'+expire.split()[1]+'-'+expire.split()[2]+ 'T08:00:00+00:00')
        scheduler.add_job(TocMachine.my_job, intervalTrigger, id='my_job_id'+str(TocMachine.count))
        scheduler.start()
        
        
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

    # delete
    def is_going_to＿deletedfood(self, event):
        text = event.message.text
        return text.lower() == "刪除食材"

    def on_enter_deletedfood(self, event):
        print("I'm entering state1")

        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入要刪除的菜名")

    def is_going_to＿delete(self, event):
        text = event.message.text
        return True

    def on_enter_delete(self, event):
        print("I'm entering state1")
        #TocMachine.foodtype.append(event.message.text)
        length = len(TocMachine.foodtype)
        for i in range(0,length):
            if event.message.text == TocMachine.foodtype[i]:
                TocMachine.foodtype[i] = ""
                TocMachine.date[i] = ""
                #TocMachine.num[i] = ""
                break
        

        reply_token = event.reply_token 
        send_text_message(reply_token, "刪除成功！")

    def on_exit_delete(self): 
        print("Leaving state2")

