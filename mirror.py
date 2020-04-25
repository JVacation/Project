# smartmirror.py
# requirements
# requests, feedparser, traceback, Pillow

from tkinter import *
#from mttkinter import mtTkinter as tk
import locale,threading
from PIL import Image, ImageTk
import clock, news, weather, cam, stock, splash
import json, time
from Naked.toolshed.shell import execute_js

getName = ""
enableCameraPreview = "enable"
xlarge_text_size = 94

class startWebServer (threading.Thread):
    def __init__(self):
      threading.Thread.__init__(self)
    def run(self):
      success = execute_js('./webserver/server.js')

thread1 = startWebServer()

class FullscreenWindow:

    def __init__(self):
        self.tk = Tk()
        self.tk.configure(background='black')
        self.topFrame = Frame(self.tk, background = 'black')
        self.bottomFrame = Frame(self.tk, background = 'black')
        self.topFrame.pack(side = TOP, fill=BOTH, expand = YES)
        self.bottomFrame.pack(side = BOTTOM, fill=BOTH, expand = YES)
        self.state = False
        self.tk.bind("<Return>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        self.splash = splash.Splash(self.topFrame, 'JVacations Facial Recognition Smart Mirror', 48)
        self.splash.pack(side=TOP, anchor=CENTER, padx=100, pady=60)
        self.cam =  cam.Cam(self.topFrame, enableCameraPreview)
        self.cam.pack( anchor=CENTER, padx=100, pady=60)
        self.instructions = splash.Splash(self.bottomFrame, 'Wait for the mirror to recognise your face and wait till your settings load', 28)
        self.instructions.pack(side=BOTTOM, anchor=CENTER, padx=100, pady=60)
        self.getUserName()
        thread1.start()

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"

    def getUserName(self):
        getName = self.cam.readUserName()
        print (getName)
        if getName == "Unknown" or getName == "No User Detected":
            self.tk.after(5000, self.getUserName)
        else:
            jsonfile = getName
            with open('./json/' + getName + '.json') as json_file:
                data = json.load(json_file)
            for p in data[jsonfile]:
                clockCheckbox = (p['clockCheckbox'])
                clockFrame = (p['clockFrame'])
                clockSide = (p['clockSide'])
                weatherCheckbox = (p['weatherCheckbox'])
                weatherFrame = (p['weatherFrame'])
                weatherSide = (p['weatherSide'])
                newsCheckbox = (p['newsCheckbox'])
                newsFrame = (p['newsFrame'])
                newsSide = (p['newsSide'])
                stockCheckbox = (p['stockCheckbox'])
                stockFrame = (p['stockFrame'])
                stockSide = (p['stockSide'])
                stockList = (p['stockList'])
            self.splash.pack_forget()
            self.cam.pack_forget()
            self.instructions.pack_forget()
            #self.showUser = splash.Splash(self.topFrame, getName, 12)
            #self.showUser.pack(side=TOP, anchor=N, padx=0, pady=0)
            #clock
            if clockCheckbox == 'enable': 
                self.clock = clock.Clock(getattr(self, clockFrame))
                self.clock.pack(side=clockSide, anchor=N, padx=100, pady=60)
            #weather
            if weatherCheckbox == 'enable':
                self.weather = weather.Weather(getattr(self, weatherFrame))
                self.weather.pack(side=weatherSide, anchor=N, padx=100, pady=60)
            #news
            if newsCheckbox == 'enable':
                self.news = news.News(getattr(self, newsFrame))
                self.news.pack(side=newsSide, anchor=S, padx=100, pady=60)
            #stock
            if stockCheckbox == 'enable':
                self.stock = stock.Stock(getattr(self, newsFrame), stockList)
                self.stock.pack(side=stockSide, anchor=S, padx=100, pady=60)
            self.checkStillViewing()

    def checkStillViewing(self):
        if self.cam.readUserName() == "No User Detected":
            print ("NO USER")
            #self.showuser.pack_forget()
            self.clock.pack_forget()
            self.weather.pack_forget()
            self.news.pack_forget()
            self.stock.pack_forget()
            self.splash.pack(side=TOP, anchor=CENTER, padx=100, pady=60)
            self.cam.pack(side=TOP, anchor=CENTER, padx=100, pady=60)
            self.instructions.pack(side=BOTTOM, anchor=CENTER, padx=100, pady=60)
            self.getUserName()
        else:
            self.tk.after(10000, self.checkStillViewing)

if __name__ == '__main__':
    w = FullscreenWindow()
    w.tk.mainloop()
