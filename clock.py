from tkinter import *
import locale,threading,time,requests,json,traceback,feedparser
from PIL import Image, ImageTk
from contextlib import contextmanager

LOCALE_LOCK = threading.Lock()

time_format = 24 # 12 or 24
date_format = "%d %b, %Y" # check python doc for strftime() for options
xlText = 94
largeText = 48
mediumText = 28
smallText = 18
timeZone = '' # e.g. 'fr_FR' fro French, '' as default

@contextmanager
def setlocale(name): #thread proof function to work with locale
    with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)

class Clock(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        # initialize day of week
        self.day_of_week1 = ''
        self.dayOWLbl = Label(self, text=self.day_of_week1, font=('Helvetica', smallText), fg="white", bg="black")
        self.dayOWLbl.pack(side=TOP)
        # initialize date
        self.date1 = ''
        self.dateLbl = Label(self, text=self.date1, font=('Helvetica', smallText), fg="white", bg="black")
        self.dateLbl.pack()
        # initialize date time
        self.time1 = ''
        self.timeLbl = Label(self, font=('Helvetica', largeText), fg="white", bg="black")
        self.timeLbl.pack(side=TOP)
        self.tick()

    def tick(self):
        with setlocale(timeZone):
            if time_format == 12:
                time2 = time.strftime('%I:%M %p') #hour in 12h format
            else:
                time2 = time.strftime('%H:%M') #hour in 24h format

            day_of_week2 = time.strftime('%A')
            date2 = time.strftime(date_format)
            # if time string has changed, update it
            if time2 != self.time1:
                self.time1 = time2
                self.timeLbl.config(text=time2)
            if day_of_week2 != self.day_of_week1:
                self.day_of_week1 = day_of_week2
                self.dayOWLbl.config(text=day_of_week2)
            if date2 != self.date1:
                self.date1 = date2
                self.dateLbl.config(text=date2)
            # calls itself every 200 milliseconds
            # to update the time display as needed
            # could use >200 ms, but display gets jerky
            self.timeLbl.after(200, self.tick)