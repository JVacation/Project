from yahoo_fin import stock_info as si
from tkinter import *
import requests,json,traceback,feedparser
from PIL import Image, ImageTk

class Stock(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.config(bg='black')
        self.title = 'Stocks' # 'News' is more internationally generic
        self.newsLbl = Label(self, text=self.title, font=('Helvetica', medium_text_size), fg="white", bg="black")
        self.newsLbl.pack(side=TOP, anchor=W)
        self.headlinesContainer = Frame(self, bg="black")
        self.headlinesContainer.pack(side=TOP)
        self.get_stocks()

    def get_stocks(self):
        stocks = listStocks(self.headlinesContainer, "amzn")
        stocks.pack(side=TOP, anchor=W)
        self.after(600000, self.get_stocks)


class listStocks(Frame):
    def __init__(self, parent, event_name=""):
        Frame.__init__(self, parent, bg='black')
        self.stockName = event_name
        image = Image.open("assets/dollar.png")
        image = image.resize((25, 25), Image.ANTIALIAS)
        image = image.convert('RGB')
        photo = ImageTk.PhotoImage(image)
        self.stockNameLbl = Label(self, text=self.stockName, font=('Helvetica', smallText), fg="white", bg="black")
        self.stockNameLbl.pack(side=TOP, anchor=N)
        self.iconLbl = Label(self, bg='black', image=photo)
        self.iconLbl.image = photo
        self.iconLbl.pack(side=LEFT, anchor=N)
        self.stockQuote = si.get_live_price(self.stockName)
        self.eventNameLbl = Label(self, text=self.stockQuote, font=('Helvetica'), fg="white", bg="black")
        self.eventNameLbl.pack(side=LEFT, anchor=N)