from tkinter import *
import locale,threading,time,requests,json,traceback,feedparser
from PIL import Image, ImageTk
from contextlib import contextmanager

lockLocale = threading.Lock()

formatTime = 24 # 12 or 24
formatDate = "%d %b, %Y"
largeText = 48
smallText = 18
timeZone = '' # e.g. 'fr_FR' fro French, '' as default

@contextmanager
def setlocale(name): #thread proof function to work with locale
    with lockLocale:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)

class Clock(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        # initialize day of week
        self.dayOfWeek = ''
        self.dayOfWeekLbl = Label(self, text=self.dayOfWeek, font=('Helvetica', smallText), fg="white", bg="black")
        self.dayOfWeekLbl.pack(side=TOP)
        # initialize date
        self.date = ''
        self.dateLbl = Label(self, text=self.date, font=('Helvetica', smallText), fg="white", bg="black")
        self.dateLbl.pack()
        # initialize date time
        self.time = ''
        self.timeLbl = Label(self, font=('Helvetica', largeText), fg="white", bg="black")
        self.timeLbl.pack(side=TOP)
        self.updateTime()

    def updateTime(self):
        with setlocale(timeZone):
            if formatTime == 24:
                timev2 = time.strftime('%H:%M')
            else:
                timev2 = time.strftime('%I:%M %p')
            dayOfWeekv2 = time.strftime('%A')
            date2 = time.strftime(formatDate)
            if timev2 != self.time:
                self.time = timev2
                self.timeLbl.config(text=timev2)
            if dayOfWeekv2 != self.dayOfWeek:
                self.dayOfWeek = dayOfWeekv2
                self.dayOfWeekLbl.config(text=dayOfWeekv2)
            if date2 != self.date:
                self.date = date2
                self.dateLbl.config(text=date2)
            # calls itself every 200 milliseconds
            # to update the time display as needed
            # could use >200 ms, but display gets jerky
            self.timeLbl.after(200, self.updateTime)