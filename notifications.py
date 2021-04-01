import json
import multiprocessing
import sys
import threading
import time
import webbrowser

import requests
from infi.systray import SysTrayIcon
from PIL import Image
from win10toast import ToastNotifier


class Notification:
    def __init__(self,Type,link,title,description,icon):
        self.type=Type
        self.link=link
        self.title=title
        self.description=description
        self.icon=icon
    def __str__(self):
        return self.title

class KThread(threading.Thread):
  """A subclass of threading.Thread, with a kill()
method."""
  def __init__(self, *args, **keywords):
    threading.Thread.__init__(self, *args, **keywords)
    self.killed = False

  def start(self):
    """Start the thread."""
    self.__run_backup = self.run
    self.run = self.__run      # Force the Thread to
# install our trace.
    threading.Thread.start(self)

  def __run(self):
    """Hacked run function, which installs the
trace."""
    sys.settrace(self.globaltrace)
    self.__run_backup()
    self.run = self.__run_backup

  def globaltrace(self, frame, why, arg):
    if why == 'call':
      return self.localtrace
    else:
      return None

  def localtrace(self, frame, why, arg):
    if self.killed:
      if why == 'line':
        raise SystemExit()
    return self.localtrace

  def kill(self):
    self.killed = True

stop_threads=False
def say_hello(systray):
    global icon_url
    webbrowser.open_new(icon_url)
    print("Stop icon")
    global icon_active
    icon_active=False
    systray.shutdown()
    
    # icon_thread.kill()
    # icon_thread.exit()
    # stop_threads= True
    # icon_thread.join()
    
def infisystray():
    menu_options = (("Say Hello", None, say_hello),)
    systray = SysTrayIcon("inprovo-favicon.ico", "Example tray icon", menu_options)
    systray.start()
    
    

def GetData():
    res=requests.get("https://app.inprovo.nl/api/v1/notifications")
    res=res.json()
    notifications=[]
    for i in res['notifications']:
        notifications.append(Notification(i['type'],i['url'],i['title'],i['description'],i['icon']))
    return notifications
def notify(title,text,url):
   noti.show_toast(title,text,duration=5, threaded=True,callback_on_click=action) 

def action():
    global url
    webbrowser.open_new(url)
    print("Done")    



 
noti = ToastNotifier()
global icon_active
icon_active=False
while True:
    starttime=time.time()
    #Code would come here
    notifications=GetData()
    print(notifications)
    
    if len(notifications) >0:
        for notification in notifications:
            print(notification.title)
            print(icon_active)
            
            if notification.type=="email" and icon_active ==False:
                print("activating icon")
                icon_url= notification.link
                icon_thread = threading.Thread(target=infisystray,name="icon_thread",args=(),daemon=True)
                icon_thread.start()
                # infisystray()
                # print(icon_thread.pid)
                
                
                icon_active=True
                
                
                # time.sleep(5)            
            elif notification.type!="email":
                # pass
                url=notification.link
                notify(notification.title,notification.description,notification.link)
                # x=threading.Thread(target=notify,args=(notification.title,notification.description,notification.link,))
                # threads.append(x)
                time.sleep(10)
    #Timer code
    time.sleep(5.0 - ((time.time() - starttime) % 5.0))

    # time.sleep(10)
    
