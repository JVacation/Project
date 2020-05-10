from yahoo_fin import stock_info as si
from tkinter import *
import requests,json,traceback,feedparser
from PIL import Image, ImageTk


xlarge_text_size = 94
large_text_size = 48
medium_text_size = 28
small_text_size = 18
smallText = 18

class Stock(Frame):
    def __init__(self, parent, event_name="", *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.config(bg='black')
        self.title = 'Stocks' # 'News' is more internationally generic
        self.newsLbl = Label(self, text=self.title, font=('Helvetica', medium_text_size), fg="white", bg="black")
        self.newsLbl.pack(side=TOP, anchor=N)
        self.headlinesContainer = Frame(self, bg="black")
        self.headlinesContainer.pack(side=TOP)
        self.get_stocks(event_name)

    def get_stocks(self, event_name=""):
        self.stockList = event_name.split(",")
        for stock in self.stockList:
            stocks = listStocks(self.headlinesContainer, stock)
            stocks.pack(side=TOP, anchor=N)
        self.after(5000, self.get_stocks)


class listStocks(Frame):
    def __init__(self, parent, event_name=""):
        Frame.__init__(self, parent, bg='black')
        self.stockName = event_name
        image = Image.open("assets/dollar.png")
        image = image.resize((25, 25), Image.ANTIALIAS)
        image = image.convert('RGB')
        photo = ImageTk.PhotoImage(image)
        self.stockNameLbl = Label(self, text=self.stockName, font=('Helvetica'), fg="white", bg="black")
        self.stockNameLbl.pack(side=TOP, anchor=N)
        self.iconLbl = Label(self, bg='black', image=photo)
        self.iconLbl.image = photo
        self.iconLbl.pack(side=LEFT, anchor=W)
        self.stockQuote = si.get_live_price(self.stockName)
        self.eventNameLbl = Label(self, text=round(self.stockQuote, 3), font=('Helvetica'), fg="white", bg="black")
        self.eventNameLbl.pack(side=LEFT, anchor=W)