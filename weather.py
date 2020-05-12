from tkinter import *
import requests,json,traceback
from PIL import Image, ImageTk

apiToken = 'f4b64fa2896f793c58ff296ca4876ab6' # create account at https://darksky.net/dev/
locationApiToken = '7cbae623103ed2b984af6751946ac77c' # www.ipstack.com
language = 'en' # see https://darksky.net/dev/docs/forecast for full list of language parameters values
weathUnit = 'uk2' # see https://darksky.net/dev/docs/forecast for full list of unit parameters values
lat = None # Set this if IP location lookup does not work for you (must be a string)
lon = None # Set this if IP location lookup does not work for you (must be a string)
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
    'hail': "assests/hailing.png",
    'snow-thin': "assets/snow.png",    
    'snow': "assets/snow.png",
    'clear-day': "assets/sun.png", 
    'fog': "assets/mist.png",
    'partly-cloudy-night': "assets/partmoon.png",  
    'clear-night': "assets/clearmoon.png"      
}

class Weather(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        self.currentLoc = ''
        self.forecast = ''
        self.image = ''
        self.current = ''
        self.temp = ''
        # Packing Frame with Labels #
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
        # Calling Weather Function #
        self.grabWeather()


    # Weather Function # 
    def grabWeather(self):
        try:
            # Gets location from IP stack #
            locURL = "http://api.ipstack.com/%s?access_key=%s" % (self.ip(),locationApiToken)
            request = requests.get(locURL)
            locObject = json.loads(request.text)
            lat = locObject['latitude']
            lon = locObject['longitude']
            currentLocv2 = "%s, %s" % (locObject['city'], locObject['region_code'])

            # Gets Weather from Dark Sky API # 
            weatherURL = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (apiToken, lat,lon,language,weathUnit)
            request = requests.get(weatherURL)
            weathObj = json.loads(request.text)
            tempv2 = "%s%s" % (str(int(weathObj['currently']['temperature'])), '\N{DEGREE SIGN}')
            currentv2 = weathObj['currently']['summary']
            forecastv2 = weathObj["hourly"]["summary"]
            imageId = weathObj['currently']['icon']
            imagev2 = None

            # Checks if Image is in the list of assets#
            if imageId in imageList:
                imagev2 = imageList[imageId]

            # Scales picture to be suitable for widget #
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
                self.imageLbl.config(image='')

            # Sets Current Weather Label #
            if self.current != currentv2:
                self.current = currentv2
                self.currentLbl.config(text=currentv2)

            # Sets Forecast Label #
            if self.forecast != forecastv2:
                self.forecast = forecastv2
                self.forecastLbl.config(text=forecastv2)
            
            # Sets Temperature Label #
            if self.temp != tempv2:
                self.temp = tempv2
                self.tempLbl.config(text=tempv2)

            # Sets Current Location Label #
            if self.currentLoc != currentLocv2:
                if currentLocv2 == ", ":
                    self.currentLoc = "Could not find location"
                    self.currentLocLbl.config(text="Could not find location")
                else:
                    self.currentLoc = currentLocv2
                    self.currentLocLbl.config(text=currentLocv2)

        # Error handling #             
        except Exception as e:
            traceback.print_exc()
            print (("Error: %s. Cannot get weather." % e))

        # Updates Weather after 20 seconds #  
        self.after(20000, self.grabWeather)

    # Gets IP of device as JSON #
    def ip(self):
        # Calls JSON IP API #
        requestIP = requests.get("http://jsonip.com/")
        jsonIP = json.loads(requestIP.text)
        return jsonIP['ip']
