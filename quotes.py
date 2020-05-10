from tkinter import *
import requests,json,traceback,feedparser
from PIL import Image, ImageTk
import random

news_country_code = 'gb'
weather_api_token = '<TOKEN>' # create account at https://darksky.net/dev/
xlarge_text_size = 94
large_text_size = 48
medium_text_size = 28
small_text_size = 18


class Quotes(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.config(bg='black')
        self.quoteContainer = Frame(self, bg="black")
        self.quoteContainer.pack(side=TOP)
        self.quoteLbl = Label(self, text="", font=('Helvetica', medium_text_size), fg="white", bg="black")
        self.quoteLbl.pack(side=TOP, anchor=W)
        self.get_quote()

    def get_quote(self):
        line = random.choice(open('quotes.txt', 'r', encoding='utf-8').readlines())
        self.quoteLbl.config(text=line)
        self.after(5000, self.get_quote)
