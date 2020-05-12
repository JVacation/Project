from tkinter import *
import requests,json,traceback
from PIL import Image, ImageTk

apiToken = 'f4b64fa2896f793c58ff296ca4876ab6' # create account at https://darksky.net/dev/
locationApiToken = '7cbae623103ed2b984af6751946ac77c' # www.ipstack.com
language = 'en' # see https://darksky.net/dev/docs/forecast for full list of language parameters values
weathUnit = 'uk2' # see https://darksky.net/dev/docs/forecast for full list of unit parameters values
latitude = None # Set this if IP location lookup does not work for you (must be a string)
longitude = None # Set this if IP location lookup does not work for you (must be a string)
xlText = 94
medText = 28
smallText = 18

			
imageList = { 
    'wind': "assets/wind.png",   
    'cloudy': "assets/cloud.png", 
    'partly-cloudy-day': "assets/partsun.png",
    'thunderstorm': "assets/storm.png", 
    'rain': "assets/rain.png",
    'tornado': "assests/twister.png",
    'hail': "assests/hailing.png"
    'snow-thin': "assets/snow.png",    
    'snow': "assets/snow.png",
    'clear-day': "assets/sun.png", 
    'fog': "assets/mist.png",
    'partly-cloudy-night': "assets/partmoon.png",  
    'clear-night': "assets/clearmoon.png",      
}

class Weather(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        self.currentLoc = ''
        self.forecast = ''
        self.image = ''
        self.current = ''
        self.temp = ''
        self.currentLocLbl = Label(self, font=('Helvetica', smallText), fg="white", bg="black")
        self.currentLocLbl.pack(side=TOP)
        self.degreesFrame = Frame(self, bg="black")
        self.degreesFrame.pack(side=TOP)
        self.imageLbl = Label(self.degreesFrame, bg="black")
        self.imageLbl.pack(side=LEFT, anchor=N, padx=20)
        self.tempLbl = Label(self.degreesFrame, font=('Helvetica', xlText), fg="white", bg="black")
        self.tempLbl.pack(side=LEFT, anchor=N)
        self.currentLbl = Label(self, font=('Helvetica', medText), fg="white", bg="black")
        self.currentLbl.pack(side=TOP)
        self.forecastLbl = Label(self, font=('Helvetica', smallText), fg="white", bg="black")
        self.forecastLbl.pack(side=TOP)
        self.grabWeather()

    def grabWeather(self):
        try:
            if latitude is None and longitude is None:
                # get location
                locURL = "http://api.ipstack.com/%s?access_key=%s" % (self.ip(),locationApiToken)
                request = requests.get(locURL)
                locObject = json.loads(request.text)
                lat = locObject['latitude']
                lon = locObject['longitude']
                currentLocv2 = "%s, %s" % (locObject['city'], locObject['region_code'])
                # get weather
                weatherURL = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (apiToken, lat,lon,language,weathUnit)
            else:
                currentLocv2 = ""
                # get weather
                weatherURL = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (apiToken, lat, lon, language,weathUnit)
            request = requests.get(weatherURL)
            weathObj = json.loads(request.text)
            tempv2 = "%s%s" % (str(int(weathObj['currently']['temperature'])), '\N{DEGREE SIGN}')
            currentv2 = weathObj['currently']['summary']
            forecastv2 = weathObj["hourly"]["summary"]

            imageId = weathObj['currently']['icon']
            imagev2 = None

            if imageId in imageList:
                imagev2 = imageList[imageId]

            if imagev2 is not None:
                if self.image != imagev2:
                    self.image = imagev2
                    image = Image.open(imagev2)
                    image = image.resize((100, 100), Image.ANTIALIAS)
                    image = image.convert('RGB')
                    photo = ImageTk.PhotoImage(image)

                    self.imageLbl.config(image=photo)
                    self.imageLbl.image = photo
            else:
                # remove image
                self.imageLbl.config(image='')

            if self.current != currentv2:
                self.current = currentv2
                self.currentLbl.config(text=currentv2)
            if self.forecast != forecastv2:
                self.forecast = forecastv2
                self.forecastLbl.config(text=forecastv2)
            if self.temp != tempv2:
                self.temp = tempv2
                self.tempLbl.config(text=tempv2)
            if self.currentLoc != currentLocv2:
                if currentLocv2 == ", ":
                    self.currentLoc = "Cannot Pinpoint Location"
                    self.currentLocLbl.config(text="Cannot Pinpoint Location")
                else:
                    self.currentLoc = currentLocv2
                    self.currentLocLbl.config(text=currentLocv2)
        except Exception as e:
            traceback.print_exc()
            print (("Error: %s. Cannot get weather." % e))

        self.after(600000, self.grabWeather)

    def ip(self):
        requestIP = requests.get("http://jsonip.com/")
        jsonIP = json.loads(requestIP.text)
        return jsonIP['ip']
