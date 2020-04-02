from Tkinter import *
from PIL import ImageTk, Image
import cv2
import face_recognition
import numpy as np

xlarge_text_size = 94
large_text_size = 48
medium_text_size = 28
small_text_size = 18
# Capture from camera
cap = cv2.VideoCapture(0)

obama_image = face_recognition.load_image_file("obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Load a second sample picture and learn how to recognize it.
biden_image = face_recognition.load_image_file("biden.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding
]
known_face_names = [
    "Barack Obama",
    "Joe Biden"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
# function for video streaming

class Cam(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.config(bg='black')
        self.title = 'User' # 'News' is more internationally generic
        self.titleLbl = Label(self, text=self.title, font=('Helvetica', medium_text_size), fg="white", bg="black")
        self.titleLbl.pack(side=TOP, anchor=W)
        self.userContainer = Frame(self, bg="white")
        self.userContainer.pack(side=TOP)
        self.get_video()

    def get_video(self):
        process_this_frame = True
        ret, frame = cap.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                user = NewsHeadline(self.userContainer, name)
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                else:
                    name = "Not detected"
                    user = NewsHeadline(self.userContainer, name)
                face_names.append(name)
        process_this_frame = not process_this_frame
        self.after(15000, self.get_video)

class userTitle(Frame):
    def __init__(self, parent, event_name=""):
        Frame.__init__(self, parent, bg='black')
        image = Image.open("assets/Newspaper.png")
        image = image.resize((25, 25), Image.ANTIALIAS)
        image = image.convert('RGB')
        photo = ImageTk.PhotoImage(image)
        self.iconLbl = Label(self, bg='black', image=photo)
        self.iconLbl.image = photo
        self.iconLbl.pack(side=LEFT, anchor=N)
        self.eventName = event_name
        self.eventNameLbl = Label(self, text=self.eventName, font=('Helvetica'), fg="black", bg="white")
        self.eventNameLbl.pack(side=LEFT, anchor=N)
        