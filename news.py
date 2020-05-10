from tkinter import *
import requests,json,traceback,feedparser
from PIL import Image, ImageTk

class News(Frame):
    def __init__(self, parent, event_name="", category="", *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.config(bg='black')
        self.newsLbl = Label(self, text="News", font=('Helvetica', 28), fg="white", bg="black")
        if event_name == "left":
            self.newsLbl.pack(side=TOP, anchor=W)
        else:
            self.newsLbl.pack(side=TOP, anchor=E)
        self.breakingNews = Frame(self, bg="black")
        self.breakingNews.pack(side=TOP)
        self.getBreakingNews(event_name, category)

    def getBreakingNews(self, event_name="", category=""):
        try:
            for widget in self.breakingNews.winfo_children():
                widget.destroy()
            if category == "HEADLINES":
                newsURL = "https://news.google.com/news?ned=gb&output=rss"
            else:
                newsURL = "https://news.google.com/news/headlines/section/topic/%s?ned=gb&output=rss" % category
            newsFeed = feedparser.parse(newsURL)
            for post in newsFeed.entries[0:5]:
                newsLine = retrieveNewsLine(self.breakingNews, post.title, event_name)
                if event_name == "left": 
                    newsLine.pack(side=TOP, anchor=W)
                else:
                    newsLine.pack(side=TOP, anchor=E)
        except Exception as e:
            traceback.print_exc()
            print (("%s UNABLE TO RETRIEVE NEWS" % e))
        self.after(600000, self.getBreakingNews)

class retrieveNewsLine(Frame):
    def __init__(self, parent, postName="", event_name=""):
        Frame.__init__(self, parent, bg='black')
        image = Image.open("assets/Newspaper.png")
        image = image.resize((25, 25), Image.ANTIALIAS)
        image = image.convert('RGB')
        photo = ImageTk.PhotoImage(image)
        self.newspaperLbl = Label(self, bg='black', image=photo)
        self.newspaperLbl.image = photo
        if event_name == "left": 
            self.newspaperLbl.pack(side=LEFT, anchor=N)
        else:
            self.newspaperLbl.pack(side=RIGHT, anchor=N)
        self.newsName = postName
        self.newsNameLbl = Label(self, text=self.newsName, font=('Helvetica'), fg="white", bg="black")
        self.newsNameLbl.pack(side=LEFT, anchor=N)