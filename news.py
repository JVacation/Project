from tkinter import *
import requests,json,traceback,feedparser
from PIL import Image, ImageTk

countryCode = 'gb'
medium_text_size = 28

class News(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.config(bg='black')
        self.newsLbl = Label(self, text="News", font=('Helvetica', medium_text_size), fg="white", bg="black")
        self.newsLbl.pack(side=TOP, anchor=W)
        self.breakingNews = Frame(self, bg="black")
        self.breakingNews.pack(side=TOP)
        self.getBreakingNews()

    def getBreakingNews(self):
        try:
            for widget in self.breakingNews.winfo_children():
                widget.destroy()
            if countryCode == None:
                newsURL = "https://news.google.com/news?ned=us&output=rss"
            else:
                newsURL = "https://news.google.com/news?ned=%s&output=rss" % countryCode
            newsFeed = feedparser.parse(newsURL)
            for post in newsFeed.entries[0:5]:
                newsLine = retrieveNewsLine(self.breakingNews, post.title)
                newsLine.pack(side=TOP, anchor=W)
        except Exception as e:
            traceback.print_exc()
            print (("%s UNABLE TO RETRIEVE NEWS" % e))
        self.after(600000, self.getBreakingNews)

class retrieveNewsLine(Frame):
    def __init__(self, parent, postName=""):
        Frame.__init__(self, parent, bg='black')
        image = Image.open("assets/Newspaper.png")
        image = image.resize((25, 25), Image.ANTIALIAS)
        image = image.convert('RGB')
        photo = ImageTk.PhotoImage(image)
        self.newspaperLbl = Label(self, bg='black', image=photo)
        self.newspaperLbl.image = photo
        self.newspaperLbl.pack(side=LEFT, anchor=N)
        self.newsName = postName
        self.newsNameLbl = Label(self, text=self.newsName, font=('Helvetica'), fg="white", bg="black")
        self.newsNameLbl.pack(side=LEFT, anchor=N)