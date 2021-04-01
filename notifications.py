import requests
import json
import time
import tkinter as tk
from tkinter import *
import webbrowser
# from win10toast import ToastNotifier
from win10toast import ToastNotifier
from pystray import MenuItem as item
import pystray
from PIL import Image
import threading
class Notification:
    def __init__(self,Type,link,title,description,icon):
        self.type=Type
        self.link=link
        self.title=title
        self.description=description
        self.icon=icon
    def __str__(self):
        return self.title
def tray(icon,item):
    # print("Clicked")
    pass
def quit_window(icon, item):
    icon.stop()
    window.destroy()

def show_window(icon, item):
    icon.stop()
    window.after(0,window.deiconify)
state = False

def on_clicked(icon, item):
    global state
    state = not item.checked

def icon_action():
    image = Image.open("inprovo-favicon.ico")
    # menu = (item("name",tray),item("name",tray))
    menu = (item('Quit', quit_window), item('Show', show_window))
    # menu = (item('Quit', quit_window), item('Show', show_window))
    icon = pystray.Icon("name", image, "title", menu=menu(
    item(
        'Checkable',
        on_clicked,
        checked=lambda item: state))).run()
    
# icon.run()
from infi.systray import SysTrayIcon

def say_hello(systray):
    global icon_url
    webbrowser.open_new(icon_url)
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
icon_active=False
while True:
    starttime=time.time()
    #Code would come here
    notifications=GetData()
    print(notifications)
    
    if len(notifications) >0:
        for notification in notifications:
            print(notification.title)
            if notification.type=="email" and icon_active==False:
                icon_url= notification.link
                icon_thread = threading.Thread(target=infisystray,name="icon_thread",args=())
                icon_thread.start()
                icon_active=True
                
                
                # time.sleep(5)            
            else:
                pass
                url=notification.link
                notify(notification.title,notification.description,notification.link)
                x=threading.Thread(target=notify,args=(notification.title,notification.description,notification.link,))
                threads.append(x)
                time.sleep(10)
    #Timer code
    time.sleep(5.0 - ((time.time() - starttime) % 5.0))

    # time.sleep(10)
    
