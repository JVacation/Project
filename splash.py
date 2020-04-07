from tkinter import *
import requests,json,traceback,feedparser
from PIL import Image, ImageTk

news_country_code = 'gb'
weather_api_token = '<TOKEN>' # create account at https://darksky.net/dev/
xlarge_text_size = 94
large_text_size = 48
medium_text_size = 28
small_text_size = 18

class Splash(Frame):
    def __init__(self, parent, event_name="", fontsize="", *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.config(bg='black')
        self.title = event_name # 'News' is more internationally generic
        self.newsLbl = Label(self, text=self.title, font=('Helvetica', fontsize), fg="white", bg="black")
        self.newsLbl.pack(side=TOP, anchor=W)