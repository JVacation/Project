from PIL import Image
import face_recognition
import os, csv
import numpy as np
from numpy import savetxt
import pickle
import json
import shutil

all_face_encodings = {}
current_face_encodings = {}

if os.path.exists('./webserver/dataset_faces.dat'):
    with open('./webserver/dataset_faces.dat', 'rb') as f:
        current_face_encodings = pickle.load(f)

# Load the jpg file into a numpy array
i = 1
directory = './webserver/public/images/'

for subdir, dirs, files in os.walk(directory):
    for file in files:
        print((os.path.join(subdir, file)))
        image = face_recognition.load_image_file(os.path.join(subdir, file))
        folderName = os.path.basename(subdir)
        current_face_encodings[folderName] = face_recognition.face_encodings(image)[0]
     
with open('./webserver/dataset_faces.dat', 'wb') as f:
    pickle.dump(current_face_encodings, f)
 
if os.path.basename(subdir) != "images":
    print (subdir)
    shutil.rmtree(subdir) 

# Find all the faces in the image using the default HOG-based model.
# This method is fairly accurate, but not as accurate as the CNN model and not GPU accelerated.
# See also: find_faces_in_picture_cnn.py