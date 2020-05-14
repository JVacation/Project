from tkinter import *
#from mttkinter import mtTkinter as tk
import locale,threading
import socket
from PIL import Image, ImageTk
import clock, news, weather, cam, stock, splash, quotes
import json, time
from Naked.toolshed.shell import execute_js

getName = ""
enableCameraPreview = "enable"
clockCheckbox = ""
weatherCheckbox = ""
newsCheckbox = ""
stockCheckbox = ""
quoteCheckbox = ""
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
        self.tk.bind("<Return>", self.fullscreen)
        self.tk.bind("<Escape>", self.finishFullscreen)
        self.splash = splash.Splash(self.topFrame, 'JVacations Facial Recognition Smart Mirror', 48)
        self.splash.pack(side=TOP, anchor=CENTER, padx=100, pady=60)
        self.cam =  cam.Cam(self.topFrame, enableCameraPreview)
        self.cam.pack( anchor=CENTER, padx=100, pady=60)
        self.instructions1 = splash.Splash(self.bottomFrame, "To add or edit users visit: " + socket.gethostbyname(socket.gethostname()) + ":3000", 28)
        self.instructions1.pack(side=BOTTOM, anchor=N, padx=100, pady=20)
        self.instructions2 = splash.Splash(self.bottomFrame,"Stand in front of the mirror until the mirror recognises you and loads your settings.", 28)
        self.instructions2.pack(side=BOTTOM, anchor=N, padx=100, pady=20)
        self.getUserName()
        thread1.start()

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
                newsCategory = (p['newsCategory'])
                stockCheckbox = (p['stockCheckbox'])
                stockFrame = (p['stockFrame'])
                stockSide = (p['stockSide'])
                stockList = (p['stockList'])
                quoteCheckbox = (p['quoteCheckbox'])
            self.splash.pack_forget()
            self.cam.pack_forget()
            self.instructions1.pack_forget()
            self.instructions2.pack_forget()
            #Quotes
            if quoteCheckbox == 'enable':
                self.quotes = quotes.Quotes(self.bottomFrame)
                self.quotes.pack(anchor=N, padx=100, pady=60)
            #clock
            if clockCheckbox == 'enable':
                self.clock = clock.Clock(getattr(self, clockFrame)) 
                if clockFrame == 'topFrame':
                    self.clock.pack(side=clockSide, anchor=N, padx=100, pady=60)
                else:
                    self.clock.pack(side=clockSide, anchor=S, padx=100, pady=60)
            #weather
            if weatherCheckbox == 'enable':
                self.weather = weather.Weather(getattr(self, weatherFrame), weatherSide)
                if weatherFrame == 'topFrame':
                    self.weather.pack(side=weatherSide, anchor=N, padx=100, pady=60)
                else:
                    self.weather.pack(side=weatherSide, anchor=S, padx=100, pady=60)
            #news
            if newsCheckbox == 'enable':
                self.news = news.News(getattr(self, newsFrame), newsSide, newsCategory)
                if newsFrame == 'topFrame':
                    self.news.pack(side=newsSide, anchor=N, padx=100, pady=60)
                else:
                    self.news.pack(side=newsSide, anchor=S, padx=100, pady=60)
            #stock
            if stockCheckbox == 'enable':
                self.stock = stock.Stock(getattr(self, stockFrame), stockList)
                if stockFrame == 'topFrame':
                    self.stock.pack(side=stockSide, anchor=N, padx=100, pady=60)
                else:
                    self.stock.pack(side=stockSide, anchor=S, padx=100, pady=60)
            self.checkStillViewing()

    def checkStillViewing(self):
        if self.cam.readUserName() == "No User Detected":
            print ("NO USER")
            #self.showuser.pack_forget()
            for widget in self.topFrame.winfo_children():
                widget.destroy()
            for widget in self.bottomFrame.winfo_children():
                widget.destroy()
            self.splash = splash.Splash(self.topFrame, 'JVacations Facial Recognition Smart Mirror', 48)
            self.splash.pack(side=TOP, anchor=CENTER, padx=100, pady=60)
            self.cam =  cam.Cam(self.topFrame, enableCameraPreview)
            self.cam.pack( anchor=CENTER, padx=100, pady=60)
            self.instructions1 = splash.Splash(self.bottomFrame, "To add or edit users visit: " + socket.gethostbyname(socket.gethostname()) + ":3000", 28)
            self.instructions1.pack(side=BOTTOM, anchor=N, padx=100, pady=20)
            self.instructions2 = splash.Splash(self.bottomFrame,"Stand in front of the mirror until the mirror recognises you and loads your settings.", 28)
            self.instructions2.pack(side=BOTTOM, anchor=N, padx=100, pady=20)
            self.getUserName()
        else:
            self.tk.after(10000, self.checkStillViewing)

    def finishFullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"
    
    def fullscreen(self, event=None):
        self.state = not self.state
        self.tk.attributes("-fullscreen", self.state)
        return "break"

if __name__ == '__main__':
    w = FullscreenWindow()
    w.tk.mainloop()
