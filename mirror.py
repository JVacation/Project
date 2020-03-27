# smartmirror.py
# requirements
# requests, feedparser, traceback, Pillow

from Tkinter import *
import locale,threading
from PIL import Image, ImageTk
import clock, news, weather, cam, stock
import json

# maps open weather icons to
# icon reading is not impacted by the 'lang' parameter
icon_lookup = {
    'clear-day': "assets/Sun.png",  # clear sky day
    'wind': "assets/Wind.png",   #wind
    'cloudy': "assets/Cloud.png",  # cloudy day
    'partly-cloudy-day': "assets/PartlySunny.png",  # partly cloudy day
    'rain': "assets/Rain.png",  # rain day
    'snow': "assets/Snow.png",  # snow day
    'snow-thin': "assets/Snow.png",  # sleet day
    'fog': "assets/Haze.png",  # fog day
    'clear-night': "assets/Moon.png",  # clear sky night
    'partly-cloudy-night': "assets/PartlyMoon.png",  # scattered clouds night
    'thunderstorm': "assets/Storm.png",  # thunderstorm
    'tornado': "assests/Tornado.png",    # tornado
    'hail': "assests/Hail.png"  # hail
}

jsonfile = 'constant'

with open('./json/' + jsonfile + '.json') as json_file:
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
        # clock
        if clockCheckbox == 'enable': 
           self.clock = clock.Clock(getattr(self, clockFrame))
           self.clock.pack(side=clockSide, anchor=N, padx=100, pady=60)
        # weather
        if weatherCheckbox == 'enable':
           self.weather = weather.Weather(getattr(self, weatherFrame))
           self.weather.pack(side=weatherSide, anchor=N, padx=100, pady=60)
        # news
        #if newsCheckbox == 'enable':
          # self.news = news.News(getattr(self, newsFrame))
           #self.news.pack(side=newsSide, anchor=S, padx=100, pady=60)

        self.cam =  cam.Cam(self.bottomFrame)
        self.cam.pack(side=LEFT, anchor=S, padx=60, pady=60)
        self.cam = cam.NewsHeadline(self.bottomFrame)
        self.cam.pack(side=RIGHT, anchor=S, padx=60, pady=60)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"


if __name__ == '__main__':
    w = FullscreenWindow()
    w.tk.mainloop()
